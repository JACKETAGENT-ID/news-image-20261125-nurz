import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The front page for Wednesday 25 November 2026 lives beside this script.
// Resolve it from the script's own location: the grader runs
// `node /bot/main.ts` from another working directory, so process.cwd()
// must never be used to find the image.
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");

const buf = readFileSync(src);
const size = statSync(src).size;

// PNG signature: 89 50 4E 47 0D 0A 1A 0A
const sig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!buf.subarray(0, 8).equals(sig)) {
  throw new Error("entry.png is not a PNG file");
}
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}
// IHDR: width at bytes 16-19, height at bytes 20-23, big-endian.
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024 limit`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
// Confirm the copy landed whole: same byte count as the source.
if (statSync(dest).size !== size) {
  throw new Error("copied entry.png does not match the source size");
}
console.log(`entry.png: ${width}x${height}, ${size} bytes -> ${outDir}`);
