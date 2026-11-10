# Contratos comuns

Escreva estes arquivos no projeto **antes** das cenas. Todos os executores os leem.

## 1. `timeline.json` — beat grid e trechos

```json
{ "fps": 30, "bpm": 120, "width": 1920, "height": 1080,
  "sections": [ {"id": "s1", "style": "led", "from": 0, "frames": 240}, {"id": "s2", "style": "flat", "from": 240, "frames": 240} ] }
```
- 1 beat = `60/bpm` s; a 30 fps e 120 BPM, 15 frames. Seções começam em downbeat (múltiplos de 60 frames a 120 BPM).
- Com música do usuário: meça o BPM e os downbeats (numpy/librosa/aubio) e calibre pelos kicks reais antes de fixar.
- Footage real que não cabe em compassos inteiros: estenda a seção até o próximo beat inteiro e retome o grid depois (como no editorial de 1290 frames do vídeo do Hub).

## 2. `handoff.json` — o bastão entre estilos

```json
{ "s1->s2": { "shape": "circle", "color": "#FF6200", "x": 960, "y": 540, "r": 8,  "frame": 299,
              "out": "pontos convergem no centro", "in": "ponto cresce e vira esfera" },
  "s2->s3": { "shape": "rect", "x": 575, "y": 445, "w": 806, "h": 454, "rot": -3.5, "frame": 552,
              "out": "cena encolhe e vira foto", "in": "foto colada no caderno" } }
```
- O último frame de N e o primeiro de N+1 mostram o bastão **idêntico** (forma, cor, posição, tamanho). Isso permite corte invisível mesmo entre motores diferentes.
- Bastões testados: ponto/esfera, foto/quadro, linha vertical, círculo de inundação, contorno de documento → quadro 16:9, íris, página rasgada revelando a cena de baixo.
- Revise com stills **dos dois lados** de cada passagem.

## 3. Motores diferentes na mesma peça

- Cada estilo com motor próprio (Manim, Blender, canvas do collage, HTML/Playwright) renderiza um **clipe** (MP4/ProRes, mesmo fps e tamanho) com o bastão nas pontas.
- O master monta em Remotion: `<Sequence from={...}><OffthreadVideo src={staticFile('clips/sN.mp4')} /></Sequence>`, com áudio da trilha global por cima.
- Cenas leves ficam direto no projeto Remotion (kit em `assets/kit-src`).

## 4. Tipografia e cor

- Até 3 famílias: display (títulos), texto (frases), mono (rótulos, fontes, timecode). Fontes locais (pacotes `@fontsource` ou arquivos), carregadas com `@remotion/fonts`.
- Cada estilo pode ter paleta própria, mas o **acento** (uma cor de sinal) atravessa o vídeo — ele é o bastão visual.
- Perfil de marca, se houver, substitui famílias e paletas.

## 5. Legendas

- Fala real → transcrição local (`assets/kit-scripts/transcribe.mjs` → `words.py` → `make_edl.py`): grupos de até 7 palavras, quebra em `.?!`, palavra a palavra.
- Posição: fora de rostos e de grafismos do material (crachás, marcas d'água); suba a legenda só enquanto houver conflito.
- Texto cinético na tela = **verbatim** da fala.

## 6. Áudio

- Trilha: sintetizada em código (`assets/kit-scripts/score.py`, um bloco por seção) ou faixa licenciada. Silencie/abaixe sob fala real.
- Alvos no MP4 exportado: **−16 LUFS** (redes) ou **−18/−19** (apresentação), pico ≤ **−1 dBFS** (prefira −2 para o AAC). Meça com `measure.py`; ajuste o *drive* do limitador, não o volume final no escuro.
- SFX: um por evento, pelo pico; para biblioteca CC0 e mix medido, rode o skill `sound-effects`.

## 6b. Nivelamento entre cenas (aprendido no vídeo de 8 min)

- Meça LUFS **por cena** (`assets/kit2/scripts/measure_scenes.py`). Sem nivelamento, cenas calmas ficaram 15 dB abaixo das energéticas.
- Na trilha: suba cenas calmas até ~4 dB abaixo das energéticas (rampas de 0,4 s); fala real fica com música ×0,3.
- Alvo: LRA ≤ 6 LU; total −18/−19 LUFS (YouTube) ou −16 (Reels). Pico final com `alimiter` de master sem re-render (ver KIT2.md).

## 6c. Determinismo de texto em canvas

- Qualquer texto/máscara desenhado em `<canvas>` (LED, areia, mosaico, pixel, mapa) espera `useFonts()` — senão processos de render paralelos podem usar fontes diferentes.

## 7. QA obrigatório

- `ffprobe`: duração, fps, frames, áudio presente.
- `measure.py`: LUFS total e por trecho, pico, Δ de sincronia dos eventos-chave (≤ 1 frame).
- Stills em lote com um bundle só (`assets/kit2/scripts/stills.mjs`) + folhas de contato; depois frames extraídos **do MP4** em cada tipo de passagem e no meio de cada trecho; olhe todos.
- Margens: nada importante fora de 96 px (1080p) ou das safe zones da plataforma (vertical).
- Diga o que não foi verificado (ex.: você não ouviu).
