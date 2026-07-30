#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
from typing import Iterable

import requests

from env_config import (
    AUTH_ENV_KEYS,
    BASE_URL_ENV_KEYS,
    apply_local_env,
    first_env_value,
)


DEFAULT_BASE_URL = "https://api.openai.com/v1"


def default_base_url() -> str:
    return (
        first_env_value(os.environ, BASE_URL_ENV_KEYS)
        or DEFAULT_BASE_URL
    ).rstrip("/")


def auth_key() -> str:
    token = first_env_value(os.environ, AUTH_ENV_KEYS)
    if not token:
        raise SystemExit("Missing auth key. Set OPENAI_API_KEY.")
    return token


def build_endpoint(base_url: str, path: str) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    if base_url.endswith("/v1") and normalized_path.startswith("/v1/"):
        return f"{base_url}{normalized_path[3:]}"
    return f"{base_url}{normalized_path}"


def ensure_out_dir(path: str) -> Path:
    out_dir = Path(path).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def write_outputs(payload: dict, out_dir: Path, mode: str) -> None:
    metadata_path = out_dir / f"{mode}-response.json"
    metadata_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    for idx, item in enumerate(payload.get("data", []), start=1):
        if item.get("b64_json"):
            image_bytes = base64.b64decode(item["b64_json"])
            output_path = out_dir / f"{mode}-{idx:02d}.png"
            output_path.write_bytes(image_bytes)
        elif item.get("url"):
            output_path = out_dir / f"{mode}-{idx:02d}.url.txt"
            output_path.write_text(item["url"], encoding="utf-8")


def generate(args: argparse.Namespace) -> None:
    url = build_endpoint(args.base_url, "/v1/images/generations")
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "n": args.n,
        "response_format": args.response_format,
    }
    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {auth_key()}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=args.timeout,
    )
    response.raise_for_status()
    result = response.json()
    write_outputs(result, ensure_out_dir(args.out), "generate")


def iter_files(paths: Iterable[str]):
    for path_str in paths:
        path = Path(path_str).expanduser().resolve()
        if not path.is_file():
            raise SystemExit(f"Image not found: {path}")
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        yield ("image[]", (path.name, path.read_bytes(), content_type))


def edit(args: argparse.Namespace) -> None:
    url = build_endpoint(args.base_url, "/v1/images/edits")
    files = list(iter_files(args.image))
    if len(files) == 1:
        name, value = files[0]
        files = [("image", value)]
    data = {
        "model": args.model,
        "prompt": args.prompt,
        "n": str(args.n),
        "response_format": args.response_format,
    }
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {auth_key()}"},
        data=data,
        files=files,
        timeout=args.timeout,
    )
    response.raise_for_status()
    result = response.json()
    write_outputs(result, ensure_out_dir(args.out), "edit")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run OpenAI-compatible image generation or editing with gpt-image-2.")
    parser.add_argument("--base-url", default=default_base_url(), help="Base URL, defaults to local config, OPENAI_BASE_URL, or https://api.openai.com/v1")
    parser.add_argument("--timeout", type=int, default=180, help="HTTP timeout in seconds")

    subparsers = parser.add_subparsers(dest="command", required=True)

    generate_parser = subparsers.add_parser("generate", help="Text-to-image generation")
    generate_parser.add_argument("--prompt", required=True, help="Prompt text")
    generate_parser.add_argument("--model", default="gpt-image-2", help="Model name")
    generate_parser.add_argument("--n", type=int, default=1, choices=range(1, 5), help="Number of outputs, 1-4")
    generate_parser.add_argument("--response-format", default="b64_json", choices=["b64_json", "url"])
    generate_parser.add_argument("--out", required=True, help="Output directory")
    generate_parser.set_defaults(func=generate)

    edit_parser = subparsers.add_parser("edit", help="Image editing")
    edit_parser.add_argument("--prompt", required=True, help="Edit prompt")
    edit_parser.add_argument("--image", required=True, nargs="+", help="One or more input image paths")
    edit_parser.add_argument("--model", default="gpt-image-2", help="Model name")
    edit_parser.add_argument("--n", type=int, default=1, choices=range(1, 5), help="Number of outputs, 1-4")
    edit_parser.add_argument("--response-format", default="b64_json", choices=["b64_json", "url"])
    edit_parser.add_argument("--out", required=True, help="Output directory")
    edit_parser.set_defaults(func=edit)

    return parser


def main() -> None:
    apply_local_env()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
