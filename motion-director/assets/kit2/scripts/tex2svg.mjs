// TeX → SVG com MathJax (Apache-2.0), para Manim sem LaTeX instalado: node scripts/tex2svg.mjs <entrada.json> <pasta>
// entrada: {"nome": "\\TeX com \\color{#hex}{...}", ...}. Caminhos embutidos (fontCache none), cor padrão substituída.
import fs from 'node:fs';
import path from 'node:path';
import {mathjax} from 'mathjax-full/js/mathjax.js';
import {TeX} from 'mathjax-full/js/input/tex.js';
import {SVG} from 'mathjax-full/js/output/svg.js';
import {liteAdaptor} from 'mathjax-full/js/adaptors/liteAdaptor.js';
import {RegisterHTMLHandler} from 'mathjax-full/js/handlers/html.js';
import {AllPackages} from 'mathjax-full/js/input/tex/AllPackages.js';
const [, , inp, out, color = '#F3F4F7'] = process.argv;
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const doc = mathjax.document('', {InputJax: new TeX({packages: AllPackages}), OutputJax: new SVG({fontCache: 'none'})});
fs.mkdirSync(out, {recursive: true});
for (const [name, tex] of Object.entries(JSON.parse(fs.readFileSync(inp, 'utf8')))) {
	const node = doc.convert(tex, {display: true});
	let svg = adaptor.innerHTML(node).replace(/currentColor/g, color);
	fs.writeFileSync(path.join(out, `${name}.svg`), svg);
}
console.log('ok', out);
