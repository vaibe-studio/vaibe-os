# Landing Page Patterns

Reference material for the `landing-page-design` skill. Non-actionable — consult during execution.

---

## 1. Page structure — canonical B2B SaaS / consulting

```
Nav (fixed)
  → Logo + anchor links + CTA button

Hero
  → Badge/label (optional, e.g. "AI Design Sprint")
  → H1: one strong claim (≤12 words)
  → Sub-headline: expand the claim (1-2 sentences)
  → 2 CTAs: primary (action) + secondary (learn more)
  → Trust strip (logos / "120+ clients" / badge)

Problem (3-4 cards)
  → Section label + H2
  → Pain cards: icon + H3 + short description
  → Goal: visitor thinks "yes, that's me"

Process / How it works (3-5 steps)
  → Numbered steps with connectors
  → Each step: number + H3 + description
  → Visual: timeline, cards, or columns

Services / Pricing (2-4 packages)
  → Package cards: name + price + what's included + CTA
  → Highlight recommended package
  → "Starting from" pricing is OK for consulting

Results / Social proof
  → Metric cards: big number + label + context
  → Before/after comparison (optional)
  → Testimonials with name + role (when available)
  → Case study links (when available)

FAQ (5-7 questions)
  → Accordion or static list
  → Address: cost, timeline, "will AI replace my staff?", process, results guarantee
  → Reduces objections, builds trust

Final CTA
  → Repeat primary CTA with emotional reinforcement
  → Contact options: Telegram + email + Calendly
  → Box with accent border or gradient top line

Footer
  → Legal entity, contacts, social links
  → Copyright year
```

### Conversion patterns

- **Sticky CTA**: fixed button on mobile, visible after scrolling past hero
- **Contrast buttons**: primary = filled accent, secondary = ghost/outline
- **Risk reversal**: "Free diagnostic", "No obligation", "Cancel anytime"
- **Micro-copy**: button sub-text ("30-minute call, no commitment")
- **Social proof near CTA**: "120+ businesses trust us" near the action button
- **FAQ as objection handler**: preempt "too expensive", "how long", "what if it doesn't work"

---

## 2. Typography — font library with Cyrillic support

All fonts below are Google Fonts (free, commercial use allowed). Use variable font format when available for smaller payload.

### Ready-made pairings

| Pair name | Heading | Body | Character | When to use |
|---|---|---|---|---|
| **Tech Modern** | Inter (700-900) | Inter (400-500) | Neutral, technical, UI | SaaS product, dashboard, neutral brand |
| **Warm Geometric** | Manrope (700-800) | Inter (400-500) | Friendly, modern | Startup, B2B with human tone |
| **Premium Clean** | Plus Jakarta Sans (700-800) | Plus Jakarta Sans (400-500) | Soft, premium | Boutique studio, coaching, consulting |
| **Bold Statement** | Montserrat (700-900) | Source Sans 3 (400-500) | Bold, confident | Agency, active selling |
| **Classic Authority** | Playfair Display (700-900) | PT Sans (400) | Serif, authoritative | Enterprise, legal, finance |
| **Soft Rounded** | Nunito (700-800) | Open Sans (400-500) | Rounded, approachable | Education, coaching, workshops |
| **Editorial** | Merriweather (700-900) | Roboto (400) | Book-like, expert | Content projects, blogs, media |
| **Minimal Geo** | Raleway (600-700) | Noto Sans (400-500) | Minimalist, light | Technology minimalism |

### Default recommendation for vAIbe

**Manrope (heading) + Inter (body)** — modern, friendly, excellent Cyrillic, variable font (small payload ~40KB total).

### Implementation rules

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
```

```css
:root {
  --font-heading: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

h1, h2, h3 { font-family: var(--font-heading); }
body { font-family: var(--font-body); }
```

### Sizing scale

| Element | Size | Weight | Line-height |
|---|---|---|---|
| H1 (hero) | clamp(2.4rem, 5vw, 3.8rem) | 800-900 | 1.08-1.12 |
| H2 (section) | clamp(1.8rem, 4vw, 2.6rem) | 700-800 | 1.12-1.2 |
| H3 (card) | 1.1rem-1.25rem | 600-700 | 1.3 |
| Body | 1rem-1.1rem | 400 | 1.6-1.7 |
| Small / label | 0.78rem-0.85rem | 500-600 | 1.4 |
| Button | 0.88rem-0.95rem | 600-700 | 1 |

---

## 3. CSS conventions

### Custom properties template

```css
:root {
  /* Colors */
  --bg: #ffffff;
  --bg-elevated: #f8f8fa;
  --bg-card: #ffffff;
  --surface: #f0f0f5;
  --text: #1a1a2e;
  --text-heading: #0d0d1a;
  --text-muted: #6b6b80;
  --border: rgba(0,0,0,0.08);
  --accent: #2563eb;
  --accent-hover: #1d4ed8;
  --accent-soft: rgba(37,99,235,0.08);

  /* Typography */
  --font-heading: 'Manrope', sans-serif;
  --font-body: 'Inter', sans-serif;

  /* Spacing & Shape */
  --radius: 16px;
  --radius-sm: 10px;
  --radius-xs: 6px;
  --max-w: 1120px;
  --shadow-card: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
}
```

### Responsive breakpoints (mobile-first)

```css
/* Base: mobile (< 600px) */
/* Tablet */
@media (min-width: 600px) { ... }
/* Desktop */
@media (min-width: 900px) { ... }
/* Wide */
@media (min-width: 1200px) { ... }
```

### Layout pattern

```css
.wrap {
  width: min(var(--max-w), calc(100% - 48px));
  margin: 0 auto;
}
.section { padding: 80px 0; }

@media (max-width: 600px) {
  .wrap { width: calc(100% - 32px); }
  .section { padding: 56px 0; }
}
```

---

## 4. SEO minimum

### Required meta tags

```html
<title>Brand — One-line value proposition</title>
<meta name="description" content="2-sentence description with primary keyword">
<meta property="og:title" content="Same as title or shorter">
<meta property="og:description" content="Same as meta description">
<meta property="og:type" content="website">
<meta property="og:image" content="https://...og-image-1200x630.png">
<meta property="og:url" content="https://...canonical-url">
<link rel="canonical" href="https://...canonical-url">
```

### Structured data (JSON-LD)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Brand Name",
  "description": "...",
  "url": "https://...",
  "telephone": "+7...",
  "address": { "@type": "PostalAddress", "addressLocality": "..." }
}
</script>
```

### Performance

- Page weight target: < 200KB (excluding external font CDN)
- No render-blocking JS (defer or end-of-body)
- `<link rel="preconnect">` for Google Fonts
- Images: use CSS gradients / SVG icons instead of raster where possible

---

## 5. Competitor references

Analyzed in March 2026 for AI consulting / automation / Design Sprint market:

| Company | Key pattern | URL |
|---|---|---|
| **AI Sapiens** | Anti-hype tone ("AI is impressive. We make it impactful"), approach-first structure, form CTA | aisapiens.studio |
| **Dootrix** | Process visualization (Day 1-5), "3 months in 5 days", brochure download as lead magnet | dootrix.com |
| **Poplab** | Productized sprints with fixed prices and timelines, metric-driven | poplab.io |
| **4GIC** | Catalog of 20+ solutions, 3-tier pricing (120K-600K+), FAQ block, Telegram AI bot | 4gic.com |
| **Opus Digital** | Case studies with numbers (+50% conversion, +340% traffic), FAQ, price transparency | opusdigital.ru |
| **Parallel** | Portfolio-first, fractional partnership model | parallelhq.com |

### Common winning elements

1. One strong claim in hero (not "we do AI" but a specific benefit)
2. Process as visual anchor (3-5 numbered steps)
3. Productized packages (fixed price + timeline + deliverables)
4. Case studies with before/after metrics
5. Free entry point (diagnostic / discovery call / AI bot)
6. Anti-hype tone ("practical results", not "AI revolution")
7. FAQ as trust-building block
