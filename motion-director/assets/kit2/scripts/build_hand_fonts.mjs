// Converte fontes SVG de traço único (EMS/Hershey, OFL) em polilinhas JSON + acentos compostos.
import fs from 'node:fs';
const FONTS = {felix: 'EMSFelix', read: 'EMSReadability'};
const out = {};
const parse = (d) => { const strokes = []; let cur = null; const tk = d.trim().split(/\s+/); for (let i = 0; i < tk.length;) { const c = tk[i]; if (c === 'M') { cur = [[+tk[i + 1], +tk[i + 2]]]; strokes.push(cur); i += 3; } else if (c === 'L') { cur.push([+tk[i + 1], +tk[i + 2]]); i += 3; } else i++; } return strokes; };
for (const [k, f] of Object.entries(FONTS)) {
	const svg = fs.readFileSync(`node_modules/hersheytext/svg_fonts/${f}.svg`, 'utf8');
	const g = {};
	for (const m of svg.matchAll(/<glyph unicode="([^"]*)"[^>]*?horiz-adv-x="([\d.]+)"(?: d="([^"]*)")?/g)) {
		const ch = m[1].replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<');
		g[ch] = {a: +m[2], s: m[3] ? parse(m[3]) : []};
	}
	// acentos compostos sobre a letra base (unidades da fonte: x-height ≈ 300, y para cima)
	const base = {'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ú': 'u', 'ç': 'c',
		'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ã': 'A', 'Õ': 'O', 'Ç': 'C', 'Ê': 'E', 'Ô': 'O', 'Â': 'A'};
	for (const [acc, b] of Object.entries(base)) {
		const bg = g[b]; if (!bg) continue;
		const cx = bg.a * 0.5 + (k === 'felix' ? 40 : 0), top = b === b.toUpperCase() ? 760 : 470;
		const mark = {
			'´': [[[cx - 30, top], [cx + 50, top + 110]]],
			'`': [[[cx + 30, top], [cx - 50, top + 110]]],
			'^': [[[cx - 70, top], [cx, top + 90], [cx + 70, top]]],
			'~': [[[cx - 90, top + 20], [cx - 50, top + 70], [cx, top + 40], [cx + 50, top + 10], [cx + 90, top + 60]]],
			'¸': [[[cx, 0], [cx + 20, -60], [cx + 60, -90], [cx + 20, -140], [cx - 40, -130]]],
		}[{'á': '´', 'é': '´', 'í': '´', 'ó': '´', 'ú': '´', 'Á': '´', 'É': '´', 'Í': '´', 'Ó': '´', 'Ú': '´', 'à': '`', 'â': '^', 'ê': '^', 'ô': '^', 'Ê': '^', 'Ô': '^', 'Â': '^', 'ã': '~', 'õ': '~', 'Ã': '~', 'Õ': '~', 'ç': '¸', 'Ç': '¸'}[acc]];
		// no i acentuado, remove o pingo (traço curto acima da x-height)
		const s = b === 'i' ? bg.s.filter((st) => Math.min(...st.map((p) => p[1])) < 380) : bg.s;
		g[acc] = {a: bg.a, s: [...s, ...mark]};
	}
	// seta → (a fonte não tem): traço + ponta
	g['→'] = {a: 900, s: [[[90, 260], [740, 250]], [[590, 380], [760, 250], [600, 120]]]};
	out[k] = g;
}
fs.writeFileSync('src/b/handfonts.json', JSON.stringify(out));
console.log('ok', Object.keys(out.felix).length, 'glifos felix', (fs.statSync('src/b/handfonts.json').size / 1024).toFixed(0), 'KB');
