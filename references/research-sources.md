# Research Sources

This file captures the higher-signal sources used to shape this skill on April 25, 2026.

## Official

| Source | What it contributed |
| --- | --- |
| [OpenAI Image Generation Guide](https://developers.openai.com/api/docs/guides/image-generation) | Confirms the current API workflow for image generation and editing. |
| [OpenAI GPT Image Prompting Guide](https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide) | Useful prompt construction guidance for structure-heavy image tasks. |
| [OpenAI API model page for gpt-image-2](https://platform.openai.com/docs/models/gpt-image-2) | Model reference target for this skill. |

## GitHub Prompt Libraries

All repository stats below were re-checked on April 25, 2026 via the GitHub API.

| Source | Current signal | Why it matters |
| --- | --- | --- |
| [EvoLinkAI/awesome-gpt-image-2-prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts) | 3,530 stars, updated 2026-04-25 | Best current source for X-attributed prompt cases, image directories, and scene breadth. |
| [YouMind-OpenLab/awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2) | 2,265 stars, updated 2026-04-25 | Strongest category system and many structure-heavy commercial / layout prompt templates. |
| [Anil-matcha/Awesome-GPT-Image-2-API-Prompts](https://github.com/Anil-matcha/Awesome-GPT-Image-2-API-Prompts) | 1,680 stars, updated 2026-04-25 | Useful exact prompts for portraits, notebooks, UI, posters, and edit workflows. |
| [ZeroLu/awesome-gpt-image](https://github.com/ZeroLu/awesome-gpt-image) | 512 stars, updated 2026-04-25 | Good X-sourced cases for panorama, typography, documents, and prompt minimalism. |

## Recent X Signals Worth Reusing

| Date | Source | Reusable angle | Prompt status |
| --- | --- | --- | --- |
| 2026-04-25 | [Worldbuilding set with prompt in ALT](https://x.com/i/web/status/2046866168208916503) | Multi-image consistency for brand world / IP bible / concept pack | Exact ALT prompt captured |
| 2026-04-25 | [Single restaurant photo -> brand guideline](https://x.com/i/web/status/2046869915034890703) | One reference image expanded into a full mini brand system board | Reference-first workflow, prompt not fully public |
| 2026-04-25 | [Medical infographic JSON prompt](https://x.com/i/web/status/2046891801072501046) | Structured schema prompt for medical long image / poster | Partial prompt captured |
| 2026-04-25 | [Fenty-style email campaign sequence](https://x.com/i/web/status/2046717569013293231) | Lifecycle marketing visuals and email module packs | Exact prompt captured |
| 2026-04-25 | [Advanced Stephen Curry poster](https://x.com/i/web/status/2047030997175124052) | One-prompt sports / celebrity poster generation | Exact prompt captured |
| 2026-04-25 | [360 panorama conversion flow](https://x.com/i/web/status/2046717349945135472) | Base image -> equirectangular panorama workflow | Exact second-step prompt captured |
| 2026-04-25 | [Chinese clerical script layout](https://x.com/i/web/status/2047882040096559249) | Chinese typography and calligraphy-led poster work | Exact topic prompt captured |
| 2026-04-23 | [Chinese infographic prompt](https://x.com/i/web/status/2047153211560399009) | Web-research-to-infographic workflow | Pattern captured |
| 2026-04-22 | [Chinese comic generation](https://x.com/i/web/status/2047065819796930579) | Story-to-comic multi-page packaging | Pattern captured |
| 2026-04-22 | [Scientist manga with reference image](https://x.com/i/web/status/2046778077905056068) | Reference-image-driven comic adaptation | Pattern captured |

## Chinese Articles Discovered

These are discovery leads for later deep-reading. They are useful because they surface commercial use cases, but they are not yet normalized into the main case table.

- `OpenAI ChatGPT Images 2.0的10个疯狂案例`
- `10个案例上手ChatGPT Images 2.0`
- `玩疯了的ChatGPT Images 2.0`
- `ChatGPT Images 2.0 正式发布,附最新社区评测`
- `ChatGPT Images 2.0对比Midjourney,谁更适合电商`
- `ChatGPT Images 2.0:会排版、会写字、还能直接干活`
- `gpt-image-2 火了,但我只关心一件事:能不能帮门厂客户解决获客卡点`

## Local Asset Notes

- Asset download manifest lives in [case-assets.json](case-assets.json).
- Structured reusable cases live in [case-library.json](case-library.json).
- Prompt shortcuts grouped by scene live in [prompt-index.md](prompt-index.md).
- Refresh raw upstream sources with:

```bash
python scripts/sync_case_sources.py
```

- Download reference images with:

```bash
python scripts/fetch_case_assets.py
```
