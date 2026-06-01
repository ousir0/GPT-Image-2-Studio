# GPT Image 2 Studio

`GPT Image 2 Studio` is an open Codex skill for turning a rough visual brief into structured `gpt-image-2` prompts, API calls, and reusable visual deliverables.

It is designed for people who do not want to rely on a single giant prompt. Instead, it helps break image work into a repeatable workflow:

1. collect source material
2. choose a scenario scaffold
3. compile a structured prompt
4. generate or edit with an OpenAI-compatible image API
5. package the result into a poster, infographic, storyboard, PPT visual set, brand board, or other design asset

## Open-Source Notes

- The skill is repository-ready, but you should still review any bundled examples before publishing if you want a stricter public subset.
- Local portfolio references in `references/` are best treated as optional research material, not required runtime dependencies.
- API credentials are never committed; configure them through environment variables.

## What It Supports

This skill supports both single-image and multi-image workflows.

### Core image operations

- Text-to-image generation with `gpt-image-2`
- Single-image and multi-image edit flows
- OpenAI-compatible `/v1/images/generations` and `/v1/images/edits`
- Optional Responses API mode for compatible deployments
- Local saving of prompts, API responses, and output images

### Prompt orchestration

- Structured prompt building instead of one-shot prompting
- Scenario catalog for picking a strong scene family quickly
- Prompt playbook with reusable prompt frames
- Case library and example assets for reuse
- Research notes and source tracking for reference-heavy jobs

### Deliverable types

- Single hero image
- Poster or campaign key visual
- Long infographic / vertical card
- Article cover and inline illustration pack
- Comic starter pack
- Storyboard / keyframe board
- UI mockup board
- PPT visual pack
- Game concept pack
- Brand guideline board / VI proposal board
- Panorama and immersive concept scenes

### Batch workflows

- Prompt-pack generation through `prompt_pack_builder.py`
- Manifest-based batch rendering through `render_manifest.py`
- Dry-run mode before spending image quota
- Retry, skip, and partial rerender support

## Repository Layout

```text
GPT-Image-2-Studio/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
├── assets/
├── references/
└── scripts/
```

Important files:

- `SKILL.md`: the Codex skill instructions
- `references/scene-catalog.csv`: scene families and reusable scaffolds
- `references/prompt-playbook.md`: prompt construction patterns
- `references/case-library.json`: reusable cases and provenance notes
- `scripts/gpt_image2_api.py`: direct API caller
- `scripts/prompt_pack_builder.py`: prompt-pack generator
- `scripts/render_manifest.py`: manifest renderer

## Quick Start

### 1. Set environment variables

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.example.com/v1"
```

`OPENAI_BASE_URL` is optional if your deployment uses the script default.

By default, the public scripts assume `https://api.openai.com/v1`.

### 2. Generate one image

```bash
python scripts/gpt_image2_api.py generate \
  --prompt "Create a premium Children's Day poster with clear Chinese headline space." \
  --model gpt-image-2 \
  --outdir ./outputs/children-day-poster
```

### 3. Edit an existing image

```bash
python scripts/gpt_image2_api.py edit \
  --prompt "Keep the product shape unchanged and turn it into a premium futuristic poster." \
  --image ./input.png \
  --model gpt-image-2 \
  --outdir ./outputs/product-edit
```

### 4. Build a prompt pack

```bash
python scripts/prompt_pack_builder.py \
  --scene poster \
  --brief "Launch visuals for an AI education product" \
  --style "clean, premium, trustworthy, future-facing" \
  --out ./outputs/ai-edu-pack
```

### 5. Render the manifest

```bash
python scripts/render_manifest.py \
  --manifest ./outputs/ai-edu-pack/manifest.json \
  --dry-run
```

Then run again without `--dry-run` when the prompts look right.

## Supported Prompt-Pack Scenes

- `ppt`
- `infographic`
- `comic`
- `ui`
- `poster`
- `article`
- `game`

Each scene expands into one or more prompt files plus a `manifest.json` that you can edit before rendering.

## API Notes

This skill assumes an OpenAI-compatible image backend.

Reliable parameters in the current scripts:

- `prompt`
- `model`
- `n`
- `response_format`

Do not rely on deployment-specific support for parameters such as:

- `size`
- `quality`
- `style`
- `background`

## Safety

This repository is for legitimate creative and design work.

It should not be used for:

- forged documents
- deceptive identity or evidence generation
- fraud assets
- unlabeled misinformation visuals

When working with factual public content, keep exact claims outside the image unless they have been verified.

## Good Fit

Use this skill when you want:

- stronger prompts for `gpt-image-2`
- repeatable creative workflows
- a reusable visual production system
- structured batch rendering
- design deliverables instead of raw image prompts only

## Limitations

- It does not guarantee perfect in-image typography.
- It does not replace a full design system or human brand strategist.
- It assumes the target API is OpenAI-compatible.
- Some references in `references/` are curated examples, not official documentation.

## Before You Publish Your Fork

- choose a license
- review bundled reference files for anything you do not want to distribute
- point examples to your preferred API base URL
- add screenshots or sample outputs if you want the GitHub page to be more discoverable

## License

This project is released under the MIT License.
