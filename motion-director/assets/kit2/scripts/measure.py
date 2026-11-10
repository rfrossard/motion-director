"""Mede o áudio exportado: loudness integrada (BS.1770, K-weighting + gating), pico de amostra e sincronia de eventos."""
import wave, array, math, sys
w = wave.open(sys.argv[1]); sr = w.getframerate(); ch = w.getnchannels()
a = array.array('h', w.readframes(w.getnframes()))
L = [a[i] / 32768 for i in range(0, len(a), ch)]
R = [a[i + 1] / 32768 for i in range(0, len(a), ch)] if ch > 1 else L
def biquad(x, b, a_):
    y = [0.0] * len(x); x1 = x2 = y1 = y2 = 0.0
    for i, v in enumerate(x):
        o = b[0]*v + b[1]*x1 + b[2]*x2 - a_[1]*y1 - a_[2]*y2
        x2, x1, y2, y1 = x1, v, y1, o; y[i] = o
    return y
def kw(x):
    x = biquad(x, [1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585])
    return biquad(x, [1.0, -2.0, 1.0], [1, -1.99004745483398, 0.99007225036621])
kl, kr = kw(L), kw(R)
blk, hop = int(0.4 * sr), int(0.1 * sr)
z = []
for s in range(0, len(kl) - blk, hop):
    e = (sum(v*v for v in kl[s:s+blk]) + sum(v*v for v in kr[s:s+blk])) / blk
    z.append(e)
lk = lambda e: -0.691 + 10 * math.log10(e) if e > 0 else -200
g1 = [e for e in z if lk(e) > -70]
rel = lk(sum(g1) / len(g1)) - 10
g2 = [e for e in g1 if lk(e) > rel]
print(f"integrada: {lk(sum(g2)/len(g2)):.1f} LUFS")
pk = max(max(abs(v) for v in L), max(abs(v) for v in R))
print(f"pico de amostra: {20*math.log10(pk):.1f} dBFS")
# sincronia: pico de envelope (janela de 10 ms) mais próximo de cada evento esperado
win = int(0.01 * sr)
env = [max(abs(v) for v in L[i:i+win]) for i in range(0, len(L) - win, win)]
for name, t in [('papel fita', 18.5), ('papel faixa', 19.0), ('papel cartão', 20.0), ('papel adesivo', 21.5), ('rasgo', 26.0), ('impacto', 28.0)]:
    c = int(t / 0.01); lo, hi = c - 5, c + 8
    k = max(range(lo, hi), key=lambda j: env[j])
    print(f"{name:14s} esperado {t:5.2f}s  pico {k*0.01:5.2f}s  Δ {(k*0.01 - t)*1000:+.0f} ms")
