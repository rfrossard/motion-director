"""Trilha sintetizada do vídeo "Biblioteca de estilos" a partir de src/b/plan.json (mesma timeline do Remotion).
Um gerador por cena (clima por capítulo), música abaixada sob fala real, efeito por transição.
Uso: python3 scripts/score2.py public/audio/score.wav [drive]"""
import json, math, random, sys, wave, array

SR = 44100
plan = json.load(open('src/b/plan.json'))
OV = plan['overlap']
T, at = [], 0
for s in plan['scenes']:
    T.append({**s, 'start': at / 30, 'len': s['dur'] / 30})
    at += s['dur'] - OV.get(s['out'], 0)
DUR = T[-1]['start'] + T[-1]['len'] + 0.5
N = int(SR * DUR)
buf = [0.0] * N
rnd = random.Random(11)
NOISE = [rnd.uniform(-1, 1) for _ in range(SR)]
B = 0.5  # 120 BPM

def add(t0, dur, fn, amp=1.0):
    i0 = max(0, int(t0 * SR)); i1 = min(N, int((t0 + dur) * SR))
    for i in range(i0, i1):
        buf[i] += amp * fn((i - i0) / SR, i)

def kick(t, a=0.8):
    add(t, 0.35, lambda x, i: math.sin(2 * math.pi * (45 * x + 75 * (1 - math.exp(-x * 30)) / 30)) * math.exp(-x * 9), a)
def hat(t, a=0.08):
    add(t, 0.05, lambda x, i: (NOISE[i % SR] - NOISE[(i - 1) % SR]) * math.exp(-x * 90), a)
def clap(t, a=0.25):
    add(t, 0.18, lambda x, i: (NOISE[(i * 3) % SR] - 0.6 * NOISE[(i * 3 - 2) % SR]) * (math.exp(-x * 28) + 0.5 * math.exp(-max(0, x - 0.012) * 40)), a)
def tone(t, fr, dur, a=0.1, shape='sine', decay=6.0, att=0.005):
    def f(x, i):
        env = min(1, x / att) * math.exp(-x * decay)
        if shape == 'sq': v = 0.6 * (1 if math.sin(2 * math.pi * fr * x) >= 0 else -1) + 0.4 * math.sin(2 * math.pi * fr * x)
        elif shape == 'saw': v = 0.5 * (2 * ((fr * x) % 1) - 1) + 0.5 * math.sin(2 * math.pi * fr * x)
        elif shape == 'tri': v = 2 * abs(2 * ((fr * x) % 1) - 1) - 1
        elif shape == 'piano': v = sum(math.sin(2 * math.pi * fr * k * x) / k ** 1.6 for k in (1, 2, 3, 4))
        else: v = math.sin(2 * math.pi * fr * x)
        return v * env
    add(t, dur, f, a)
def pad(t, frs, dur, a=0.06):
    def f(x, i):
        env = min(1, x / 0.8) * min(1, max(0, (dur - x)) / 0.8)
        return env * sum(math.sin(2 * math.pi * fr * x) + 0.3 * math.sin(2 * math.pi * fr * 2.003 * x) for fr in frs) / len(frs)
    add(t, dur, f, a)
def swell(t, dur, a=0.15, up=True):
    st = [0.0]
    def f(x, i):
        k = x / dur if up else 1 - x / dur
        st[0] += (0.02 + 0.3 * k) * (NOISE[(i * 23) % SR] - st[0])
        return st[0] * math.sin(math.pi * x / dur)
    add(t, dur, f, a)
def impact(t, a=0.6):
    add(t, 1.5, lambda x, i: math.sin(2 * math.pi * 48 * x) * math.exp(-x * 2.5) + 0.25 * NOISE[(i * 13) % SR] * math.exp(-x * 18), a)
def click(t, a=0.2):
    add(t, 0.02, lambda x, i: (NOISE[(i * 29) % SR] - NOISE[(i * 29 - 1) % SR]) * math.exp(-x * 400), a)
def paper(t, a=0.35):
    st = [0.0]
    def f(x, i):
        st[0] += 0.25 * (NOISE[(i * 7) % SR] - st[0]); return st[0] * math.exp(-x * 45)
    add(t, 0.12, f, a)
def drum(t, a=0.5):
    add(t, 0.9, lambda x, i: math.sin(2 * math.pi * (62 + 40 * math.exp(-x * 20)) * x) * math.exp(-x * 5) + 0.3 * NOISE[(i * 19) % SR] * math.exp(-x * 35), a)
def bell(t, fr, a=0.1):
    add(t, 1.6, lambda x, i: (math.sin(2 * math.pi * fr * x) + 0.4 * math.sin(2 * math.pi * fr * 2.76 * x)) * math.exp(-x * 3.2) * min(1, x / 0.003), a)

A2, C3, D3, E3, F3, G3, A3 = 110.0, 130.81, 146.83, 164.81, 174.61, 196.0, 220.0
CHORDS = [[A3, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66], [164.81, 207.65, 246.94]]
PENTA = [220.0, 246.94, 277.18, 329.63, 369.99, 440.0, 493.88]
SPEECH = {'creator', 'archival', 'broll', 'podcast'}

def beats(s):
    t0 = s['start']; n = int(s['len'] / B)
    return [t0 + k * B for k in range(n)]

def groove(s, g=1.0, arp=False, clapon=True):
    for k, t in enumerate(beats(s)):
        kick(t, 0.75 * g); hat(t + B / 2, 0.07 * g)
        if clapon and k % 2 == 1: clap(t, 0.2 * g)
        tone(t, [A2, A2, 87.31, 98.0][(k // 4) % 4], 0.45, 0.16 * g, 'saw', decay=6)
        if arp:
            for q in range(4): tone(t + q * B / 4, [A3, 261.63, 329.63, 392.0][(k + q) % 4] * 2, 0.12, 0.05 * g, 'sq', decay=24)

def mellow(s, g=1.0):
    for k, t in enumerate(beats(s)):
        if k % 2 == 0: kick(t, 0.4 * g)
        hat(t + B / 2, 0.04 * g)
    for c in range(int(s['len'] / 2)):
        pad(s['start'] + c * 2, CHORDS[c % 4], 2.2, 0.07 * g)

for s in T:
    i, t0, L = s['id'], s['start'], s['len']
    g = 0.3 if i in SPEECH else 1.0
    if i == 'intro':
        for k in range(8): tone(t0 + k * 0.4, [523.25, 659.25, 783.99, 1046.5][k % 4], 0.3, 0.12, 'sq', decay=10); kick(t0 + k * 0.4, 0.5)
        impact(t0 + 3.3, 0.4); pad(t0 + 3.3, [A3, 329.63, 440.0], L - 3.3, 0.07)
    elif s['chap'] == 'social':
        groove(s, g, arp=(i in ('hype', 'led', 'anime')))
        if i == 'anime': [impact(t0 + fr / 30, 0.35) for fr in (75, 120, 230)]
        if i == 'toon3d': [tone(t0 + fr / 30, 520 + n * 140, 0.3, 0.14, 'sine', decay=8) for n, fr in enumerate((45, 90, 135))]; bell(t0 + 205 / 30, 1046.5, 0.15)
        if i == 'hype': [impact(t0 + fr / 30, 0.25) for fr in (6, 66, 126, 186)]
    elif i == 'manim':
        pad(t0, [A3, 329.63, 493.88], L, 0.05)
        for k in range(int(L / 2)): tone(t0 + k * 2, PENTA[k % 7] * 2, 1.2, 0.04, 'sine', decay=3)
    elif i == 'comic':
        mellow(s, 0.7)
        for k, t in enumerate(beats(s)): tone(t, PENTA[(k * 2) % 7] * 2, 0.2, 0.05, 'tri', decay=14)
        for fr in (190, 205): paper(t0 + fr / 30, 0.4); impact(t0 + fr / 30, 0.15)
    elif i == 'sketch':
        mellow(s, 0.6)
        for fr in range(10, 392, 9): add(t0 + fr / 30, 0.2, lambda x, j: (NOISE[(j * 17) % SR]) * 0.5 * math.exp(-x * 12), 0.04)  # marcador
    elif s['chap'] == 'youtube':
        mellow(s, 0.8)
    elif i == 'datastory' or i == 'stroke':
        for c in range(int(L / 2)):
            for fr in CHORDS[c % 4]: tone(t0 + c * 2, fr, 1.8, 0.05, 'piano', decay=2.4)
        if i == 'datastory': [tone(t0 + (20 + k * 4) / 30, 523.25 * 2 ** (k / 12), 0.25, 0.04, 'piano', decay=6) for k in range(12)]
    elif i == 'ink':
        for k, t in enumerate(beats(s)):
            if k % 2 == 0: drum(t, 0.35)
            if k % 3 != 2: tone(t, PENTA[(k * 3) % 7], 0.3, 0.06, 'sine', decay=9)
        drum(t0 + 165 / 30, 0.9)
    elif i == 'particles':
        pad(t0, [110.0, 164.81, 220.0, 329.63], L, 0.08)
        for k in range(int(L * 3)): bell(t0 + k / 3, PENTA[(k * 5) % 7] * 4, 0.025)
    elif i == 'extrude3d':
        impact(t0 + 0.1, 0.45); pad(t0, [110.0, 164.81, 220.0], L, 0.09); swell(t0 + 1.2, 1.4, 0.12)
    elif i == 'news':
        swell(t0, 1.0, 0.2); impact(t0 + 0.9, 0.5)
        for k, t in enumerate(beats(s)):
            if t - t0 > 2.3: kick(t, 0.55); hat(t + B / 2, 0.06); tone(t, [A2, 87.31][(k // 8) % 2], 0.3, 0.12, 'saw', decay=8)
        for b in range(3): drum(t0 + (150 + b * 110) / 30, 0.6); bell(t0 + (150 + b * 110) / 30, 880.0, 0.08)
    elif i == 'geomap':
        pad(t0, [55.0, 82.41, 110.0, 164.81], L, 0.12); swell(t0 + 6.6, 1.8, 0.14); impact(t0 + 8.2, 0.35)
    elif i == 'blender':
        pad(t0, [A3, 261.63, 329.63, 493.88], L, 0.07)
        for k in range(int(L)): tone(t0 + k, PENTA[k % 7] * 2, 0.8, 0.03, 'piano', decay=3)
    elif i in ('archival',):
        pad(t0, [55.0, 110.0], L, 0.05)
    elif i in ('broll', 'podcast'):
        mellow(s, 0.35)
    elif i == 'screencast':
        mellow(s, 0.6)
        log = json.load(open('src/b/screencast-log.json'))['frames']
        for q in log:
            if q['click']: click(t0 + 14 / 30 + q['t'], 0.5)
        for k in range(30): click(t0 + 14 / 30 + 3.3 + k * 0.06, 0.06)
        bell(t0 + 14 / 30 + 13.4, 1046.5, 0.12)
    elif i == 'demo':
        for c in range(int(L / 2)):
            for fr in CHORDS[c % 4]: tone(t0 + c * 2, fr * 2, 1.6, 0.04, 'piano', decay=2.6)
        for k in range(50): click(t0 + 70 / 30 + k * 0.035, 0.05)
    elif i == 'sand':
        for c in range(int(L / 2)):
            for fr in CHORDS[c % 4]: tone(t0 + c * 2, fr, 1.9, 0.045, 'piano', decay=2)
        for tt in (0, 160, 330, 630): swell(t0 + tt / 30, 2.3, 0.09)
    elif i == 'shadow':
        pad(t0, [A3, 329.63], L, 0.05)
        for k, t in enumerate(beats(s)):
            if k % 2 == 0: tone(t, PENTA[(k * 5) % 7] * 2, 0.6, 0.06, 'tri', decay=5)
        bell(t0 + 240 / 30, 659.25, 0.15); swell(t0 + 230 / 30, 1.5, 0.1)
    elif i == 'collage':
        groove(s, 0.6, clapon=True)
        for fr in (10, 30, 50, 75, 100, 115, 130): paper(t0 + fr / 30, 0.4)
    elif i == 'pixel':
        for k, t in enumerate(beats(s)):
            if k % 2 == 0: kick(t, 0.35)
            hat(t + B / 2, 0.04)
            tone(t, [A3, 261.63, 329.63, 392.0, 329.63, 261.63][k % 6], 0.35, 0.05, 'sq', decay=5)
        for c in range(int(L / 2)): pad(s['start'] + c * 2, [x / 2 for x in CHORDS[c % 4]], 2.2, 0.06)
    elif i == 'mosaic':
        pad(t0, [A3, 329.63, 440.0, 554.37], L, 0.07)
        for k in range(160):
            tt = 40 / 30 + (k / 160) * 6.0
            click(t0 + tt + rnd.random() * 0.05, 0.05)
        for k in range(8): bell(t0 + 3.7 + k * 0.25, [880, 987.77, 1108.73, 1318.5][k % 4], 0.05)
    elif i == 'outro':
        impact(t0 + 0.5, 0.5); pad(t0, [A3, 261.63, 329.63, 440.0], L, 0.1); bell(t0 + 1.3, 880.0, 0.1)
    # efeito da transição de saída
    end = t0 + L
    o = s['out']
    if o in ('whip', 'swipe', 'zoom', 'page'): swell(end - 0.45, 0.5, 0.2)
    elif o == 'impact': impact(end - 0.1, 0.45)
    elif o == 'flood': swell(end - 0.4, 0.45, 0.16)
    elif o == 'iris': swell(end - 0.5, 0.5, 0.1, up=False)

# nivelamento por cena: cenas calmas sobem até ~4 dB abaixo das energéticas (rampas de 0,4 s nas fronteiras)
ENERGETIC = {'hype', 'creator', 'anime', 'toon3d', 'led', 'news', 'ink', 'collage', 'archival', 'broll', 'podcast'}
def rms(a, b):
    i0, i1 = int(a * SR), min(N, int(b * SR)); seg_ = buf[i0:i1]
    return math.sqrt(sum(v * v for v in seg_[::4]) / max(1, len(seg_[::4]))) + 1e-9
levels = {s['id']: rms(s['start'], s['start'] + s['len']) for s in T}
ref = sorted(levels[i] for i in ENERGETIC if i in levels and i not in SPEECH)[len([i for i in ENERGETIC if i not in SPEECH]) // 2]
target = ref * 10 ** (-4 / 20)
gain = [1.0] * N
for s in T:
    if s['id'] in ENERGETIC or s['id'] in SPEECH: continue
    gsc = min(8.0, max(1.0, target / levels[s['id']]))
    i0, i1 = int(s['start'] * SR), min(N, int((s['start'] + s['len']) * SR)); r = int(0.4 * SR)
    for i in range(i0, i1):
        k = min(1.0, (i - i0) / r, (i1 - i) / r)
        gain[i] = max(gain[i], 1 + (gsc - 1) * k)
buf = [v * g_ for v, g_ in zip(buf, gain)]

DRIVE = float(sys.argv[2]) if len(sys.argv) > 2 else 1.6
peak = max(abs(v) for v in buf) or 1
buf = [math.tanh(DRIVE * v / peak) / math.tanh(DRIVE) for v in buf]
peak = max(abs(v) for v in buf) or 1
g = 10 ** (-3.0 / 20) / peak
out = array.array('h')
for v in buf:
    s_ = int(max(-1, min(1, v * g)) * 32767); out.append(s_); out.append(s_)
with wave.open(sys.argv[1] if len(sys.argv) > 1 else 'public/audio/score.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print('ok', round(DUR, 1), 's')
