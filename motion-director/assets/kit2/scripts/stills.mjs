// Renderiza stills de vários frames com um único bundle. Uso: node scripts/stills.mjs <saida> <frame> [frame...]
import path from 'node:path';
import fs from 'node:fs';
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
const [, , out, ...frames] = process.argv;
fs.mkdirSync(out, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const composition = await selectComposition({serveUrl, id: 'Biblioteca'});
for (const fr of frames) {
	await renderStill({serveUrl, composition, frame: Number(fr), output: path.join(out, `f${fr}.png`), scale: 0.5, logLevel: 'error'});
}
console.log('ok', frames.length);
