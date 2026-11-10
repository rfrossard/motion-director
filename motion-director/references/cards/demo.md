# Demo calmo de produto (`demo`)

**Look**: canvas claro e arejado, o app inteiro recriado (chat com checklist laranja + prévia com tabela e botão), filmado de perto com push-in, deslizes e leve blur de movimento.
**Usos**: walkthroughs, lançamentos de feature, tutoriais curtos.
**Executor**: skill `explainer-default`. **Cena de ouro**: `kit2/src/b/v2.tsx` · `DemoV2`.

## Como a cena de ouro funciona
- Abrir a 2× no campo de prompt, seguir a digitação, deslizar até a prévia e recuar.
- Checklist que marca um passo por vez; linhas da tabela entram em cascata; clique no botão (escala 0,95) e barra de progresso até "pronto ✓".

## Lições e armadilhas
- Na v1, a tela ficou quase vazia (nota 3): recrie a UI inteira com conteúdo realista.
- Blur de movimento só quando a câmera anda rápido.

**Status**: aprovada no portão de qualidade (09/11/2026), ≥ 2 rodadas de crítica contra referência. Traços obrigatórios em `references/quality.md` §1.
