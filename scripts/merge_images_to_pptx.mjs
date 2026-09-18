#!/usr/bin/env node
// Image-only export. Embedded page images do not become editable text.
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const [imageDir, output, fit = 'contain'] = process.argv.slice(2);
if (!imageDir || !output || !['contain', 'cover'].includes(fit)) {
  throw new Error('Usage: merge_images_to_pptx.mjs IMAGE_DIR OUTPUT.pptx [contain|cover]');
}
const runtimeModules = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
if (!runtimeModules || !path.isAbsolute(runtimeModules)) {
  throw new Error('Managed CODEX_PRIMARY_RUNTIME_NODE_MODULES is required.');
}
const requireRuntime = createRequire(path.join(runtimeModules, 'artifact-loader.cjs'));
const { Presentation, PresentationFile } = await import(pathToFileURL(requireRuntime.resolve('@oai/artifact-tool')).href);
const extensions = new Set(['.png', '.jpg', '.jpeg', '.webp']);
const entries = await fs.readdir(imageDir, { withFileTypes: true });
const files = entries.filter(e => e.isFile() && extensions.has(path.extname(e.name).toLowerCase())).map(e => e.name)
  .sort((a, b) => a.localeCompare(b, 'en', { numeric: true, sensitivity: 'base' }));
if (!files.length) throw new Error(`No supported images found in ${imageDir}`);
const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });
for (const file of files) {
  const slide = presentation.slides.add();
  slide.background.fill = '#FFFFFF';
  const extension = path.extname(file).toLowerCase();
  const contentType = extension === '.jpg' || extension === '.jpeg' ? 'image/jpeg' : `image/${extension.slice(1)}`;
  const blob = new Uint8Array(await fs.readFile(path.join(imageDir, file)));
  slide.images.add({ blob, contentType, alt: file, fit,
    position: { left: 0, top: 0, width: 1280, height: 720 } });
}
await fs.mkdir(path.dirname(output), { recursive: true });
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(output);
console.log(`Saved ${files.length} image-only slides to ${output}. Image text is not editable.`);
