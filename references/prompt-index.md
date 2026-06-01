# Prompt Index

This file is the fast human-readable index for reusable `gpt-image-2` cases. For machine-friendly fields, use [case-library.json](case-library.json).

## `information_dense`

- `x-infographic-endangered-animal`
  Prompt type: `pattern`
  Prompt: `先研究对象,再分成 habitat / diet / traits / protection 四到六个结构化分区,用中文标题、callout 和图示组合成长图。`
  Local refs: `assets/cases/x-infographic-endangered-animal`

- `x-medical-infographic-json`
  Prompt type: `partial`
  Prompt: `{ "type": "comprehensive medical infographic", "style": "highly detailed 3D medical illustration, clinical white background, clean typography", "sections": ["anatomy", "symptoms", "diagnosis", "treatment", "prevention"] }`
  Local refs: `assets/cases/x-medical-infographic-json`

## `narrative`

- `x-chinese-modern-comic`
  Prompt type: `pattern`
  Prompt: `明确页数、每页 panel 数、人物设定、中文对白密度和故事主线，再要求角色跨页一致。`
  Local refs: `assets/cases/x-chinese-modern-comic`

- `gh-korean-idol-3x3-grid`
  Prompt type: `exact`
  Prompt: `9:16 vertical, Korean idol portrait photoshoot, 3x3 grid (nine frames), same person in all images, consistent facial features and styling...`
  Local refs: none

- `gh-epic-silhouette-world-poster`
  Prompt type: `exact`
  Prompt: `A collectible epic poster featuring a character's side-profile silhouette. Inside the silhouette grows a complete world and iconic scenes...`
  Local refs: none

## `commercial`

- `x-3d-concept-store`
  Prompt type: `pattern`
  Prompt: `品牌名 + 标志性产品外观 + 3D chibi miniature concept store + premium toy-like materials。`
  Local refs: `assets/cases/x-3d-concept-store`

- `x-email-campaign-fenty`
  Prompt type: `exact`
  Prompt: `Create a polished email sequence template for fenty beauty`
  Local refs: `assets/cases/x-email-campaign-fenty`

- `x-sports-poster-stephen-curry`
  Prompt type: `exact`
  Prompt: `Haz un póster, un diseño de Stephen Curry fichando por los Dallas Mavericks. Nivel de diseño avanzado, 4:5, wallpaper de móvil.`
  Local refs: `assets/cases/x-sports-poster-stephen-curry`

- `gh-green-tea-ad-poster`
  Prompt type: `exact`
  Prompt: `JSON-like retail poster scaffold with headline, feature labels, price_badge, promo_banner, footer CTA.`
  Local refs: none

## `presentation`

- `x-brand-guideline-from-reference-restaurant`
  Prompt type: `reference_first`
  Prompt: `Use the provided restaurant reference image as the brand seed. Build a mini brand guideline board including hero treatment, color palette, type direction, signage, packaging, and social thumbnail outputs while preserving the original mood.`
  Local refs: `assets/cases/x-brand-guideline-from-reference-restaurant`

## `immersive`

- `x-worldbuilding-set-desert-solar`
  Prompt type: `exact`
  Prompt: `Create a complete visual worldbuilding set for a futuristic desert civilization powered by solar technology, multiple images including architecture, characters, clothing, vehicles, and maps, cohesive design language, cinematic realism, ultra detailed.`
  Local refs: `assets/cases/x-worldbuilding-set-desert-solar`

- `x-panorama-equirectangular-flow`
  Prompt type: `exact_step`
  Prompt: `Step 1: generate a strong base scene. Step 2: Convert this scene into a 360 equirectangular image`
  Local refs: `assets/cases/x-panorama-equirectangular-flow`

## `editing`

- `x-scientist-comic`
  Prompt type: `pattern`
  Prompt: `给人物参考图,指定全彩中文漫画、角色一致性、主线情节和每格对白控制。`
  Local refs: `assets/cases/x-scientist-comic`

## `design_mockup`

- `x-clerical-script-calligraphy`
  Prompt type: `exact_topic`
  Prompt: `GPT image 2 隶书字体书写曹操的《龟虽寿》`
  Local refs: `assets/cases/x-clerical-script-calligraphy`

- `gh-handwritten-notebook-photo`
  Prompt type: `exact`
  Prompt: `Amateur photo of an open notebook lying flat, filled with handwritten notes in black ballpoint pen... Shot from slightly above, natural daylight from a window, no flash.`
  Local refs: none

- `gh-rice-grain-micro-typography`
  Prompt type: `exact`
  Prompt: `A massive pile of rice, and on one single grain of rice there is tiny text that reads "wOw"`
  Local refs: `assets/cases/gh-rice-grain-micro-typography`

- `gh-taobao-product-detail-page`
  Prompt type: `exact`
  Prompt: `A Taobao product detail page for [product], displaying three-view drawings, price, details, functions, and usage scenarios.`
  Local refs: none
