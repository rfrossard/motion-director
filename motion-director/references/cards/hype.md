# Anúncio no beat com HUD (`hype`)

**Look**: tipografia cinética pesada, cortes no beat (120 BPM = 15 frames/batida), **uma forma que atravessa todos os cortes**, HUD de visor (cantos, CENA 0X/05, rótulo, timecode com ponto vermelho), paleta tinta/acento/creme/azul elétrico.
**Usos**: Reels, Shorts, teasers, lançamentos, CTA.
**Executor**: skill `explainer-high-energy`. **Cena de ouro**: `kit2/src/b/v3.tsx` · `HypeV3` (9:16).

## Como a cena de ouro funciona
- Faísca → linha que vira o sublinhado do slam.
- Slam com máscaras por letra a 1/16 de beat (~4 frames); o ponto final se solta e inunda a tela com a cor da próxima cena.
- Trio cinético, 2 beats por palavra, cada uma com tratamento próprio: tinta sobre laranja; laranja sobre preto com a palavra repetida em contorno preenchendo o quadro; branco sobre azul elétrico dentro de cantos de visor com rótulo `1080 × 1920`; palavra manuscrita que se escreve (`Written`).
- Visual-assinatura: partículas em fluxo → anel → explosão. Flash ≤ 6 frames, colorido.
- Fim: ponto → anel pulsando → marca com o ponto como pontuação.

## Lições e armadilhas
- Cartões de texto soltos sem forma de ligação foram a falha da v1 (nota 3).
- Explosão curta demais deixa frames vazios. Use ≥ 30 frames de easing e opacidade quadrática.
- Flash branco sobre fundo escuro vira cinza no frame; use a cor de acento com opacidade ≤ 0,55.

**Status**: aprovada no portão de qualidade (09/11/2026), ≥ 2 rodadas de crítica contra referência. Traços obrigatórios em `references/quality.md` §1.
