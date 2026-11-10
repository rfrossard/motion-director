# Teatro de sombras (`shadow`)

**Look**: silhuetas pretas recortadas (papel com bordas levemente irregulares, articulações com rebites visíveis, varetas finas) contra uma tela iluminada por trás (gradiente quente âmbar/laranja, vinheta, textura de tecido). Profundidade por desfoque: peças mais longe da tela ficam mais borradas e maiores.
**Usos**: fábulas, histórias pessoais e de família, valores, contos curtos, vídeos verticais delicados.
**Exemplo**: "Shadow puppet film: what makes a home" (@x4b47x — vertical 9:16, áudio feito em código).

## Gramática
- Personagens articulados (2–6 partes) com rotação por junta; andam aos "trancos" (pose a pose, 8 desenhos/s).
- Cenas montadas por camadas que entram deslizando dos lados (como no palco).
- Luz que tremula levemente (vela/lamparina): brilho da tela varia ±3% com ruído suave.
- Texto (se houver) como cartela recortada, curto.

## Técnica (Remotion/SVG)
```tsx
// tela: radial-gradient(ellipse at 50% 45%, #ffcf8a, #e07a2a 60%, #3a1405 100%) + textura de tecido (feTurbulence sutil)
// silhueta: <path fill="#120a06"> com filter blur(dist * 2px) e scale(1 + dist * 0.06) para "longe da tela"
// articulação: <g transform={`rotate(${ang} ${pivotX} ${pivotY})`}> com ang = pose[floor(t*8)] interpolado e quantizado
// varetas: <line> fina e semitransparente do membro até fora do quadro
```

## Armadilhas
- Silhueta precisa ser legível só pelo contorno — perfis, não frentes.
- Evite detalhes internos (são invisíveis em sombra); use recortes vazados (olho, janela) para expressão.
- Som: música suave (kalimba, cordas pizzicato), foley de papel e madeira.

## Bastões
A lamparina apaga (tela escurece → próximo estilo) ou uma silhueta atravessa a tela e "limpa" a cena.

## Prompt-semente
"Teatro de sombras de <30–60> s, <vertical/horizontal>, sobre <tema>: silhuetas de papel recortado com articulações e varetas, tela iluminada por trás em tom quente, profundidade por desfoque, movimento pose a pose, música e foley gerados em código."

**Status**: v3 (09/11/2026), aprovada em 2 rodadas de crítica contra referências. Código: `assets/kit2/src/b/v3.tsx` (cena `ShadowV3`).

**Lições do teste**: v1 usava boneco de palitinho. v3: silhueta Open Peeps de corpo inteiro (`WalkingFilled` → `PointingFingerBW`, `strokeColor`=`backgroundColor`=tinta). As poses de corpo inteiro precisam de viewBox ~1400×2470; com 1500 de altura a figura é cortada na cintura. As camadas de fundo devem ser mais claras que a silhueta (opacidade 0,2–0,45), senão as pernas somem. Moldura de teatro (cortinas e bambinela) e morros com parallax.
