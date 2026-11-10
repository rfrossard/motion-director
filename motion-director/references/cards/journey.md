# Jornada em take único (`journey`)

**Look**: fundo grafite pontilhado, um herói (bola branca com halo e rastro) que salta entre estações, e estações que são cartões de UI realistas reagindo à chegada. Câmera perto (~1,5×) e recuo para revelar o caminho.
**Usos**: processos, pipelines, "do pedido ao resultado".
**Executor**: skill `explainer-engaging`. **Cena de ouro**: `kit2/src/b/v2.tsx` · `JourneyV2`.

## Como a cena de ouro funciona
- Cartões com conteúdo de verdade: checklist com toggles laranja, chips de seleção, barra de render com contador de frames, verificação com ✓.
- Pulso de escala ao pousar; recuo final mostra a trilha pontilhada ligando tudo.

## Lições e armadilhas
- Na v1, elementos minúsculos num fundo escuro (nota 3).
- A câmera mira abaixo da bola (o cartão), não a bola.

**Status**: aprovada no portão de qualidade (09/11/2026), ≥ 2 rodadas de crítica contra referência. Traços obrigatórios em `references/quality.md` §1.
