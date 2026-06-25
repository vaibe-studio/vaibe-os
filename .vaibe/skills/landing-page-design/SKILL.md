---
name: landing-page-design
description: Create marketing landing pages through iterative UX wireframe, visual concept selection, and final HTML build. Triggers: landing, лендинг, одностраничник, one-pager, marketing page, web page, landing page.
license: MIT
---

# Purpose

Create high-converting single-page marketing websites through an iterative, user-guided process: structure first, visual style second, code last.

# When to use

- Building a marketing landing page for a product, service, or event
- Creating a one-pager website for sales outreach
- Redesigning an existing landing page with new messaging

# Procedure

The process has **three phases with mandatory STOP points**. Never skip ahead — the user is sensitive to visual decisions and must approve each phase before the next begins.

## Phase A — Meaning

### Step 1 — Messaging brief

Gather or extract from existing project materials:

- **Target audience** — who exactly sees this page (role, company size, pain)
- **One core value** — the single most important thing the visitor should understand
- **Primary CTA** — one action the visitor should take (book a call, sign up, download)
- **Proof points** — 3-5 reasons to trust (experience, clients, methodology, numbers)
- **Tone of voice** — anti-hype / bold / warm / technical / etc.

If a messaging document exists in the project, use it as the source of truth.

### Step 2 — UX wireframe (text-based)

Create a Markdown wireframe showing the page structure. For each section specify:

- Section name and purpose
- Content hierarchy: what is H1, H2, body, CTA, card
- Approximate content (headlines, bullet points, not final copy)
- Layout hints: grid columns, card count, alignment

Use the canonical B2B structure from `.vaibe/skills/landing-page-design/references/landing-page-patterns.md` as default:

```
Nav → Hero → Problem → Process/Solution → Services/Pricing →
Results/Social proof → FAQ → Final CTA → Footer
```

Present the wireframe as a numbered Markdown document the user can scan in 30 seconds.

### STOP 1 — User approves structure

Show the wireframe to the user. Ask:
- Is the section order right?
- Any sections to add, remove, or reorder?
- Is the content hierarchy clear?

**Do not proceed until the user confirms.**

## Phase B — Visual style

### Step 3 — Generate 2-3 visual concepts

For each concept, create a **mini-HTML file** (hero block + one content section only) demonstrating:

- Color palette (CSS custom properties: background, text, accent, card, border)
- Font pairing from the library in `.vaibe/skills/landing-page-design/references/landing-page-patterns.md`
- Mood: dark premium / light clean / bold accent / warm minimal / etc.
- Component style: card borders, button shape, shadow intensity, spacing rhythm

Each mini-HTML should be a self-contained file the user can open in a browser.

Name files descriptively: `concept-a-dark-premium.html`, `concept-b-light-clean.html`.

**Optional:** if the `static-banner` skill and Higgsfield API are available, generate hero images to replace placeholders — the user sees real visuals, not grey boxes.

### STOP 2 — User chooses a visual direction

Present all concepts. Ask:
- Which concept feels right? (A / B / C / mix)
- Any color or font adjustments?
- Any elements from one concept to merge into another?

**Do not proceed until the user confirms the visual direction.**

## Phase C — Build

### Step 4 — Content

Fill the approved wireframe with final copy:

- Write in the user's language (Russian by default), not meta-descriptions
- Use concrete numbers, not vague claims
- Every headline should be scannable in 3 seconds
- CTA button text should be specific ("Записаться на диагностику", not "Узнать больше")
- Include social proof if available (clients, metrics, testimonials)

### Step 5 — HTML build

Build a single self-contained HTML file using the approved visual style:

- Semantic HTML5 (`<nav>`, `<main>`, `<section>`, `<footer>`)
- All CSS in `<style>` (no external files)
- CSS custom properties for all colors, fonts, radii, shadows
- Google Fonts via CDN with `display=swap` and variable font weights
- Responsive: mobile-first with breakpoints at 600px, 900px
- Burger menu for mobile navigation
- Smooth scroll for anchor links
- OG meta tags (title, description, image, type)
- Structured data placeholder (LocalBusiness / ProfessionalService)

Use the starter template from `.vaibe/skills/landing-page-design/assets/landing-starter-template.html` if available.

### Step 6 — Quality checklist

- [ ] Hero CTA visible without scrolling on mobile
- [ ] All sections render correctly at 375px, 768px, 1440px
- [ ] Font loading: no FOUT/FOIT (display=swap + preconnect)
- [ ] OG meta tags present and correct
- [ ] No placeholder text remaining ("Lorem ipsum", "TODO", "TBD")
- [ ] All links are anchors or real URLs (no broken hrefs)
- [ ] Color contrast ratio ≥ 4.5:1 for body text (WCAG AA)
- [ ] Page weight < 200KB (no images beyond CDN fonts)
- [ ] Analytics placeholder present (comment block for GTM/Metrica)
- [ ] Favicon and apple-touch-icon referenced
- [ ] Consistent spacing rhythm across sections
- [ ] Single primary CTA style used throughout

### STOP 3 — User reviews in browser

The user opens the HTML file in a browser and checks:
- Desktop and mobile views
- Text accuracy
- Visual polish
- CTA clarity

**Iterate on feedback until the user approves.**

# Output format

- Approved wireframe (Markdown)
- 2-3 visual concept files (mini-HTML)
- Final landing page (`index.html`, single file)
- All files placed in `results/v{N}/` of the corresponding task

# Quality bar

- [ ] All Step 6 checklist items pass
- [ ] User explicitly approved at all 3 STOP points
- [ ] No meta-commentary in visible content
- [ ] Mobile experience is complete (not a degraded desktop)
- [ ] Page loads and renders without JavaScript (CSS-only layout)

# Anti-patterns

- Generating final HTML without wireframe and style approval
- Meta-comments as content ("Here goes the headline about...")
- Encyclopedic hero with 5+ lines of text
- Missing or generic CTA ("Learn more" instead of specific action)
- Inconsistency with approved messaging document
- Single visual concept without offering choice
- Ignoring mobile until the final review
- Placeholder images with no plan for replacement
- Mixing multiple accent colors without system

# Related knowledge

- `.vaibe/skills/landing-page-design/references/landing-page-patterns.md` — page structure, font library with Cyrillic pairs, CSS conventions, SEO checklist, competitor references
- `.vaibe/skills/strategy-frameworks/SKILL.md` — Value Proposition Canvas, Lean Canvas for structuring the messaging brief
- `.vaibe/skills/sales-methodologies/SKILL.md` — Challenger "Teach" framework for insight-led page structure
