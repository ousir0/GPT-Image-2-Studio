#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import subprocess
import sys
import time


SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
API_SCRIPT = SCRIPT_DIR / "gpt_image2_api.py"


def has_auth(env: dict[str, str]) -> bool:
    return bool(
        env.get("OPENAI_API_KEY")
        or env.get("GPT_IMAGE_API_AUTH_KEY")
        or env.get("GPT_IMAGE_2_AUTH_KEY")
        or env.get("AUTH_KEY")
    )


def expected_success_marker(item: dict) -> pathlib.Path:
    return pathlib.Path(item["outdir"]).expanduser().resolve() / "response.json"


def item_status_path(item: dict) -> pathlib.Path:
    return pathlib.Path(item["outdir"]).expanduser().resolve() / "render-status.json"


def should_skip_item(item: dict, args: argparse.Namespace) -> bool:
    if args.force:
        return False
    return expected_success_marker(item).exists()


def write_item_status(item: dict, status: str, code: int, attempts_used: int) -> None:
    status_path = item_status_path(item)
    status_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "id": item.get("id"),
        "title": item.get("title"),
        "status": status,
        "code": code,
        "attempts_used": attempts_used,
        "outdir": item.get("outdir"),
    }
    status_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def render_item(item: dict, args: argparse.Namespace, env: dict[str, str]) -> tuple[int, int]:
    command = [
        sys.executable,
        str(API_SCRIPT),
        item.get("mode", "generate"),
        "--prompt-file",
        item["prompt_file"],
        "--model",
        item.get("model", args.model),
        "--n",
        str(item.get("n", args.n)),
        "--response-format",
        item.get("response_format", args.response_format),
        "--outdir",
        item["outdir"],
        "--timeout",
        str(args.timeout),
    ]

    for image_path in item.get("images", []):
        command.extend(["--image", image_path])

    if args.base_url:
        command.extend(["--base-url", args.base_url])

    print(" ".join(command))
    if args.dry_run:
        return 0, 0
    attempts = max(1, args.retries)
    for attempt in range(attempts):
        code = subprocess.run(command, env=env, check=False).returncode
        if code == 0:
            return 0, attempt + 1
        if attempt < attempts - 1:
            time.sleep(1.5 * (attempt + 1))
    return code, attempts


def write_summary(manifest_path: pathlib.Path, summary: dict) -> None:
    summary_path = manifest_path.parent / "render-summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def write_failures_manifest(manifest: dict, failed_items: list[dict], manifest_path: pathlib.Path) -> None:
    failure_manifest = {
        **manifest,
        "source_manifest": str(manifest_path),
        "items": failed_items,
    }
    out_path = manifest_path.parent / "failed-items.manifest.json"
    out_path.write_text(json.dumps(failure_manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a gpt-image-2 prompt pack manifest.")
    parser.add_argument("--manifest", required=True, help="Path to manifest.json")
    parser.add_argument("--limit", type=int, help="Only render the first N items")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without calling the API")
    parser.add_argument("--model", default="gpt-image-2", help="Default model if item does not specify one")
    parser.add_argument("--n", type=int, default=1, choices=range(1, 5), help="Default number of images")
    parser.add_argument("--response-format", default="b64_json", choices=["b64_json", "url"])
    parser.add_argument("--base-url", help="Optional API base URL")
    parser.add_argument("--timeout", type=int, default=180, help="HTTP timeout in seconds")
    parser.add_argument("--retries", type=int, default=2, help="Retries per manifest item on failure")
    parser.add_argument("--force", action="store_true", help="Re-render items even if response.json already exists")
    args = parser.parse_args()

    manifest_path = pathlib.Path(args.manifest).expanduser().resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = manifest.get("items", [])
    if args.limit:
        items = items[: args.limit]

    env = os.environ.copy()
    if not args.dry_run and not has_auth(env):
        raise SystemExit("Missing auth key. Set OPENAI_API_KEY.")

    summary = {
        "manifest": str(manifest_path),
        "total_items": len(items),
        "attempted_items": 0,
        "skipped_items": 0,
        "succeeded_items": 0,
        "failed_items": 0,
        "retries_per_item": args.retries,
        "force": args.force,
        "items": [],
    }
    failures = 0
    failed_items = []
    for item in items:
        if should_skip_item(item, args):
            summary["skipped_items"] += 1
            summary["items"].append(
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "status": "skipped",
                    "outdir": item.get("outdir"),
                }
            )
            continue

        summary["attempted_items"] += 1
        code, attempts_used = render_item(item, args, env)
        if code != 0:
            failures += 1
            summary["failed_items"] += 1
            failed_items.append(item)
            write_item_status(item, "failed", code, attempts_used)
            summary["items"].append(
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "status": "failed",
                    "code": code,
                    "attempts_used": attempts_used,
                    "outdir": item.get("outdir"),
                }
            )
            if not args.dry_run:
                print(f"failed: {item.get('id')} code={code}", file=sys.stderr)
        else:
            summary["succeeded_items"] += 1
            write_item_status(item, "succeeded", code, attempts_used)
            summary["items"].append(
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "status": "succeeded",
                    "attempts_used": attempts_used,
                    "outdir": item.get("outdir"),
                }
            )

    write_summary(manifest_path, summary)
    if failed_items:
        write_failures_manifest(manifest, failed_items, manifest_path)

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
