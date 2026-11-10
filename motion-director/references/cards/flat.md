# Flat científico Kurzgesagt-like (`flat`)

**Look**: ilustração vetorial plana, fundo profundo saturado com gradiente, cel shading (sombra recortada), luz de borda, glow, partículas em 3 camadas, mascotes geométricos, granulação + vinheta, zoom de escala contínuo.
**Usos**: ciência, mecanismos, escala, "como funciona".
**Executor**: skill `flat-science-explainer` (guia de estilo e paletas). **Cena de ouro**: `kit2/src/b/v3.tsx` · `FlatV3` (paleta Ártico).

## Como a cena de ouro funciona
- Abrir com zoom extremo (16×) num detalhe (um pixel do frame) e recuar continuamente até revelar o mundo inteiro.
- Uma cena-mundo: relógio-planeta (tempo) → cano com pulsos → máquina f(t) com engrenagens e vapor → esteira de frames. Cada frame mostra um passo da animação.
- Mascotes em pílula com olhos (piscar, respirar, olhar seguindo a ação).
- Rótulos em caixa alta com linha-guia e bolinha; título só depois do recuo.

## Lições e armadilhas
- Três bolinhas num fundo vazio foi a falha da v1 (nota 2,5).
- Zoom exponencial com alvo interpolado pelo mesmo easing perde o objeto: use `kc = (Z/z − 1)/(Z − 1)`.
- Rótulos no mundo podem colidir com o título fixo na tela; confira o recuo final.

**Status**: aprovada no portão de qualidade (09/11/2026), ≥ 2 rodadas de crítica contra referência. Traços obrigatórios em `references/quality.md` §1.
