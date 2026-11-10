"""Trilha sintetizada do protótipo (120 BPM, 32 s), sem samples. Gera public/audio/score.wav.
Mesmos tempos do beat sheet em src/HubFormatos.tsx (frame / 30 = segundos)."""
import math, random, wave, array, sys

SR = 48000
DUR = 137.0
N = int(SR * DUR)
buf = [0.0] * N
rnd = random.Random(7)
NOISE = [rnd.uniform(-1, 1) for _ in range(SR)]  # 1 s de ruído com seed, reutilizado

def add(t0, dur, fn, amp=1.0):
    i0 = max(0, int(t0 * SR)); i1 = min(N, int((t0 + dur) * SR))
    for i in range(i0, i1):
        buf[i] += amp * fn((i - i0) / SR, i)

def kick(t, a=0.9):
    def f(x, i):
        ph = 2 * math.pi * (45 * x + (120 - 45) * (1 - math.exp(-x * 30)) / 30)
        return math.sin(ph) * math.exp(-x * 9)
    add(t, 0.4, f, a)

def hat(t, a=0.12):
    def f(x, i):
        n = NOISE[i % SR] - NOISE[(i - 1) % SR]
        return n * math.exp(-x * 90)
    add(t, 0.06, f, a)

def clap(t, a=0.35):
    def f(x, i):
        n = NOISE[(i * 3) % SR] - 0.6 * NOISE[(i * 3 - 2) % SR]
        return n * (math.exp(-x * 28) + 0.5 * math.exp(-max(0, x - 0.012) * 40))
    add(t, 0.2, f, a)

def note(t, freq, dur, a=0.1, shape='sq', decay=8.0, attack=0.004):
    def f(x, i):
        env = min(1, x / attack) * math.exp(-x * decay)
        if shape == 'sq':
            v = 1 if math.sin(2 * math.pi * freq * x) >= 0 else -1
            v = 0.6 * v + 0.4 * math.sin(2 * math.pi * freq * x)
        elif shape == 'saw':
            v = 2 * ((freq * x) % 1) - 1
            v = 0.5 * v + 0.5 * math.sin(2 * math.pi * freq * x)
        else:
            v = math.sin(2 * math.pi * freq * x)
        return v * env
    add(t, dur, f, a)

def pad(t, freqs, dur, a=0.06):
    def f(x, i):
        env = min(1, x / 0.9) * min(1, (dur - x) / 0.8)
        return env * sum(math.sin(2 * math.pi * fr * x) + 0.3 * math.sin(2 * math.pi * fr * 2.003 * x) for fr in freqs) / len(freqs)
    add(t, dur, f, a)

def bell(t, freq, a=0.18):
    def f(x, i):
        return (math.sin(2 * math.pi * freq * x) + 0.4 * math.sin(2 * math.pi * freq * 2.76 * x)) * math.exp(-x * 3.2) * min(1, x / 0.003)
    add(t, 1.6, f, a)

def paper(t, a=0.45):  # "tapa" de papel: ruído curto e abafado
    state = [0.0]
    def f(x, i):
        state[0] += 0.25 * (NOISE[(i * 7) % SR] - state[0])
        return state[0] * math.exp(-x * 45)
    add(t, 0.12, f, a)

def rip(t, dur=0.6, a=0.5):
    state = [0.0]
    def f(x, i):
        k = 0.05 + 0.6 * (x / dur)
        state[0] += k * (NOISE[(i * 5) % SR] - state[0])
        crackle = 1 + 0.8 * (1 if NOISE[(i // 300) % SR] > 0.6 else 0)
        return state[0] * crackle * min(1, x / 0.02) * (1 - x / dur)
    add(t, dur, f, a)

def riser(t, dur, a=0.25):
    state = [0.0]
    def f(x, i):
        k = 0.01 + 0.35 * (x / dur) ** 2
        state[0] += k * (NOISE[(i * 11) % SR] - state[0])
        return state[0] * (x / dur) ** 2
    add(t, dur, f, a)

def impact(t, a=0.9):
    def f(x, i):
        return math.sin(2 * math.pi * 48 * x) * math.exp(-x * 2.2) + 0.25 * NOISE[(i * 13) % SR] * math.exp(-x * 18)
    add(t, 2.0, f, a)

A2, C3, D3, E3, G3, A3 = 110.0, 130.81, 146.83, 164.81, 196.0, 220.0
B = 0.5  # beat

# 0–2 s: abertura — pulso suave no beat + riser
for k in range(4):
    note(k * B, 55, 0.4, 0.35, 'sine', decay=7)
riser(1.0, 1.0, 0.22)

# 2–10 s: LED — kick em todo beat, hat em colcheias, arpejo quadrado em semicolcheias, baixo
arp = [A3, 261.63, 329.63, 392.0, 440.0, 392.0, 329.63, 261.63]
roots = [A2, A2, 87.31, 98.0]  # Am  Am  F  G (um por cartão)
for b in range(16):
    t = 2 + b * B
    kick(t, 0.85)
    hat(t + B / 2)
    if b % 2 == 1:
        clap(t, 0.22)
for s in range(64):
    t = 2 + s * B / 4
    note(t, arp[s % 8] * (2 if (s // 16) % 2 else 1), 0.12, 0.07, 'sq', decay=26)
for k, r in enumerate(roots):
    for b in range(4):
        note(2 + k * 2 + b * B, r, 0.45, 0.22, 'saw', decay=5)

# 10–18 s: flat — meio-tempo, pads, sinos nos nós
for b in range(0, 16, 2):
    kick(10 + b * B, 0.5)
for b in range(16):
    hat(10 + b * B + B / 2, 0.05)
pad(10.0, [A3, 261.63, 329.63], 4.2, 0.09)
pad(14.0, [174.61, 220.0, 261.63], 4.0, 0.09)
bell(10.0, 880.0, 0.12)   # esfera nasce
bell(11.5, 659.25)        # Hipótese
bell(13.0, 783.99)        # Experimento
bell(15.0, 987.77)        # Evidência

# 17.5–18.5: passagem para a colagem
riser(17.0, 1.0, 0.15)

# 18–26 s: colagem — groove leve com palmas e foley de papel
for b in range(16):
    t = 18 + b * B
    kick(t, 0.75 if b % 2 == 0 else 0.55)
    hat(t + B / 2, 0.08)
    if b % 2 == 1:
        clap(t, 0.3)
    note(t, [A2, A2, C3, G3 / 2][(b // 4) % 4], 0.4, 0.18, 'saw', decay=6)
for f0 in [555, 570, 600, 645, 690, 720]:
    paper(f0 / 30)
for f0, dur in [(660, 0.8), (735, 0.6)]:  # traços à mão: arranhado de marcador
    state = [0.0]
    def scratch(x, i, d=dur):
        state[0] += 0.4 * (NOISE[(i * 17) % SR] - state[0])
        return state[0] * (0.5 + 0.5 * math.sin(x * 60)) * (1 - x / d)
    add(f0 / 30, dur, scratch, 0.12)

# 26 s: rasgo revela a linha do tempo
rip(26.0, 0.65, 0.55)

def drum(t, a=0.7):  # tambor grave (selo / marcos)
    def f(x, i):
        return (math.sin(2 * math.pi * (62 + 40 * math.exp(-x * 20)) * x) * math.exp(-x * 5)
                + 0.3 * NOISE[(i * 19) % SR] * math.exp(-x * 35))
    add(t, 0.9, f, a)

def swell(t, dur, a=0.2, up=True):  # whoosh de ruído filtrado
    st = [0.0]
    def f(x, i):
        k = x / dur if up else 1 - x / dur
        st[0] += (0.02 + 0.3 * k) * (NOISE[(i * 23) % SR] - st[0])
        return st[0] * math.sin(math.pi * x / dur)
    add(t, dur, f, a)

def click(t, a=0.25):
    def f(x, i):
        return (NOISE[(i * 29) % SR] - NOISE[(i * 29 - 1) % SR]) * math.exp(-x * 400)
    add(t, 0.02, f, a)

def blip(t, f0=660, f1=990, a=0.16):
    def f(x, i):
        fr = f0 + (f1 - f0) * min(1, x / 0.06)
        return math.sin(2 * math.pi * fr * x) * math.exp(-x * 18)
    add(t, 0.25, f, a)

def piano(t, freq, a=0.12, dur=1.6):
    def f(x, i):
        h = sum(math.sin(2 * math.pi * freq * k * x) / k ** 1.6 for k in (1, 2, 3, 4))
        return h * math.exp(-x * 2.6) * min(1, x / 0.004)
    add(t, dur, f, a)

PENTA = [220.0, 246.94, 277.18, 329.63, 369.99, 440.0, 493.88]

# 26–34 s: F4 linha do tempo — tambor nos tempos 1 e 3, pizzicato pentatônico, pincelada, selo
for b in range(0, 16, 2):
    drum(26 + b * B, 0.45)
for s_ in range(0, 32):
    if s_ % 3 != 2:
        note(26 + s_ * B / 2, PENTA[(s_ * 3) % 7], 0.3, 0.07, 'sine', decay=9)
swell(26.7, 1.9, 0.14)
for fr in (70, 95, 120):
    drum(26 + fr / 30, 0.35)
drum(26 + 165 / 30, 0.95)
impact(26 + 165 / 30, 0.35)
riser(26 + 200 / 30, 1.33, 0.22)

# 34–42 s: F5 jornada — groove leve, um "boing" a cada pouso, whoosh no recuo
for b in range(16):
    t = 34 + b * B
    kick(t, 0.6)
    hat(t + B / 2, 0.07)
    note(t, [A2, A2, 87.31, 98.0][(b // 4) % 4], 0.4, 0.16, 'saw', decay=6)
for k, fr in enumerate((24, 72, 120, 168)):
    blip(34 + fr / 30, 520 + k * 110, 880 + k * 140, 0.2)
swell(34 + 170 / 30, 0.9, 0.14)

# 42–50 s: F6 demo — cliques de UI, carregando, sucesso, gráfico
for b in range(16):
    t = 42 + b * B
    kick(t, 0.45)
    hat(t + B / 2, 0.05)
click(42 + 48 / 30, 0.5)
for k in range(8):
    click(42 + 62 / 30 + k * 0.15, 0.12)
bell(42 + 100 / 30, 1046.5, 0.14)
bell(42 + 100 / 30 + 0.12, 1318.5, 0.1)
swell(42 + 116 / 30, 0.5, 0.1)
for k in range(10):
    note(42 + 140 / 30 + k * 0.17, 440 * 2 ** (k / 12), 0.15, 0.05, 'sine', decay=14)
swell(42 + 200 / 30, 1.1, 0.14)

# 50–58 s: F7 data story — piano seco, uma nota por barra que sobe
for bar, ch in enumerate([[A3, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66], [A3, 261.63, 329.63]]):
    for fr in ch:
        piano(50 + bar * 2, fr, 0.06)
for k in range(5):
    piano(51 + k * 0.2, [523.25, 587.33, 659.25, 783.99, 880.0][k], 0.09 if k != 3 else 0.14)
swell(50 + 200 / 30, 1.1, 0.16)

# 58–66 s: F8 paper em traço — esparso, pings nos nós
pad(58.0, [A3, 329.63, 493.88], 8.0, 0.06)
for b in range(0, 16, 4):
    kick(58 + b * B, 0.35)
for fr in (44, 52, 96, 106, 116, 140, 150):
    note(58 + fr / 30, 1318.5 if fr > 90 else 987.77, 0.4, 0.05, 'sine', decay=7)
swell(58 + 206 / 30, 1.1, 0.12)

# 66–109 s: F9 entrevista — sem música (fala original). Só a íris no fim.
swell(108.0, 1.0, 0.1, up=False)

# 109–117 s: F10 3D — pad cinematográfico, sub grave na entrada, riser na separação, inundação
impact(109.1, 0.55)
pad(109.0, [110.0, 164.81, 220.0, 329.63], 8.0, 0.1)
riser(110.2, 1.3, 0.16)
for b in range(4, 16, 2):
    kick(109 + b * B, 0.4)
swell(109 + 214 / 30, 0.9, 0.2)

# 117–125 s: F11 anúncio — kick em todo beat, palmas, impacto por palavra, whoosh nas inundações
for b in range(16):
    t = 117 + b * B
    kick(t, 0.85)
    hat(t + B / 2, 0.1)
    if b % 2 == 1:
        clap(t, 0.3)
    note(t, [A2, 87.31, 98.0, A2][(b // 4) % 4], 0.4, 0.2, 'saw', decay=6)
for fr in (6, 66, 126):
    impact(117 + fr / 30, 0.35)
for fr in (52, 112):
    swell(117 + fr / 30, 0.5, 0.2)
swell(117 + 196 / 30, 1.3, 0.14, up=False)

# 125–137 s: fechamento — impacto com o logo, acorde longo e arpejo suave durante a lista de skills
impact(125 + 6 / 30, 0.7)
pad(125.0, [A3, 261.63, 329.63, 440.0], 12.0, 0.11)
for k in range(11):  # um ping por linha da lista (36 + 5·i frames)
    note(125 + (36 + k * 5) / 30, [880.0, 987.77, 1046.5, 1174.66, 1318.5][k % 5], 0.5, 0.035, 'sine', decay=6)
for b in range(0, 20, 4):
    note(126.5 + b * B, [A2, 87.31, 98.0, A2, A2][b // 4], 1.6, 0.1, 'sine', decay=1.8)

# limitador suave (saturação tanh) para subir a loudness sem clipar; depois pico em -3 dBFS (margem para o AAC)
DRIVE = float(sys.argv[2]) if len(sys.argv) > 2 else 1.8  # 1.8 → ≈ -17 LUFS no MP4
peak = max(abs(v) for v in buf) or 1
buf = [math.tanh(DRIVE * v / peak) / math.tanh(DRIVE) for v in buf]
peak = max(abs(v) for v in buf) or 1
g = 10 ** (-3.0 / 20) / peak
out = array.array('h')
for v in buf:
    s = int(max(-1, min(1, v * g)) * 32767)
    out.append(s); out.append(s)
path = sys.argv[1] if len(sys.argv) > 1 else 'public/audio/score.wav'
with wave.open(path, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(out.tobytes())
print('ok', path, f'peak_gain={g:.3f}')
