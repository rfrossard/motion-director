# Traço preciso / desenho técnico (`stroke`)

**Look**: linhas finas sobre preto (estilo 03 do Hub), grade sutil, ícones em linha, numeração mono, cotas de engenharia, laço de revisão em laranja.
**Usos**: papers, arquitetura, fluxos, "como o sistema funciona".
**Executor**: kit 2. **Cena de ouro**: `kit2/src/b/v3.tsx` · `StrokeV3`.

## Como a cena de ouro funciona
- Câmera a 1,75× que percorre os nós enquanto o traço desenha (círculo → ícone → seta), com um ponto laranja liderando a pena.
- Recuo para 1× só depois que todos os nós estão desenhados; então entram notas, cota de ponta a ponta e laço com ponto viajante.

## Lições e armadilhas
- Caixinhas pequenas num mar preto foi a falha da v1 (nota 3): use ícones de verdade e câmera perto.
- Ícones em `SL` (pathLength=1 + dashoffset) desenham na ordem do path; escreva os paths na ordem em que uma mão desenharia.

**Status**: aprovada no portão de qualidade (09/11/2026), ≥ 2 rodadas de crítica contra referência. Traços obrigatórios em `references/quality.md` §1.
