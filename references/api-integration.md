# API Integration

This skill is built around an OpenAI-compatible image API.

## Base URL

Default base URL:

```bash
https://api.openai.com/v1
```

The bundled scripts use `OPENAI_BASE_URL`, then fall back to this value.

The scripts normalize the endpoint path automatically, so both base URLs below are acceptable:

- `https://api.openai.com/v1`
- `https://api.openai.com`

## Auth

Pass an API key via environment variable or `--auth-key`.

Use one of:

- `OPENAI_API_KEY`

Never hardcode secrets into the skill.

## Generate

Endpoint:

```bash
POST /v1/images/generations
```

Reliable fields in this deployment:

- `prompt`
- `model`
- `n`
- `response_format`

Recommended starting call:

```bash
python scripts/gpt_image2_api.py generate \
  --prompt "一张高信息密度中文信息图，主题是濒危动物保护" \
  --model gpt-image-2 \
  --n 1 \
  --outdir ./outputs/animal-infographic
```

## Edit

Endpoint:

```bash
POST /v1/images/edits
```

Reliable fields in this deployment:

- `image` or `image[]`
- `prompt`
- `model`
- `n`
- `response_format`

Recommended starting call:

```bash
python scripts/gpt_image2_api.py edit \
  --prompt "保留主体构图，把它改成高级国风海报，加入中文标题留白" \
  --image ./input.png \
  --model gpt-image-2 \
  --outdir ./outputs/edit-01
```

## Batch Rendering

For multi-image deliverables, create a manifest first:

```bash
python scripts/prompt_pack_builder.py \
  --scene ppt \
  --brief "为 AI 教育产品做一套融资路演 PPT 配图" \
  --out ./outputs/ai-edu-ppt-pack
```

Then render:

```bash
python scripts/render_manifest.py \
  --manifest ./outputs/ai-edu-ppt-pack/manifest.json
```

## Deployment Reality

As of April 23, 2026 in this project:

- `gpt-image-2` is available and should be the primary model for this skill.
- `gpt-image-1` remains a fallback if you need a more conservative option.
- `n=1` to `n=4` is supported, but higher `n` is slower because the backend loops requests.
- `response_format=b64_json` is the safest option for local saving.

## Parameters To Avoid Depending On

These may appear in generic OpenAI examples, but the current deployment does not guarantee them:

- `size`
- `quality`
- `background`
- `output_format`
- `moderation`
- `style`

Treat them as non-authoritative in this environment.
