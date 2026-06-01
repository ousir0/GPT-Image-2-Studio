#!/usr/bin/env python3
import json
import pathlib
import urllib.request


ROOT = pathlib.Path(__file__).resolve().parents[1]
CACHE_ROOT = ROOT / "references" / "cache"
RAW_DIR = CACHE_ROOT / "raw"
NORMALIZED_DIR = CACHE_ROOT / "normalized"

SOURCES = [
    {
        "name": "openai-image-generation-guide",
        "kind": "html",
        "url": "https://developers.openai.com/api/docs/guides/image-generation",
    },
    {
        "name": "openai-gpt-image-prompting-guide",
        "kind": "html",
        "url": "https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide",
    },
    {
        "name": "evolink-awesome-gpt-image-2-readme",
        "kind": "markdown",
        "url": "https://raw.githubusercontent.com/EvoLinkAI/awesome-gpt-image-2-prompts/main/README.md",
    },
    {
        "name": "evolink-ingested-tweets",
        "kind": "json",
        "url": "https://raw.githubusercontent.com/EvoLinkAI/awesome-gpt-image-2-prompts/main/data/ingested_tweets.json",
    },
    {
        "name": "youmind-awesome-gpt-image-2-readme",
        "kind": "markdown",
        "url": "https://raw.githubusercontent.com/YouMind-OpenLab/awesome-gpt-image-2/main/README.md",
    },
    {
        "name": "anil-awesome-gpt-image-2-api-prompts-readme",
        "kind": "markdown",
        "url": "https://raw.githubusercontent.com/Anil-matcha/Awesome-GPT-Image-2-API-Prompts/main/README.md",
    },
    {
        "name": "zerolu-awesome-gpt-image-readme",
        "kind": "markdown",
        "url": "https://raw.githubusercontent.com/ZeroLu/awesome-gpt-image/main/README.md",
    },
]


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)

    manifest = []
    top_cases = []

    for source in SOURCES:
        content = fetch(source["url"])
        suffix = {
            "html": ".html",
            "markdown": ".md",
            "json": ".json",
        }[source["kind"]]
        raw_path = RAW_DIR / f"{source['name']}{suffix}"
        raw_path.write_bytes(content)

        item = {
            "name": source["name"],
            "kind": source["kind"],
            "url": source["url"],
            "raw_path": str(raw_path),
        }
        manifest.append(item)

        if source["name"] == "evolink-ingested-tweets":
            data = json.loads(content.decode("utf-8"))
            if isinstance(data, dict):
                data = data.get("records", [])
            if not isinstance(data, list):
                data = []

            def score(case: dict) -> int:
                return case.get("likeCount") or case.get("likes") or 0

            data = sorted(
                [case for case in data if isinstance(case, dict)],
                key=score,
                reverse=True,
            )

            for case in data[:30]:
                media = case.get("media") or case.get("media_urls") or []
                if media and isinstance(media[0], dict):
                    media_urls = [m.get("url") for m in media if m.get("url")]
                else:
                    media_urls = [m for m in media if isinstance(m, str)]

                top_cases.append(
                    {
                        "url": case.get("url") or case.get("tweet_url"),
                        "author": case.get("author") or case.get("author_handle"),
                        "title": case.get("title"),
                        "category": case.get("category"),
                        "createdAt": case.get("createdAt"),
                        "likes": case.get("likeCount") or case.get("likes"),
                        "retweets": case.get("retweetCount") or case.get("retweets"),
                        "views": case.get("viewCount") or case.get("views"),
                        "text": case.get("text") or case.get("prompt"),
                        "media_urls": media_urls,
                    }
                )

    (NORMALIZED_DIR / "source-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (NORMALIZED_DIR / "top-community-cases.json").write_text(
        json.dumps(top_cases, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"saved raw sources to {RAW_DIR}")
    print(f"saved normalized files to {NORMALIZED_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
