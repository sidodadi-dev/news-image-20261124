// Entry point for the news-image-20261124 entry (Node 22, standard
// library only). The poster is drawn by poster.py and shipped in this
// repository as entry.png; this program copies it to the output
// directory the grader provides, so both runs write identical bytes.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), dest);
console.log('wrote', dest);
