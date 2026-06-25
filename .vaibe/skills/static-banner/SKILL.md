---
name: static-banner
description: Create static ad banners and promotional images using AI image generation with proven scroll-stop techniques. Triggers: banner, баннер, креатив, ad creative, рекламный визуал, promotional image, ad visual.
license: MIT
---

# Purpose

Generate production-ready image prompts and images for static advertising banners using proven scroll-stop templates and AI image generators.

# When to use

- Creating static ad banners or ad creatives
- Generating image prompts for advertising visuals
- Creating promotional images for Telegram Ads, VK, Meta, Instagram, TikTok
- Building a batch of banner concepts for A/B testing

# Universal rule: break banner blindness

**Every banner MUST include at least one scroll-stopping mechanism.** Apply one or more:

1. **High Visual Contrast** — clashing colors, light on dark, hard edges, color blocking
2. **Pattern Disruption** — object out of context, surreal scale, glitch, handwritten scribbles
3. **Extreme Emotion** — exaggerated facial expression, dynamic body language, direct eye contact
4. **Visual Tension** — cropped elements, before/after, curiosity gap in text
5. **Unusual Lighting** — neon glow, duotone, infrared, harsh flash, monochrome + accent punch

In every final prompt, include: `Scroll-stop mechanism: [describe the specific technique used]`

If the user's brief is safe or neutral, proactively suggest a boldness upgrade.

# Procedure

## Step 1 — Template selection

Present 4 templates and help the user choose:

**Template 1: Character + Text**
Person/character photo with text overlay. Universal, works across niches.

**Template 2: Pinterest Infographic Collage**
Multi-tile visual with structured information. Looks like a saveable resource, not an ad.

**Template 3: Text on Surface**
Text placed on an interesting texture or object. The message is the hero.

**Template 4: Diagnostic/Calculator Preview**
Visual preview of a diagnostic tool leading to a quiz. Creates perception of expertise.

## Step 2 — Generation method

For each template, offer:
- **Option A: Full banner** — image + text together in one AI generation
- **Option B: Visual element only** — generate image, add text in editor (more control)

## Step 3 — Interactive Q&A

Run the appropriate mega-prompt based on selected template. Ask questions **one at a time**. After each answer, provide relevant examples and suggestions.

### Template 1 questions (Character + Text, full banner)
1. Reference image for layout inspiration? (yes/no)
2. Product or offer? (1-2 sentences)
3. Target persona? (age + gender + main need)
4. Key promise or result?
5. Visual style? (realistic / clean fashion / dark dramatic / illustrated / editorial)
6. Format + CTA? (e.g. 9x16 + "Start today")
7. Disclaimer needed? (yes/no)
8. Language for ad text?

### Template 2 questions (Pinterest Infographic)
1. Product + target segment
2. What to show in tiles? Focus areas?
3. Layout: tile count (default: 5), symmetric/asymmetric
4. Style: photographic / flat icons / minimalist / cinematic
5. Color vibe + emotion + tone
6. Headline style + CTA + icon style
7. Language

### Template 3 questions (Text on Surface)
1. Product or service?
2. Target audience (age, pains, motivations)?
3. Message text (or generate 5 variations)
4. Surface + setting (choose 3 from categories: clean, lifestyle, bold)
5. Visual style + mood
6. Text style + writing material
7. Aspect ratio

### Template 4 questions (Diagnostic Preview)
1. Niche/topic
2. Main problem the diagnostic solves
3. Parameters (3-7 items)
4. CTA text
5. Visual style
6. Design constraints
7. Aspect ratio

## Step 4 — Generate prompt(s)

Produce clean, ready-to-paste image generation prompts. Each prompt must include:
- Scene/visual description with scroll-stop mechanism
- Brand text and CTA button text
- Explicit `Scroll-stop mechanism:` line
- `No watermarks, no AI labels.`

## Step 5 — Generate images (if API available)

If Higgsfield API keys are configured in `.env` (copy from `.vaibe/skills/static-banner/scripts/static-banner-kit/.env.example`):

- Use `nano-banana-pro` for all banners with text (best text rendering)
- Use `higgsfield-ai/soul/standard` only for portraits without text
- Run via `node .vaibe/skills/static-banner/scripts/static-banner-kit/pipeline/generate-banners.mjs`

# Batch mode

When the user asks for a "pack" or "batch":

1. Gather: product, target audience, CTA text, brand text, number of banners
2. Generate N concepts using proven archetypes (see below)
3. Present concepts for approval
4. Write a generation script based on `.vaibe/skills/static-banner/scripts/static-banner-kit/pipeline/generate-banners.mjs`
5. Run the script: `node .vaibe/skills/static-banner/scripts/static-banner-kit/generate-my-pack.mjs`
6. Report results

# Proven scroll-stop archetypes

| Archetype | Why it works |
|---|---|
| Neon object in void | Extreme light-dark contrast |
| Stamp/mark on face | Confrontational + eye contact |
| Object on fire | Primal attention trigger |
| LED/display board | Familiar format, bold on black |
| Chalk/handwritten on black | Maximum contrast + raw texture |
| Flash celebration | Extreme emotion + UGC energy |
| Split face duotone | Visual tension + before/after |
| Giant UI element | Recognizable pattern + aspiration |
| Luxury flat-lay | Bold color accent on neutral |
| Surreal metaphor | Impossible scene = pattern disruption |
| VIP exclusivity | Exclusivity trigger |
| Breaking through | Action + empowerment |
| Golden ticket | Magical + aspirational |
| Neon sign in dark | Cyberpunk mood + reflections |
| Ripping paper | Visceral defiance |
| Door with light | Mystery + chiaroscuro |
| Megaphone/pop-art | Pop-art energy + red on black |

# Output format

- Text prompts for image generation (ready to paste)
- Generated images in `output/{pack-name}/` (if API used)
- Each banner in 2 formats: 3:4 (feed) + 9:16 (stories)

# Quality bar

- [ ] Every prompt has an explicit scroll-stop mechanism
- [ ] Brand text and CTA are present in prompts
- [ ] Dark/high-contrast backgrounds preferred for mobile feeds
- [ ] Single bold focal element (not complex compositions)
- [ ] "No watermarks, no AI labels" in every prompt
- [ ] `nano-banana-pro` used for text-heavy banners

# Anti-patterns (underperforming visuals — avoid)

- Clean studio portraits with soft lighting
- Object flat-lays with neutral tones
- Screenshot mockups (LinkedIn posts, iMessage threads)
- Before/after splits with desaturated tones
- UI dashboard screenshots
- Sticky notes / written lists

# AI image generators reference

| Model | Best for | Text quality |
|---|---|---|
| `nano-banana-pro` | **Default for banners with text** | Excellent |
| `nano-banana` | Fast generation | Good |
| `flux-2` | Complex compositions | Good |
| `reve` | UGC feel | Medium |
| `soul/standard` | Portraits without text | Poor |

Supported aspect ratios: 9:16, 16:9, 4:3, 3:4, 1:1, 2:3, 3:2 (note: 4:5 not supported, use 3:4).

# Related knowledge

- `.vaibe/skills/landing-page-design/references/landing-page-patterns.md` — visual style consistency between banners and landing page
- `.vaibe/skills/sales-methodologies/SKILL.md` — Challenger framework for insight-led banner messaging
