"""Gera src/editorial-edl.json a partir de work/words.json (transcrição whisper.cpp, tempos em s do clipe).
Legendas: grupos de até 6 palavras, quebrando na pontuação. Palavras cinéticas e telas divididas: decididas à mão,
com o texto IGUAL ao que é falado e posições fora dos rostos (mapa de tomadas abaixo).
Mapa de tomadas (aprox.): 0–10 âncora (à direita) · 10–13 guardanapo · 13–16 Roberto plano aberto (à esquerda)
· 16–18 outro entrevistado (centro) · 18–21 rascunho no guardanapo · 21–32,5 Roberto em close (rosto em ~62% da largura;
crachá do JN no canto inferior esquerdo no início) · 32,5–35 plano a dois · 35–41 pulseira (b-roll)."""
import json
W = json.load(open('work/words.json'))
# quebra na pontuação ou em 7 palavras; grupos de 1–2 palavras são unidos ao anterior (até 9)
caps, cur = [], []
for w, s, e in W:
    cur.append({'w': w, 's': round(s, 2), 'e': round(e, 2)})
    if len(cur) >= 7 or w.endswith(('.', '?', '!')) or (w.endswith(',') and len(cur) >= 3):
        caps.append(cur); cur = []
if cur: caps.append(cur)
merged = []
for g in caps:
    if merged and len(g) <= 2 and len(merged[-1]) + len(g) <= 9 and not merged[-1][-1]['w'].endswith(('.', '?', '!')):
        merged[-1] += g
    else:
        merged.append(g)
caps = merged
kinetic = [
    {'text': 'reabilitação', 's': 5.8, 'e': 9.6, 'x': 120, 'y': 320, 'size': 124, 'accent': True},
    {'text': 'ENGENHEIRO', 's': 14.16, 'e': 16.2, 'x': 1080, 'y': 230, 'size': 96, 'ink': True},
    {'text': '+ FISIOTERAPEUTA', 's': 16.41, 'e': 18.0, 'x': 110, 'y': 180, 'size': 76, 'ink': True},
    {'text': 'guardanapo', 's': 18.67, 'e': 20.6, 'x': 640, 'y': 130, 'size': 116, 'accent': True, 'ink': True},
    {'text': 'CINCO DIAS', 's': 21.18, 'e': 24.4, 'x': 120, 'y': 250, 'size': 92, 'ink': True},
    {'text': 'esboço', 's': 33.59, 'e': 35.0, 'x': 780, 'y': 120, 'size': 120, 'accent': True, 'ink': True},
    {'text': 'DE PONTA', 's': 35.19, 'e': 38.2, 'x': 120, 'y': 150, 'size': 100, 'ink': True},
    {'text': 'e muito barato', 's': 35.94, 'e': 38.2, 'x': 120, 'y': 270, 'size': 84, 'accent': True, 'ink': True},
]
splits = [{'s': 26.0, 'e': 31.6, 'faceX': 0.62, 'quote': 'Eu tinha cinco dias para chegar a uma solução que tinha a ver com saúde'}]
json.dump({'captions': caps, 'kinetic': kinetic, 'splits': splits}, open('src/editorial-edl.json', 'w'), ensure_ascii=False, indent=1)
print(len(caps), 'grupos de legenda')
for g in caps: print(f"{g[0]['s']:6.2f} {' '.join(x['w'] for x in g)}")
