// Screenshot de um HTML local com o Chrome headless do Remotion. Uso: node scripts/shot_html.mjs <arquivo.html> <saida.png> [w] [h]
import fs from 'node:fs'; import path from 'node:path'; import {openBrowser} from '@remotion/renderer';
const [, , html, out, w = '1600', h = '900'] = process.argv;
const b = await openBrowser('chrome', {chromiumOptions: {}});
const p = await b.newPage({context: () => null, logLevel: 'error', indent: false, pageIndex: 0, onBrowserLog: null, onLog: () => {}});
const cdp = p._client();
await cdp.send('Emulation.setDeviceMetricsOverride', {width: +w, height: +h, deviceScaleFactor: 1, mobile: false});
await p.goto({url: 'file://' + path.resolve(html), timeout: 20000});
const s = await cdp.send('Page.captureScreenshot', {format: 'png'});
fs.writeFileSync(out, Buffer.from(s.value.data, 'base64')); await b.close({silent: true});
