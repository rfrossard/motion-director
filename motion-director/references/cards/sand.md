# Animação em areia (`sand`)

**Look**: mesa de luz quente (âmbar/creme) com areia escura; figuras são vazios e acúmulos de grãos; a cena seguinte nasce de um gesto que varre, arrasta ou peneira a areia. Textura granular, bordas macias, nada sólido.
**Usos**: histórias emotivas, homenagens, retrospectivas, história de famílias/cidades/empresas.
**Exemplos**: "Sand animation of 250 years of US history" (@Michaelzsguo, 353 salvos, 71 mil views), "Sand animation of 100 years of Hong Kong" (@harryworld).

## Gramática
- Cada cena é um **desenho de densidade** (onde há areia). A transição é um campo de vetores que move os grãos (varrida circular, arrasto de dedo, peneira caindo).
- Ritmo lento: 6–10 s por cena, transições de 1,5–2,5 s. Sem texto, ou só datas grandes desenhadas na areia.

## Técnica (canvas/WebGL, determinística)
```js
// 1) cada cena = máscara alvo (desenhada em canvas: silhuetas, contornos grossos)
// 2) grãos: N=120k partículas com posição; a cada frame calculamos a posição como função de t:
//    pos(t) = lerp(posCenaA[i], posCenaB[i], ease(k)) + ruído(seed i, t) * (1 - |2k-1|) * amp
//    (atribuição A→B pareando grãos por ordem de varredura espacial — Hilbert/Z-order — para movimento orgânico)
// 3) render: cada grão como ponto escuro alpha 0.35 sobre fundo de luz radial; acumular gera densidade
// 4) "dedo": máscara circular que empurra grãos para fora em frames de gesto
```
- Para 1080p, renderize a 960×540 com pontos de 1 px e escale ×2 com leve blur (0,6 px) — parece areia real.
- Desenhos-alvo: gere silhuetas simples (pessoas de perfil, prédios, barcos, árvores) com paths SVG rasterizados.

## Armadilhas
- Determinismo: posições como função de t (não simulação acumulada); se usar simulação, pré-calcule ("bake") e leia por frame.
- Muitos detalhes finos somem na areia — prefira silhuetas grandes e legíveis.
- Música: piano/cordas suaves; foley de areia (ruído filtrado em fade).

## Bastões
A mão varre a areia e revela a luz da mesa (tela clara → próximo estilo); ou os grãos convergem numa forma (ponto/círculo).

## Prompt-semente
"Animação em areia de <N> minutos contando <história>: mesa de luz quente, figuras como silhuetas em areia, cada cena nasce de um gesto de varrer/arrastar, ritmo lento, música suave e foley de areia, quase sem texto."

**Status**: testado no vídeo "Biblioteca de estilos" (08/11/2026). Código: `assets/kit2/src/b/ch6.tsx` · cena `SandS`.

**Lições do teste**: 42 mil grãos em 960×540 escalado ×2 com blur 0,6 px; cenas = máscaras desenhadas em canvas, grãos pareados por ordem espacial; `useFonts()` para máscaras de texto.

**Auditoria (09/11/2026)** (composição / ofício / movimento / legibilidade / fidelidade): 4,5 / 4,5 / 4 / 4 / 4,5. Passa.
