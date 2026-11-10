# Nanquim e selo, linha do tempo (`ink`)

**Look**: papel com fibras, pincel de nanquim com pressão variável, respingos, ícones esboçados, horas manuscritas, carimbo vermelho, título à mão.
**Usos**: cronologias, contexto, "como chegamos aqui".
**Executor**: kit 2. **Cena de ouro**: `kit2/src/b/v3.tsx` · `InkV3`.

## Como a cena de ouro funciona
- A linha é um traço de perfect-freehand (`getStroke` com pressão em `[x, y, p]`), desenhado até a ponta; a câmera segue a ponta e recua no fim para mostrar tudo.
- Cada marco entra quando a ponta passa: borrão + respingos, ícone rough, hora (felix) e nota (read, ≥ 46 px no mundo para sobreviver ao recuo).
- Carimbo "AGORA" que bate; título manuscrito depois do recuo.

## Lições e armadilhas
- As fontes EMS não têm º, · nem — (o render falha de propósito); escreva "primeiro", vírgula ou dois-pontos.
- Tapers de início/fim no perfect-freehand com traço parcial geram formas estranhas; use `last: true` sem taper.
- O movimento da ponta deve ser quase linear (0,8·linear + 0,2·ease), senão o começo fica parado.

**Status**: aprovada no portão de qualidade (09/11/2026), ≥ 2 rodadas de crítica contra referência. Traços obrigatórios em `references/quality.md` §1.
