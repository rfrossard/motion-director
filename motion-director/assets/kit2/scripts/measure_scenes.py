"""Loudness (EBU R128) por cena do MP4, usando a timeline de src/b/plan.json. Uso: python3 scripts/measure_scenes.py out/video.mp4 [ffmpeg]"""
import json, subprocess, sys
V = sys.argv[1]; FF = sys.argv[2] if len(sys.argv) > 2 else 'ffmpeg'
d = json.load(open('src/b/plan.json')); ov = d['overlap']; at = 0; rows = []
for s in d['scenes']:
    st, L = at / 30, s['dur'] / 30
    r = subprocess.run([FF, '-hide_banner', '-nostats', '-ss', str(st), '-t', str(L), '-i', V, '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float([l for l in r.splitlines() if l.strip().startswith('I:')][-1].split()[1]); P = float([l for l in r.splitlines() if l.strip().startswith('Peak:')][-1].split()[1])
    rows.append((s['id'], st, I, P)); at += s['dur'] - ov.get(s['out'], 0)
for i, st, I, P in rows: print(f'{i:12s} {st:7.1f}s {I:6.1f} LUFS  pico {P:5.1f}')
print('faixa', min(r[2] for r in rows), '…', max(r[2] for r in rows), 'LUFS · pico máx', max(r[3] for r in rows))
