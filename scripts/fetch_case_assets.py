#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

import requests


def safe_name(url: str) -> str:
    path = urlparse(url).path
    name = Path(path).name or "asset"
    if "." not in name:
        name += ".bin"
    return name


def main() -> None:
    parser = argparse.ArgumentParser(description="Download media assets listed in case-assets.json")
    parser.add_argument(
        "--manifest",
        default=str(Path(__file__).resolve().parents[1] / "references" / "case-assets.json"),
        help="Path to case-assets.json",
    )
    parser.add_argument(
        "--out",
        default=str(Path(__file__).resolve().parents[1] / "assets" / "cases"),
        help="Output directory",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "gpt-image-2-studio-case-fetcher/1.0",
            "Accept": "*/*",
        }
    )

    entries = json.loads(manifest_path.read_text(encoding="utf-8"))
    for entry in entries:
        case_dir = out_dir / entry["id"]
        case_dir.mkdir(parents=True, exist_ok=True)
        meta_path = case_dir / "meta.json"
        meta_path.write_text(json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8")
        for index, media_url in enumerate(entry.get("media_urls", []), start=1):
            filename = f"{index:02d}-{safe_name(media_url)}"
            target = case_dir / filename
            if target.exists() and target.stat().st_size > 0:
                print(f"skip existing {target}")
                continue
            try:
                response = session.get(media_url, timeout=120)
                response.raise_for_status()
                target.write_bytes(response.content)
                print(f"saved {target}")
            except requests.RequestException as exc:
                print(f"failed {media_url}: {exc}")


if __name__ == "__main__":
    main()
