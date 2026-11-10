# Quadro branco e lápis (`sketch`)

**Look**: duas variantes do "feito à mão":
- **Quadro branco**: fundo branco levemente sujo, marcador preto + 1–2 cores, traço com tremor, uma **mão segurando o marcador** que desenha cada elemento; apagador entre cenas.
- **Lápis**: papel com grão, grafite com variação de pressão, hachuras, leve aberração cromática e "shimmer" (o traço vibra 1 px a cada 3 frames, como animação desenhada à mão).
**Usos**: tutoriais, resumos de livros/papers, explicações para leigos, data stories à mão, aulas.
**Exemplos**: "Whiteboard explainer of replica symmetry breaking" (@tak3sh8), "Japan's 2026 heat as a pencil-drawn data story" (@GroundControl), "Hand-drawn photosynthesis lesson for kids" (@rainwishyt), "Whiteboard tutorial for the Lemo-Opuscar skill" (@lemomo_ai).

## Técnica (Remotion/SVG)
```tsx
// traço à mão: path com tremor determinístico + desenho por strokeDashoffset
const wobble = (d: string, seed: string, amp = 1.6) => /* reamostra o path a cada 6 px e desloca normal por noise(seed, i) * amp */;
<path d={wobble(d, id)} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p}
      stroke="#1a1a1a" strokeWidth={4} strokeLinecap="round" fill="none" />
// "boil" (lápis): troque a seed do tremor a cada 3 frames: seed = `${id}-${Math.floor(frame / 3)}`
// mão: PNG/SVG de mão com marcador cuja ponta segue o ponto atual do path (getPointAtLength(p * L))
```
- Letras escritas à mão: fonte manuscrita OFL (ex.: "Caveat", "Patrick Hand", "Gochi Hand") revelada por máscara da esquerda para a direita, na velocidade de escrita (~12 caracteres/s).
- Hachuras: linhas paralelas com tremor, recortadas pela forma.
- Dados (variante lápis): eixos e barras desenhados com tremor; valores reais com fonte citada no rodapé.

## Armadilhas
- A mão não pode tapar o que está sendo explicado; desenhe da esquerda para a direita, de cima para baixo.
- Ritmo: a narração conduz; o desenho termina 0,3 s antes da frase seguinte.
- Muito tremor parece erro — amp 1–2 px a 1080p.

## Bastões
O apagador limpa o quadro (sai); a folha vira (passagem para `collage`/`comic`); um círculo desenhado à mão vira o ponto-bastão.

## Prompt-semente
"Explicação em quadro branco (ou lápis) de <tema> para <público>: cada elemento desenhado à mão com tremor leve e uma mão com marcador, letra manuscrita, 1–2 cores de destaque, narração <TTS> conduzindo o ritmo, apagador entre cenas."

**Status**: v2 (09/11/2026) aprovada em 2 rodadas de crítica contra referências da coleção. Código: `assets/kit2/src/b/sketch2.tsx` (cena `SketchV2`) + `assets/kit2/src/b/hand.tsx`.

**Lições do teste**: a v1 (polilinhas com tremor + fonte revelada por máscara + mão desenhada em SVG) ficou abaixo do nível — a v2 usa escrita traço a traço com fonte de traço único e pressão (perfect-freehand), formas e hachuras do rough.js, papel pontilhado, selos numerados, marca-texto em 1 cor + acentos, lápis na ponta do traço e apresentadora Open Peeps apontando. Siga `references/quality.md`.
