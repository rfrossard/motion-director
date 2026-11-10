# Toon 3D de game (`toon3d`)

**Look**: objeto 3D real (espessura, chanfros, detalhes geométricos) com toon shading de 3–4 degraus, contorno por pós-processo (normal + profundidade), cores saturadas que **sobem de nível** (comum verde → raro azul → épico roxo → lendário dourado), títulos com fonte arredondada e grossa batendo letra a letra.
**Usos**: conquistas, marcos, aniversários, "desbloqueou", gamificação, unboxings, celebrações.
**Exemplo**: "Mobile game reward animation template" (@op7418, 899 salvos — Three.js + GSAP + Web Audio).

## Estrutura (5 estágios)
1. **Pronto**: objeto flutua, gira de leve, treme a cada poucos segundos ("me clica").
2. **Sobe de nível** (cada clique/beat): pula, gira no ar, achata ao pousar; troca cor principal, cor do brilho e fundo.
3. **Abre**: partes móveis de verdade (tampa na dobradiça, medalha gira no eixo).
4. **Recompensa**: explosão de partículas na cor do nível, raios de fundo, título.
5. **Fecha**: segura 1,5 s com respiração.

## Técnica (Three.js)
- `MeshToonMaterial` com `gradientMap` de 3–4 tons (`NearestFilter`). Três luzes: key, sky, rim na cor do nível.
- Contorno: render de normais + profundidade e shader de bordas (grosso na silhueta, fino nas junções). **Não** use o truque de backface escalado (espessura irregular).
- Supersampling 1,5× + MSAA. Sombra suave no chão que muda com a altura.
- Sons: Web Audio — "whoosh" no pulo, "thump" no pouso, arpejo ascendente por nível, acorde de fanfarra na recompensa.

## Armadilhas
- Arte original; nada de personagens, IP ou logos de jogos existentes.
- Detalhes (tábuas, rebites) como geometria, não linhas pintadas.
- Limiar de profundidade frouxo, bordas guiadas por normais — senão aparecem riscos em superfícies inclinadas.

## Bastões
A explosão de partículas inunda a tela na cor do nível (sai); o objeto cai do alto e quica (entra).

## Prompt-semente
"Animação original de 'momento de recompensa' de jogo mobile: <assunto>. Objeto 3D real em Three.js com toon shading de 3–4 tons, contorno por pós-processo, cores que sobem de nível <escala>, cinco estágios (pronto, sobe de nível, abre, recompensa, fecha), títulos que batem letra a letra, sons em Web Audio."

**Status**: v3 (09/11/2026), aprovada em 2 rodadas de crítica contra referências. Código: `assets/kit2/src/b/v3.tsx` (cena `Toon3DV3`).

**Lições do teste**: v1 era um baú de caixas com toon shading chapado. v3, contra a referência de game show: `ExtrudeGeometry` com bevel (cantos arredondados), tampa em meio-cilindro, ferragens metálicas por tier, rebites, luz interna (pointLight) e feixe; letreiro com 4 camadas (extrusão, contorno escuro, contorno branco, gradiente com corte duro); barra de progresso 27/27; squash no toque.
