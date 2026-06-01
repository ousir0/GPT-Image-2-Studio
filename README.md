# GPT Image 2 Studio

[中文](#中文说明) | [English](#english)

---

## 中文说明

`GPT Image 2 Studio` 是一个面向 Codex / Agent 工作流的开源技能，用来把模糊的视觉需求整理成结构化的 `gpt-image-2` 提示词、API 调用流程，以及可复用的视觉交付物。

它不是“写一个超长 prompt 然后碰运气”，而是把出图过程拆成可重复执行的工作流：

1. 收集主题、受众、参考图和素材
2. 选择合适的场景脚手架
3. 生成结构化提示词
4. 调用 OpenAI 兼容图片接口做生成或编辑
5. 打包成海报、信息图、故事板、PPT 配图、品牌提案图等最终资产

## 这个仓库支持什么

### 核心能力

- 使用 `gpt-image-2` 进行文生图
- 支持单图和多图编辑
- 支持 OpenAI 兼容的 `/v1/images/generations` 和 `/v1/images/edits`
- 支持兼容部署下的 Responses API 模式
- 本地保存 prompt、API 响应和图片输出

### 提示词编排能力

- 结构化提示词，而不是一次性乱写
- 场景目录 `scene-catalog`
- 提示词手册 `prompt-playbook`
- 案例库 `case-library`
- 研究来源和复用线索整理

### 可直接支持的交付物

- 单张主视觉
- 活动海报 / 品牌 KV
- 长图信息图 / 竖版卡片
- 文章头图和内文配图组
- 漫画起稿包
- 分镜板 / 视频关键帧板
- UI 概念图
- PPT 配图包
- 游戏概念包
- 品牌指南板 / VI 提案板
- 全景图 / 沉浸式概念场景

### 批量工作流

- 通过 `prompt_pack_builder.py` 生成 prompt pack
- 通过 `render_manifest.py` 做 manifest 批量渲染
- 支持 `--dry-run` 先检查再消耗额度
- 支持重试、跳过和局部重跑

## 仓库结构

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

关键文件：

- `SKILL.md`：技能指令本体
- `references/scene-catalog.csv`：场景脚手架目录
- `references/prompt-playbook.md`：提示词构造手册
- `references/case-library.json`：案例库和来源说明
- `scripts/gpt_image2_api.py`：直接调用图片 API
- `scripts/prompt_pack_builder.py`：生成批量 prompt 包
- `scripts/render_manifest.py`：渲染 manifest

## 快速开始

### 1. 设置环境变量

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.example.com/v1"
```

如果你的环境已经有默认兼容接口，`OPENAI_BASE_URL` 可以不填。

公开版脚本默认以 `https://api.openai.com/v1` 为基线。

### 2. 生成一张图片

```bash
python scripts/gpt_image2_api.py generate \
  --prompt "Create a premium Children's Day poster with clear Chinese headline space." \
  --model gpt-image-2 \
  --outdir ./outputs/children-day-poster
```

### 3. 编辑一张已有图片

```bash
python scripts/gpt_image2_api.py edit \
  --prompt "Keep the product shape unchanged and turn it into a premium futuristic poster." \
  --image ./input.png \
  --model gpt-image-2 \
  --outdir ./outputs/product-edit
```

### 4. 生成一个 prompt pack

```bash
python scripts/prompt_pack_builder.py \
  --scene poster \
  --brief "Launch visuals for an AI education product" \
  --style "clean, premium, trustworthy, future-facing" \
  --out ./outputs/ai-edu-pack
```

### 5. 渲染 manifest

```bash
python scripts/render_manifest.py \
  --manifest ./outputs/ai-edu-pack/manifest.json \
  --dry-run
```

先用 `--dry-run` 检查，确认后再正式运行。

## 当前支持的 Prompt Pack 场景

- `ppt`
- `infographic`
- `comic`
- `ui`
- `poster`
- `article`
- `game`

每个场景会展开成多个 prompt 文件和一个可编辑的 `manifest.json`。

## API 说明

这个技能默认假设你使用的是 OpenAI 兼容图片接口。

当前脚本稳定依赖的字段：

- `prompt`
- `model`
- `n`
- `response_format`

不建议强依赖这些字段是否一定可用：

- `size`
- `quality`
- `style`
- `background`

## 安全边界

这个仓库面向正常创意生产和设计用途。

不适合用于：

- 伪造证件或文件
- 欺骗性身份素材
- 诈骗内容
- 未标注的误导性视觉内容

如果涉及公共事实内容，未经核实前，不要把精确事实直接写进图片。

## 适合什么场景

如果你想要：

- 更强的 `gpt-image-2` 提示词工作流
- 可重复执行的图像生产流程
- 批量图像任务编排
- 从 prompt 到最终设计资产的完整链路

那么这个技能很适合。

## 局限性

- 不能保证图中文字永远完美
- 不能替代完整品牌设计师或视觉总监
- 默认假设目标接口是 OpenAI 兼容接口
- `references/` 中部分内容是整理后的社区资料，不等同于官方文档

## 开源说明

- 这个仓库已经整理成可独立公开发布的版本
- API 密钥不会提交到仓库，需通过环境变量配置
- 如果你 fork 后要继续公开传播，建议自行复核案例素材与引用资料

## 许可证

本项目使用 [MIT License](./LICENSE)。

---

## English

`GPT Image 2 Studio` is an open-source skill for Codex / agent workflows. It helps turn a rough visual brief into structured `gpt-image-2` prompts, API calls, and reusable visual deliverables.

Instead of relying on one oversized prompt, it breaks image creation into a repeatable workflow:

1. gather topic, audience, references, and assets
2. choose a scene scaffold
3. compile a structured prompt
4. call an OpenAI-compatible image API for generation or editing
5. package the result into a poster, infographic, storyboard, PPT visual pack, brand board, or other final asset

## What This Repository Supports

### Core capabilities

- Text-to-image generation with `gpt-image-2`
- Single-image and multi-image editing
- OpenAI-compatible `/v1/images/generations` and `/v1/images/edits`
- Optional Responses API mode for compatible deployments
- Local saving of prompts, API responses, and output images

### Prompt orchestration

- Structured prompting instead of one-shot prompting
- `scene-catalog` for reusable scene scaffolds
- `prompt-playbook` for prompt construction patterns
- `case-library` for reusable examples
- research sources and reuse notes

### Deliverables

- Single hero image
- Poster / campaign key visual
- Long infographic / vertical card
- Article cover and inline illustration pack
- Comic starter pack
- Storyboard / keyframe board
- UI concept board
- PPT visual pack
- Game concept pack
- Brand guideline board / VI proposal board
- Panorama / immersive concept scenes

### Batch workflows

- Prompt-pack creation with `prompt_pack_builder.py`
- Manifest-based batch rendering with `render_manifest.py`
- `--dry-run` support before spending image quota
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

Key files:

- `SKILL.md`: the skill instructions
- `references/scene-catalog.csv`: reusable scene scaffolds
- `references/prompt-playbook.md`: prompt construction guide
- `references/case-library.json`: reusable cases and provenance notes
- `scripts/gpt_image2_api.py`: direct image API caller
- `scripts/prompt_pack_builder.py`: prompt-pack generator
- `scripts/render_manifest.py`: manifest renderer

## Quick Start

### 1. Set environment variables

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.example.com/v1"
```

If your environment already has a compatible default endpoint, `OPENAI_BASE_URL` is optional.

The public version defaults to `https://api.openai.com/v1`.

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

Use `--dry-run` first, then run it for real after reviewing the prompts.

## Supported Prompt-Pack Scenes

- `ppt`
- `infographic`
- `comic`
- `ui`
- `poster`
- `article`
- `game`

Each scene expands into one or more prompt files plus an editable `manifest.json`.

## API Notes

This skill assumes an OpenAI-compatible image backend.

Reliable parameters used by the current scripts:

- `prompt`
- `model`
- `n`
- `response_format`

Do not strongly depend on support for:

- `size`
- `quality`
- `style`
- `background`

## Safety

This repository is intended for legitimate creative and design work.

It should not be used for:

- forged documents
- deceptive identity assets
- fraud content
- unlabeled misleading visuals

If public facts are involved, keep exact factual claims out of the image unless they have been verified.

## Good Fit

Use this project if you want:

- stronger `gpt-image-2` prompting workflows
- repeatable image production pipelines
- batch orchestration for visual tasks
- an end-to-end path from prompt to design deliverable

## Limitations

- It does not guarantee perfect in-image typography.
- It does not replace a full brand designer or art director.
- It assumes the target backend is OpenAI-compatible.
- Some files in `references/` are curated community materials, not official documentation.

## Open-Source Notes

- This repository has been cleaned up for standalone public release.
- API credentials are not committed and must be provided through environment variables.
- If you redistribute or fork it publicly, it is worth reviewing bundled assets and references again.

## License

This project is released under the [MIT License](./LICENSE).
