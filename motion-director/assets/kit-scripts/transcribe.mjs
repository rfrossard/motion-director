// Transcrição local (whisper.cpp) com timestamps por palavra. Uso: node scripts/transcribe.mjs <wav16k> <out.json>
import path from 'node:path';
import fs from 'node:fs';
import {installWhisperCpp, downloadWhisperModel, transcribe} from '@remotion/install-whisper-cpp';
const [, , input, out] = process.argv;
const to = path.join(process.cwd(), 'whisper.cpp');
const version = '1.5.5';
await installWhisperCpp({to, version, printOutput: false});
await downloadWhisperModel({model: 'medium', folder: to, printOutput: false});
const res = await transcribe({inputPath: path.resolve(input), whisperPath: to, whisperCppVersion: version, model: 'medium', tokenLevelTimestamps: true, language: 'pt'});
fs.writeFileSync(out, JSON.stringify(res, null, 1));
for (const t of res.transcription) console.log(t.timestamps.from.slice(3, 11), '→', t.timestamps.to.slice(3, 11), t.text.trim());
