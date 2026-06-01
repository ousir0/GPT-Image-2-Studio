---
name: gpt-image-2-studio
description: "Use this skill when the user wants to generate or edit images with `gpt-image-2`, or package those images into richer deliverables such as PPT decks, long infographics, comics, posters, article illustrations, storyboards, marketing assets, panoramas, concept scenes, or other design-heavy outputs. Trigger when the request mentions `gpt-image-2`, image generation, image editing, poster design, PPT visuals, long images, manga/comics, infographics, product mockups, reference-image remixing, moodboards, concept art, virtual spaces, or when web research should be turned into scene-specific prompts and then rendered through an OpenAI-compatible image API."
---

# GPT Image 2 Studio

Use this skill as the orchestration layer around `gpt-image-2`.

The core idea is not "write one long prompt and hope." Instead:

1. Collect source material from the user, local files, or the web.
2. Pick a scenario scaffold from [references/scene-catalog.csv](references/scene-catalog.csv).
3. Build a structured prompt with [references/prompt-playbook.md](references/prompt-playbook.md).
4. Call the OpenAI-compatible image API with `gpt-image-2`.
5. Package the result into the requested deliverable such as PPT, long image, comic, article, storyboard, or concept pack.

## Read These Files

- Always read [references/api-integration.md](references/api-integration.md) before calling the API.
- Read [references/case-library.json](references/case-library.json) when you need reusable community cases with prompts, local assets, and source provenance.
- Read [references/prompt-playbook.md](references/prompt-playbook.md) when building or refining prompts.
- Read [references/prompt-index.md](references/prompt-index.md) when you want scene-grouped prompt shortcuts or local reference asset pointers.
- Read [references/scene-catalog.csv](references/scene-catalog.csv) when choosing a scenario or mining ideas.
- Read [references/research-sources.md](references/research-sources.md) when you need recent source links, update cues, or source provenance.

## Default Workflow

### 1. Lock the deliverable

If the request is ambiguous, quickly converge on one of these outputs:

- Single hero image
- Batch image set
- PPT / slide deck
- Long infographic / long poster
- Comic / manga pages
- Article cover + inline illustrations
- Product marketing pack
- UI / app mockup
- Panorama / immersive concept board
- Storyboard / video frame pack

If the request is already clear, do not ask more questions.

### 2. Gather input materials

Use the strongest available source mix:

- User brief, topic, audience, brand, or rough sketch
- Local reference images
- Web research if the user asks for fresh material or the task depends on current facts
- Existing style references or example URLs

For web research, prefer current primary or high-signal community sources. Recent `gpt-image-2` examples are changing fast.

### 3. Choose a scenario scaffold

Use `scene-catalog.csv` to map the request onto a repeatable scene type.

Strong default families:

- `information_dense`: infographic, comparison chart, educational poster, map, dashboard-like visual
- `narrative`: comic, storyboard, article illustration, carousel narrative, split-era collage
- `commercial`: e-commerce image, product poster, brand concept shop, menu, packaging scene
- `presentation`: PPT cover, section opener, background illustration, process diagram, stat scene
- `design_mockup`: app UI, landing page hero, UI screenshot, poster system
- `immersive`: panorama, isometric world, miniature store, environment concept, virtual room
- `editing`: style transfer, compositing, subject preservation, multi-image fusion

When speed matters, first check `case-library.json` for an existing scaffold close to the user's ask. Reuse proven prompt structure before inventing a new one.

When the user wants Chinese layout-heavy outputs, mini-program UI, menu design, local brand packaging, e-commerce edits, or business infographic formats, prefer `case-library.json` first. If you maintain your own local portfolio archive, you can add an optional local index alongside this skill.

### 4. Compile the prompt

Use this order unless the task clearly needs a variant:

1. Goal
2. Subject
3. Composition or page structure
4. Required text or labels
5. Style and material cues
6. Lighting / camera / rendering cues
7. Constraint list
8. Negative or exclusion cues

For tasks with text, layout, charts, panels, or multiple regions, be explicit about structure. `gpt-image-2` is especially valuable when the prompt includes:

- panel count
- section hierarchy
- label placement
- callout style
- typography intent
- reference-image preservation rules

### 5. Decide generate vs edit

Use `generations` when:

- the user mainly provides text instructions
- there is no hard reference image to preserve

Use `edits` when:

- the user provides one or more reference images
- layout, face, product, logo, or composition continuity matters
- you need style transfer, fusion, cleanup, recolor, scene swap, or derivative scenes

### 6. Call the API

For one-off images, use the bundled API script:

```bash
python skills/gpt-image-2-studio/scripts/gpt_image2_api.py generate \
  --prompt "..." \
  --model gpt-image-2 \
  --outdir ./outputs/demo
```

For editing:

```bash
python skills/gpt-image-2-studio/scripts/gpt_image2_api.py edit \
  --prompt "..." \
  --image ./input.png \
  --model gpt-image-2 \
  --outdir ./outputs/edit-demo
```

If the task is fragile, set `n=1` first, inspect the result, then iterate.

For richer tasks such as PPT packs, comics, infographics, article visuals, UI boards, posters, or game concept packs, do not call the API prompt-by-prompt manually. First create a prompt pack:

```bash
python skills/gpt-image-2-studio/scripts/prompt_pack_builder.py \
  --scene ppt \
  --brief "围绕 AI 教育产品做一套融资路演 PPT 配图" \
  --style "未来感、可信、教育科技、蓝绿色" \
  --out ./outputs/ai-edu-ppt-pack
```

Then review `manifest.json` and `prompts/*.txt`. When ready, render it:

```bash
python skills/gpt-image-2-studio/scripts/render_manifest.py \
  --manifest ./outputs/ai-edu-ppt-pack/manifest.json \
  --limit 1
```

Use `--dry-run` first if you only want to inspect the API commands without spending image quota.

### 7. Package the result

After image generation, do not stop if the user asked for a richer asset.

- PPT: use the `pptx` or `PowerPoint` skill to assemble slides.
- Long image: stack scenes into a vertical composition with clear sections.
- Comic: create page plan first, then page covers/panels, then export.
- Article: generate lead image, sectional illustrations, and optional inline pull-quote graphics.
- Storyboard/video: generate consistent keyframes, then pair them with copy or timing.
- Panorama/virtual space: generate equirectangular or isometric views, then add annotations or scene notes.

## Prompting Heuristics That Work Well

- Prefer concrete nouns over abstract adjectives.
- For dense visuals, specify section count, reading order, and labeling style.
- For editable scenes, state what must remain unchanged.
- For multi-image continuity, lock subject identity, outfit, palette, environment, and camera language.
- If you need Chinese text in-image, state the exact copy and limit the amount per region.
- For posters or slides, ask for whitespace and safe margins so downstream layout is easier.
- For product shots, describe the product geometry, materials, and camera setup before mood words.
- For comic tasks, define page count, panel count, text language, and speech-bubble density.

## Local API Constraints

This skill targets the OpenAI-compatible image API documented in [references/api-integration.md](references/api-integration.md).

Important constraints:

- Depend on `prompt`, `model`, `n`, and `response_format`.
- Do not assume `size`, `quality`, `style`, or `background` actually work in this deployment.
- Default to `gpt-image-2`, but if the user needs a stability fallback, mention `gpt-image-1`.
- Prefer `response_format=b64_json` for deterministic local saves.
- Use `response_format=url` when the user benefits from a directly shareable URL.

## Safety and Provenance

- Do not help create deceptive real-person fraud, forged evidence, fake official documents, or unlabeled misinformation assets.
- If the request is borderline but allowed, add a visible synthetic or concept label.
- When using web-collected facts, keep exact factual claims outside the image unless you verified them.
- For public-facing assets based on web research, keep a small source note in the deliverable whenever practical.

## Updating the Case Library

When the user asks to refresh the library:

1. Search recent official releases and community examples.
2. Append new rows to `scene-catalog.csv`.
3. Add structured reusable cases to `references/case-library.json`.
4. Add prompt-group summaries to `references/prompt-index.md`.
5. Refresh any optional local portfolio index files if your private portfolio archive changed.
6. Add source notes to `research-sources.md`.
7. Add media URLs to `references/case-assets.json`.
8. Run `fetch_case_assets.py` only if local asset snapshots are needed.

## Batch Prompt Packs

Use `prompt_pack_builder.py` whenever the user asks for more than one image or asks for an upper-level deliverable.

Supported first-class scenes:

- `ppt`: cover, section opener, process visual, data story, scenario visual, closing visual
- `infographic`: vertical information card / long image
- `comic`: character bible and first comic page
- `ui`: product UI concept board
- `poster`: commercial poster / banner key visual
- `article`: article hero, inline visual, summary card
- `game`: game world key art and game UI status screen

The generated `manifest.json` is intentionally editable. If a generated prompt is not aligned with the user's intent, edit the prompt file before running `render_manifest.py`.

## Output Expectation

Whenever possible, return:

- the final prompt used
- the saved output path(s)
- the scenario scaffold you selected
- any source assumptions or web sources used
