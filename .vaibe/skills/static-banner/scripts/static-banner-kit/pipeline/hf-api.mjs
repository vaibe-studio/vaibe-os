// Higgsfield Platform API — image generation client
// Requires: HF_KEY_ID and HF_KEY_SECRET in .env file
import { writeFileSync, readFileSync, existsSync, statSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load .env from project root
(function loadEnv() {
  const envPath = join(__dirname, "..", ".env");
  try {
    const lines = readFileSync(envPath, "utf-8").split("\n");
    for (const line of lines) {
      const match = line.match(/^([^=]+)=(.*)$/);
      if (match) process.env[match[1].trim()] = match[2].trim();
    }
  } catch {}
})();

const HF_KEY_ID = process.env.HF_KEY_ID;
const HF_KEY_SECRET = process.env.HF_KEY_SECRET;
const BASE_URL = "https://platform.higgsfield.ai";
const POLL_INTERVAL = 5000;
const MAX_POLLS = 120;
const MAX_RETRIES = 3;
const RETRY_DELAY = 15000;

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

export function isFileReady(path, minSize = 1000) {
  try {
    return existsSync(path) && statSync(path).size > minSize;
  } catch {
    return false;
  }
}

export async function hfRequest(endpoint, body, retries = MAX_RETRIES) {
  const url = `${BASE_URL}/${endpoint}`;
  console.log(`    POST ${url}`);

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const res = await fetch(url, {
        method: "POST",
        headers: {
          Authorization: `Key ${HF_KEY_ID}:${HF_KEY_SECRET}`,
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(body),
      });

      if (res.status === 502 || res.status === 503 || res.status === 429) {
        const wait = RETRY_DELAY * attempt;
        console.log(`    [${attempt}/${retries}] HTTP ${res.status}, retry in ${wait / 1000}s...`);
        await sleep(wait);
        continue;
      }

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Higgsfield ${res.status}: ${text.slice(0, 200)}`);
      }

      return res.json();
    } catch (e) {
      if (attempt < retries && (e.message.includes("502") || e.message.includes("fetch failed") || e.message.includes("ECONNRESET"))) {
        const wait = RETRY_DELAY * attempt;
        console.log(`    [${attempt}/${retries}] ${e.message.slice(0, 60)}, retry in ${wait / 1000}s...`);
        await sleep(wait);
        continue;
      }
      throw e;
    }
  }
  throw new Error(`All ${retries} retries exhausted`);
}

export async function pollStatus(requestId) {
  const url = `${BASE_URL}/requests/${requestId}/status`;

  for (let attempt = 0; attempt < MAX_POLLS; attempt++) {
    try {
      const res = await fetch(url, {
        headers: {
          Authorization: `Key ${HF_KEY_ID}:${HF_KEY_SECRET}`,
          Accept: "application/json",
        },
      });

      if (res.status === 502 || res.status === 503) {
        console.log(`    [${attempt + 1}/${MAX_POLLS}] server unavailable, waiting...`);
        await sleep(RETRY_DELAY);
        continue;
      }

      if (!res.ok) throw new Error(`Poll ${res.status}: ${(await res.text()).slice(0, 200)}`);

      const data = await res.json();
      const status = data.status;

      if (status === "completed") return data;
      if (status === "failed") throw new Error(`Generation failed: ${JSON.stringify(data).slice(0, 200)}`);
      if (status === "nsfw") throw new Error("Content blocked by moderation (NSFW)");

      process.stdout.write(`    [${attempt + 1}/${MAX_POLLS}] ${status}...\n`);
    } catch (e) {
      if (e.message.includes("fetch failed") || e.message.includes("ECONNRESET")) {
        console.log(`    [${attempt + 1}/${MAX_POLLS}] network error — retrying...`);
        await sleep(RETRY_DELAY);
        continue;
      }
      throw e;
    }
    await sleep(POLL_INTERVAL);
  }

  throw new Error(`Timeout: ${(MAX_POLLS * POLL_INTERVAL) / 1000}s`);
}

export async function downloadFile(url, outputPath) {
  for (let i = 0; i < 3; i++) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Download ${res.status}`);
      const buffer = Buffer.from(await res.arrayBuffer());
      writeFileSync(outputPath, buffer);
      return outputPath;
    } catch (e) {
      if (i < 2) {
        console.log(`    Download retry ${i + 1}...`);
        await sleep(5000);
        continue;
      }
      throw e;
    }
  }
}

export async function generateImage(prompt, outputPath, options = {}) {
  if (isFileReady(outputPath)) {
    console.log(`  Already exists: ${outputPath} — skipping`);
    return { requestId: "cached", url: null, localPath: outputPath };
  }

  const model = options.model || "nano-banana-pro";
  const body = {
    prompt,
    aspect_ratio: options.aspect_ratio || "3:4",
    resolution: options.resolution || "2k",
  };

  console.log(`  Generating: ${model}`);
  console.log(`  Prompt: ${prompt.slice(0, 80)}...`);

  const submitResult = await hfRequest(model, body);
  const requestId = submitResult.request_id;
  console.log(`  Request ID: ${requestId}`);

  const result = await pollStatus(requestId);
  console.log(`  Status: completed`);

  const imageUrl = result.images?.[0]?.url;
  if (!imageUrl) throw new Error("No image URL in response");

  await downloadFile(imageUrl, outputPath);
  console.log(`  Saved: ${outputPath}\n`);

  return { requestId, url: imageUrl, localPath: outputPath };
}
