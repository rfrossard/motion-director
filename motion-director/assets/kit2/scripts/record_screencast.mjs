// Gravação REAL de tela: Chrome headless do Remotion + eventos de mouse/teclado via CDP numa página real.
// Captura em tempo real (taxa variável) + log do cursor; depois vira vídeo de taxa constante.
// Uso: node scripts/record_screencast.mjs
import fs from 'node:fs';
import path from 'node:path';
import {openBrowser} from '@remotion/renderer';

const OUT = path.resolve('work/screencast');
fs.rmSync(OUT, {recursive: true, force: true});
fs.mkdirSync(OUT, {recursive: true});
const W = 1440, H = 900, DPR = 1.5;

const browser = await openBrowser('chrome', {chromiumOptions: {}});
const page = await browser.newPage({context: () => null, logLevel: 'error', indent: false, pageIndex: 0, onBrowserLog: null, onLog: () => {}});
const cdp = page._client();
await cdp.send('Emulation.setDeviceMetricsOverride', {width: W, height: H, deviceScaleFactor: DPR, mobile: false});
await page.goto({url: 'file://' + path.resolve('screencast/app.html'), timeout: 20000});

const center = async (sel) => page.evaluate((s) => { const r = document.querySelector(s).getBoundingClientRect(); return [r.x + r.width / 2, r.y + r.height / 2]; }, sel);
const P = {
	drop: await center('#drop'), titulo: await center('#titulo'), desc: await center('#desc'),
	t1: await center('#t1'), t2: await center('#t2'), pub: await center('#pub'),
};
// roteiro de ações (segundos de relógio desde o início)
const plan = [
	{t: 0.6, move: P.drop, dur: 0.9}, {t: 1.6, click: true},
	{t: 2.3, move: P.titulo, dur: 0.7}, {t: 3.1, click: true}, {t: 3.3, type: 'Cinco dias para uma solução'},
	{t: 5.2, move: P.desc, dur: 0.5}, {t: 5.8, click: true}, {t: 6.0, type: 'Do guardanapo ao protótipo de reabilitação.'},
	{t: 8.9, move: P.t1, dur: 0.9}, {t: 9.9, click: true},
	{t: 10.3, move: P.t2, dur: 0.4}, {t: 10.9, click: true},
	{t: 11.4, move: P.pub, dur: 0.8}, {t: 12.4, click: true},
];
const END = 15.0;
let cur = [1150, 720], from = cur, to = cur, mv0 = 0, mv1 = 0;
let typing = null; // {text, i, next}
const log = [];
const ease = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const t0 = Date.now();
let k = 0, pi = 0;
while (true) {
	const t = (Date.now() - t0) / 1000;
	if (t > END) break;
	let clicked = false;
	while (pi < plan.length && plan[pi].t <= t) {
		const a = plan[pi++];
		if (a.move) { from = cur; to = a.move; mv0 = t; mv1 = t + a.dur; }
		if (a.click) {
			await cdp.send('Input.dispatchMouseEvent', {type: 'mousePressed', x: cur[0], y: cur[1], button: 'left', clickCount: 1});
			await cdp.send('Input.dispatchMouseEvent', {type: 'mouseReleased', x: cur[0], y: cur[1], button: 'left', clickCount: 1});
			clicked = true;
		}
		if (a.type) typing = {text: a.type, i: 0, next: t};
	}
	if (t < mv1) { const e = ease((t - mv0) / (mv1 - mv0)); cur = [from[0] + (to[0] - from[0]) * e, from[1] + (to[1] - from[1]) * e]; }
	else cur = to;
	await cdp.send('Input.dispatchMouseEvent', {type: 'mouseMoved', x: cur[0], y: cur[1]});
	if (typing && t >= typing.next && typing.i < typing.text.length) {
		const n = Math.min(typing.text.length, typing.i + 2); // ~2 caracteres por captura
		await cdp.send('Input.insertText', {text: typing.text.slice(typing.i, n)});
		typing.i = n; typing.next = t + 0.06;
	}
	const shot = await cdp.send('Page.captureScreenshot', {format: 'jpeg', quality: 88});
	const name = `f_${String(k).padStart(5, '0')}.jpg`;
	fs.writeFileSync(path.join(OUT, name), Buffer.from(shot.value.data, 'base64'));
	log.push({t: +t.toFixed(3), file: name, x: +cur[0].toFixed(1), y: +cur[1].toFixed(1), click: clicked});
	k++;
}
fs.writeFileSync(path.join(OUT, 'log.json'), JSON.stringify({W, H, DPR, frames: log}, null, 0));
// lista para o concat do ffmpeg (taxa variável → constante)
let list = '';
for (let i = 0; i < log.length; i++) {
	const d = (i + 1 < log.length ? log[i + 1].t : END) - log[i].t;
	list += `file '${log[i].file}'\nduration ${d.toFixed(3)}\n`;
}
list += `file '${log[log.length - 1].file}'\n`;
fs.writeFileSync(path.join(OUT, 'list.txt'), list);
console.log('capturas', log.length, 'fps médio', (log.length / END).toFixed(1));
await browser.close({silent: true});
