#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
import requests

from env_config import (
    AUTH_ENV_KEYS,
    BASE_URL_ENV_KEYS,
    apply_local_env,
    first_env_value,
)


DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-image-2"


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt.strip()
    if args.prompt_file:
        return pathlib.Path(args.prompt_file).read_text(encoding="utf-8").strip()
    raise SystemExit("prompt or --prompt-file is required")


def get_auth_key(args: argparse.Namespace) -> str:
    return (args.auth_key or first_env_value(os.environ, AUTH_ENV_KEYS)).strip()


def get_base_url(args: argparse.Namespace) -> str:
    return (
        args.base_url
        or first_env_value(os.environ, BASE_URL_ENV_KEYS)
        or DEFAULT_BASE_URL
    ).rstrip("/")


def build_endpoint(base_url: str, path: str) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    if base_url.endswith("/v1") and normalized_path.startswith("/v1/"):
        return f"{base_url}{normalized_path[3:]}"
    return f"{base_url}{normalized_path}"


def ensure_outdir(path: str) -> pathlib.Path:
    outdir = pathlib.Path(path).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir


def http_json(url: str, payload: dict, auth_key: str, timeout: int) -> dict:
    last_error: requests.RequestException | None = None
    for attempt in range(3):
        try:
            response = requests.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {auth_key}",
                },
                json=payload,
                timeout=timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.ConnectionError as exc:
            last_error = exc
            if attempt == 2:
                break
            time.sleep(1.5 * (attempt + 1))

    assert last_error is not None
    raise last_error


def http_multipart(url: str, fields: dict, file_paths: list[str], auth_key: str, timeout: int) -> dict:
    files = []
    for file_path in file_paths:
        path = pathlib.Path(file_path).expanduser().resolve()
        mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        key = "image[]" if len(file_paths) > 1 else "image"
        files.append((key, (path.name, path.read_bytes(), mime_type)))

    last_error: requests.RequestException | None = None
    for attempt in range(3):
        try:
            response = requests.post(
                url,
                headers={"Authorization": f"Bearer {auth_key}"},
                data={key: str(value) for key, value in fields.items()},
                files=files,
                timeout=timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.ConnectionError as exc:
            last_error = exc
            if attempt == 2:
                break
            time.sleep(1.5 * (attempt + 1))

    assert last_error is not None
    raise last_error


def save_response(payload: dict, outdir: pathlib.Path, response_format: str) -> None:
    (outdir / "response.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    items = payload.get("data", [])
    if not isinstance(items, list):
        return

    for index, item in enumerate(items, start=1):
        revised = item.get("revised_prompt")
        if revised:
            (outdir / f"prompt-{index:02d}.txt").write_text(revised, encoding="utf-8")

        if response_format == "b64_json" and item.get("b64_json"):
            image_bytes = base64.b64decode(item["b64_json"])
            image_path = outdir / f"image-{index:02d}.png"
            image_path.write_bytes(image_bytes)
            print(image_path)
        elif response_format == "url" and item.get("url"):
            url_path = outdir / f"image-{index:02d}.url.txt"
            url_path.write_text(item["url"], encoding="utf-8")
            print(url_path)


def save_responses_image_response(payload: dict, outdir: pathlib.Path) -> None:
    (outdir / "response.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    index = 1
    for item in payload.get("output", []) or []:
        if item.get("type") == "image_generation_call" and item.get("result"):
            image_bytes = base64.b64decode(item["result"])
            image_path = outdir / f"image-{index:02d}.png"
            image_path.write_bytes(image_bytes)
            print(image_path)
            index += 1


def handle_generate(args: argparse.Namespace) -> int:
    auth_key = get_auth_key(args)
    if not auth_key:
        raise SystemExit("Missing auth key. Set OPENAI_API_KEY or use --auth-key.")

    prompt = read_prompt(args)
    outdir = ensure_outdir(args.outdir)
    if args.api_mode == "responses":
        payload = {
            "model": args.model or DEFAULT_MODEL,
            "input": prompt,
            "store": False,
        }
        url = build_endpoint(get_base_url(args), "/v1/responses")
        response = http_json(url, payload, auth_key=auth_key, timeout=args.timeout)
        save_responses_image_response(response, outdir)
        return 0

    payload = {
        "model": args.model or DEFAULT_MODEL,
        "prompt": prompt,
        "n": args.n,
        "response_format": args.response_format,
    }
    url = build_endpoint(get_base_url(args), "/v1/images/generations")
    response = http_json(url, payload, auth_key=auth_key, timeout=args.timeout)
    save_response(response, outdir, args.response_format)
    return 0


def handle_edit(args: argparse.Namespace) -> int:
    auth_key = get_auth_key(args)
    if not auth_key:
        raise SystemExit("Missing auth key. Set OPENAI_API_KEY or use --auth-key.")
    if not args.image:
        raise SystemExit("At least one --image is required for edit mode.")

    prompt = read_prompt(args)
    fields = {
        "model": args.model or DEFAULT_MODEL,
        "prompt": prompt,
        "n": args.n,
        "response_format": args.response_format,
    }
    outdir = ensure_outdir(args.outdir)
    url = build_endpoint(get_base_url(args), "/v1/images/edits")
    response = http_multipart(url, fields, args.image, auth_key=auth_key, timeout=args.timeout)
    save_response(response, outdir, args.response_format)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Call OpenAI-compatible gpt-image endpoints.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_common_arguments(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument("--prompt", help="Prompt text")
        subparser.add_argument("--prompt-file", help="Path to a UTF-8 prompt file")
        subparser.add_argument("--model", default=DEFAULT_MODEL, help="Model name")
        subparser.add_argument("--n", type=int, default=1, help="Number of images")
        subparser.add_argument(
            "--response-format",
            choices=["b64_json", "url"],
            default="b64_json",
            help="Response format returned by the API",
        )
        subparser.add_argument("--base-url", help="Base URL, defaults to OPENAI_BASE_URL or https://api.openai.com/v1")
        subparser.add_argument("--auth-key", help="API key, defaults to OPENAI_API_KEY")
        subparser.add_argument("--outdir", default="./gpt-image-output", help="Output directory")
        subparser.add_argument("--timeout", type=int, default=180, help="Request timeout in seconds")
        subparser.add_argument(
            "--api-mode",
            choices=["responses", "images"],
            default="images",
            help="Use the documented /v1/images/* endpoint by default; pass responses only for compatible Responses API deployments.",
        )

    generate = subparsers.add_parser("generate", help="Generate images from text")
    add_common_arguments(generate)
    generate.set_defaults(func=handle_generate)

    edit = subparsers.add_parser("edit", help="Edit one or more input images")
    add_common_arguments(edit)
    edit.add_argument("--image", action="append", help="Input image path", required=True)
    edit.set_defaults(func=handle_edit)

    return parser


def main() -> int:
    apply_local_env()
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        print(f"HTTP {exc.code}: {body}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        body = exc.response.text if getattr(exc, "response", None) is not None else ""
        if body:
            print(f"Request failed: {exc}\n{body}", file=sys.stderr)
        else:
            print(f"Request failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
