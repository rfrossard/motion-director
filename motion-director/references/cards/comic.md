# Quadrinhos — HQ (`comic`)

**Look**: página de HQ com quadros (gutter branco), traço de nanquim com espessura variável, retícula (halftone) nas sombras, balões de fala e de pensamento, onomatopeias grandes, cores chapadas. A câmera viaja de quadro em quadro; dentro de cada quadro, movimento sutil em stop-motion (parallax de camadas, balões que surgem).
**Usos**: humor, histórias, resumir um artigo/livro/paper, tirinhas educativas, "você sabia?".
**Exemplos**: "Stop-motion comic of 'Attention Is All You Need'" (@Jhoni_Ceron), "Comic-book motion graphic from mascot assets" (@madpencil_), "Creepy pizza parlor music video" (cutouts + caneta, @ParanoidAmerica).

## Gramática
- Layout por página: 3–6 quadros de tamanhos diferentes; a leitura guia a câmera (esquerda→direita, cima→baixo).
- Em cada quadro: entra o fundo, depois o personagem (2 desenhos de "assentamento"), depois o balão (pop 0.85→1), depois a onomatopeia.
- Transição entre páginas: virada de página ou a câmera atravessa um quadro (zoom até preencher, que vira a próxima cena).

## Técnica (Remotion/SVG)
```tsx
// retícula: <pattern id="dots" width={8} height={8} patternUnits="userSpaceOnUse"><circle cx={4} cy={4} r={r}/></pattern>
// r varia com a "sombra" (use máscara de luminância) — dá o look impresso
// traço de nanquim: perfect-freehand (getStroke com pressão → polígono), ver InkV3 em kit2/src/b/v3.tsx
// balão: rect com rx alto + cauda (path), texto em fonte de HQ OFL (ex.: "Bangers" para onomatopeia, "Comic Neue" para fala)
// stop-motion: posições quantizadas a 12 desenhos/s + "boil" de 1 px (dropIn() do kit lib.ts)
```

## Armadilhas
- Personagens originais (nada de heróis/estúdios existentes).
- Texto de balão curto (≤ 12 palavras); a narração pode carregar o resto.
- Contraste: preto do nanquim + 3–4 cores chapadas; retícula só nas sombras.

## Bastões
Zoom num quadro até ele virar a tela inteira (sai/entra); a página vira e o verso é o próximo estilo.

## Prompt-semente
"Conte <texto/história> como uma HQ animada de <N> s: páginas com quadros de tamanhos variados, traço de nanquim, retícula nas sombras, balões e onomatopeias, câmera que lê de quadro em quadro, movimento em stop-motion dentro dos quadros, personagens originais."

**Status**: v2 (09/11/2026) aprovada em 2 rodadas de crítica contra referências da coleção. Código: `assets/kit2/src/b/v2.tsx` (cena `ComicV2`).

**Lições do teste**: v1 usava bonecos desenhados em SVG (fracos). v2: personagem Open Peeps consistente em todos os quadros (bustos `Device`, `Explaining`, `Geek`, `PointingUp` com rostos diferentes), moldura de página em retícula, faixa de título, numeração, legenda de quadro, balões elípticos com cauda e onomatopeias com contorno — no padrão das HQs da coleção.
