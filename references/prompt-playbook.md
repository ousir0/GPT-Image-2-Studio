# Prompt Playbook

Use these scaffolds to turn messy requests into robust `gpt-image-2` prompts.

## Core Prompt Frame

Use this skeleton first:

```text
Goal:
Create [deliverable] for [audience/use case].

Subject:
[main subject, entities, product, people, place, concept]

Structure:
[panel count / sections / reading order / layout / angle / crop / safe margins]

Required text:
[exact copy, language, hierarchy, labels, title, callouts]

Style:
[art direction, material, era, color palette, texture, rendering approach]

Visual cues:
[lighting, lens, camera, perspective, depth, environment, mood]

Constraints:
[must keep / must avoid / brand rules / reference preservation / no watermark]
```

## Scenario Scaffolds

### 1. PPT cover image

```text
Create a premium keynote cover illustration for a PPT about [topic].
The image should leave clean title space in the [top-left / center / right side].
Use a [minimal / cinematic / editorial / infographic-led] style.
Show [key subject or metaphor].
Keep composition simple enough for slide text overlay, with safe margins and no embedded small text.
Primary palette: [palette].
Audience: [executive / client / classroom / investor].
```

### 2. PPT section divider

```text
Create a wide visual divider image for a presentation section titled "[section name]".
Represent the idea of [concept] through [metaphor or scene].
Use a consistent palette with [brand cues].
Keep one focal area and broad negative space for overlay text.
No watermark, no dense typography.
```

### 3. Long infographic / poster

```text
Create a vertically structured Chinese infographic about [topic].
First research the subject if needed, then organize the image into [4-6] sections:
[section list].
Use clear visual grouping, icons or annotated drawings, and larger section headings.
Favor visual callouts over paragraphs.
Keep the layout readable on mobile and suitable for long-image sharing.
```

### 4. Article cover + inline pack

```text
Create an editorial image set for an article about [topic].
Image 1 is a high-impact hero cover.
Images 2-4 are supporting illustrations for [subtopics].
Keep a shared visual language across the set: [style].
No logos unless requested.
```

### 5. Chinese comic / manga pages

```text
Generate a full-color [Chinese / bilingual] comic based on the following story.
Total pages: [N].
Each page should read clearly from top to bottom and include [panel count] panels.
Style: [modern Chinese manga / cinematic graphic novel / watercolor comic].
Keep character appearance consistent across pages.
Use readable [Chinese / English] speech bubbles with concise dialogue.
Story:
[story outline]
```

### 6. Storyboard / video keyframes

```text
Create a storyboard pack for a short video about [topic].
Generate [N] frames covering: [shot list].
Keep the same subject identity, costume, color palette, and camera language.
Each frame should feel like a production-ready keyframe.
No subtitles unless requested.
```

### 7. Product marketing / e-commerce

```text
Create a product hero image for [product].
Show exact material cues: [metal, glass, matte plastic, paper, fabric].
Camera angle: [front / three-quarter / macro / exploded].
Background style: [clean white / colored gradient / lifestyle set].
Highlight [selling points].
Leave optional empty area for headline placement.
```

### 8. UI mockup / app screen

```text
Create a realistic UI showcase image for a [mobile app / web app] about [topic].
Show a polished interface with clear hierarchy, believable charts/cards/text blocks, and coherent design language.
Use [platform] conventions.
Keep typography crisp and the UI plausible enough for a product concept deck.
```

### 9. 3D concept store / miniature scene

```text
Create a 3D chibi-style miniature concept store for [brand].
The exterior should borrow from the brand's iconic product or packaging.
Show the storefront, signage, product display, and surrounding details in one hero shot.
Style: collectible diorama, premium toy-like materials, high detail.
```

### 10. Panorama / virtual space

```text
Create a 360 equirectangular panorama of [place or imagined world].
The scene should wrap seamlessly and remain readable as an immersive environment.
Add environmental storytelling through props and lighting, not dense text.
```

### 11. Single photo -> brand guideline pack

```text
Use the provided reference photo as the seed for a complete mini brand guideline.
Output a cohesive presentation board containing:
- hero brand photo treatment
- logo direction
- color palette
- typography direction
- packaging or signage mockup
- one social post or campaign thumbnail

Keep the mood, materials, and space cues consistent with the reference image.
Do not copy existing trademarks unless explicitly requested.
Use clean grid layout, premium whitespace, and presentation-ready composition.
```

### 12. Email campaign visual sequence

```text
Create a polished email campaign visual sequence for [brand / offer].
Output should feel like a premium lifecycle marketing set with [3-5] frames:
- hero announcement
- product or feature highlight
- testimonial / proof card
- CTA banner

Keep the same art direction, palette, product styling, and typography hierarchy across all frames.
Design for marketing ops use: clear headline zones, CTA-safe whitespace, and modular composition.
```

### 13. Medical infographic with structured schema

```text
Create a comprehensive medical infographic about [topic].
Use a clean clinical white background and detailed 3D medical illustration style.
Organize the composition into clearly labeled sections:
- anatomy / mechanism
- symptoms
- diagnosis
- treatment
- prevention or key takeaways

Prefer structured labels, arrows, legends, and short callouts over long paragraphs.
Make the layout presentation-ready and readable on both slide and long-image formats.
```

### 14. 3x3 storyboard board

```text
Create a 3x3 storyboard board for [story / ad / explainer / video sequence].
Nine frames only, all in one image, with consistent subject identity and art direction.
Frame flow should read left-to-right, top-to-bottom.
Each frame should represent a distinct beat:
[beat 1] ... [beat 9]

Add subtle caption space or panel numbering if useful, but avoid dense text.
The board should be strong enough to reuse as a video keyframe plan.
```

### 15. Chinese calligraphy / typography sheet

```text
Create a typography-led image centered on the exact Chinese text:
"[paste exact text]"

Style direction: [clerical script / regular script / seal script / running script / poster typography].
Output should feel like a curated calligraphy specimen or cultural poster.
Control:
- legible Chinese glyph structure
- intentional ink texture or printing texture
- balanced spacing
- supporting layout kept secondary to the text
```

## Edit Prompt Frame

When using references, explicitly separate what to preserve from what to change:

```text
Use the provided image(s) as reference.
Keep unchanged:
- [subject identity]
- [composition / pose / product shape / logo placement]

Change:
- [style / environment / background / outfit / lighting / color palette]

Output:
- [poster / comic page / clean product image / magazine cover / storyboard frame]

Do not change:
- [specific immutable details]
```

## Negative Cues

Use these only when needed:

- no watermark
- no extra fingers
- no low-resolution blur
- no random background text
- no UI nonsense text outside requested regions
- avoid overdecorated layout
- keep whitespace for overlay text
- do not change facial identity
- do not alter product geometry

## Iteration Pattern

If first result is close but not usable:

1. Keep the successful structure.
2. Rewrite only the failing layer:
   - text clarity
   - composition
   - material realism
   - identity consistency
   - whitespace
3. Use edit mode with the best previous result as the new reference.

## Batch Prompt Pack Pattern

When the user asks for a deliverable with multiple images, first create a prompt pack instead of calling the API immediately.

```bash
python scripts/prompt_pack_builder.py \
  --scene ppt \
  --brief "为某个主题做一套方案 PPT 配图" \
  --style "高级、清晰、可交付" \
  --out ./outputs/topic-ppt-pack
```

Then inspect:

- `manifest.json`
- `package-plan.md`
- `prompts/*.txt`

Render after review:

```bash
python scripts/render_manifest.py \
  --manifest ./outputs/topic-ppt-pack/manifest.json
```

Use `--dry-run` to verify commands without calling the API.

### Supported scenes

| Scene | Output |
| --- | --- |
| `ppt` | cover, section opener, process visual, data story, scenario image, closing image |
| `infographic` | one vertical information-dense card |
| `comic` | character bible and first comic page |
| `ui` | product UI concept board |
| `poster` | commercial poster / banner key visual |
| `article` | article hero, inline visual, summary card |
| `game` | world key art and game UI status page |
