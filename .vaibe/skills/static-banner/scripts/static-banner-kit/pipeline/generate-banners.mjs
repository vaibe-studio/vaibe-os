#!/usr/bin/env node
// ============================================================
// Static Banner Generator — Template Script
// ============================================================
// Usage: node pipeline/generate-banners.mjs
//
// 1. Edit the BANNERS array below with your concepts
// 2. Set PACK_NAME to your desired output folder name
// 3. Run the script — it generates 2 formats per banner:
//    - 3:4 (Meta/IG feed)
//    - 9:16 (Stories/Reels/TikTok)
//
// Prerequisites:
//   - Node.js 18+
//   - .env file with HF_KEY_ID and HF_KEY_SECRET
// ============================================================

import { mkdirSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { generateImage } from "./hf-api.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── CONFIG ──────────────────────────────────────────────────
const PACK_NAME = "my-banners"; // Change this for each new pack
const OUTPUT_DIR = join(__dirname, "..", "output", PACK_NAME);

// ── BANNERS ─────────────────────────────────────────────────
// Each banner needs:
//   id:     filename-friendly slug
//   prompt: full image generation prompt
//
// Prompt rules:
//   - Include at least 1 scroll-stop mechanism (neon, fire, flash, surreal, etc.)
//   - Include brand text and CTA button in the prompt
//   - Use dark/black backgrounds for strongest feed contrast
//   - End with "No watermarks, no AI labels."
//
// See SKILL.md → "Proven Scroll-Stop Concepts" for 20 validated archetypes.

const BANNERS = [
  {
    id: "01-example-neon",
    prompt: `YOUR PROMPT HERE. Bold white text at top: "YOUR BRAND". At the bottom: a bright teal rounded button with white bold text "Your CTA". No watermarks, no AI labels.`,
  },
  // Add more banners here...
];

// ── FORMATS ─────────────────────────────────────────────────
const FORMATS = [
  { suffix: "feed", aspect_ratio: "3:4" },
  { suffix: "stories", aspect_ratio: "9:16" },
];

// ── MAIN ────────────────────────────────────────────────────
async function main() {
  if (!existsSync(OUTPUT_DIR)) {
    mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const total = BANNERS.length * FORMATS.length;
  console.log(`\n=== Banner Generation: ${PACK_NAME} ===`);
  console.log(`Output: ${OUTPUT_DIR}`);
  console.log(`Banners: ${BANNERS.length} x ${FORMATS.length} formats = ${total} images\n`);

  const results = [];

  for (const banner of BANNERS) {
    for (const format of FORMATS) {
      const filename = `${banner.id}-${format.suffix}.png`;
      const outputPath = join(OUTPUT_DIR, filename);
      console.log(`\n--- ${filename} ---`);

      try {
        const result = await generateImage(banner.prompt, outputPath, {
          aspect_ratio: format.aspect_ratio,
          model: "nano-banana-pro",
          resolution: "2k",
        });
        results.push({ id: filename, status: "ok", path: result.localPath });
        console.log(`  OK: ${outputPath}`);
      } catch (e) {
        console.error(`  FAIL: ${e.message}`);
        results.push({ id: filename, status: "fail", error: e.message });
      }
    }
  }

  console.log(`\n=== Results ===`);
  for (const r of results) {
    console.log(`  ${r.status === "ok" ? "✓" : "✗"} ${r.id} ${r.status === "fail" ? `— ${r.error}` : ""}`);
  }

  const ok = results.filter((r) => r.status === "ok").length;
  console.log(`\nDone: ${ok}/${total} generated`);
}

main().catch((e) => {
  console.error("Fatal:", e);
  process.exit(1);
});
