# Data story editorial (`datastory`)

**Look**: página de caderno/revista: papel com textura e cruzetas nos cantos, cabeçalho de edição em mono, manchete em itálico serifado, número-herói grande à mão em cor, gráfico hachurado, carimbo, anotação à mão com seta, fonte citada.
**Usos**: artigos, relatórios, um número ou uma comparação.
**Executor**: kit 2. **Cena de ouro**: `kit2/src/b/v3.tsx` · `DataV3`.

## Como a cena de ouro funciona
- Número-herói conta de 0 até o valor.
- Colunas hachuradas (pattern 45°) que crescem com mola em cascata; destaque com hachura colorida e contorno grosso.
- Linha de referência tracejada com anotação manuscrita (Caveat) acima dos valores e seta curva.
- Carimbo de borda dupla que bate com escala 1,6 → 1.

## Lições e armadilhas
- Na v1, gráfico pequeno e rótulos de 20 px ficaram ilegíveis (nota 3). Rótulos de gráfico: 22–24 px.
- Use espaço não separável em "8 s" para não quebrar a linha.
- Reserve a área do cartão de invocação (pos `left`, topo 600) antes de diagramar.

**Status**: aprovada no portão de qualidade (09/11/2026), ≥ 2 rodadas de crítica contra referência. Traços obrigatórios em `references/quality.md` §1.
