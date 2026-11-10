# Mosaico de vidro e ouro (`mosaic`)

**Look**: parede de mosaico (pastilhas de vidro colorido e folha de ouro) cujas peças "nunca foram coladas": levantam, viram, voam em bando e voltam ao lugar com um clique. Figuras são **bandos de pastilhas** (um peixe nada porque suas pastilhas nadam). Brilho especular no ouro, leve irregularidade no rejunte.
**Usos**: aberturas artísticas, cartões, vídeos contemplativos, vinhetas de marca, "a peça que faltava".
**Exemplo**: "Glass and gold mosaic that comes alive" (@LCSlates, 867 salvos — 80 s, quadrado, WebGL2 puro, som sintetizado no navegador).

## Técnica (WebGL2 instanciado)
- Grade de pastilhas (ex.: 96×96 = 9.216 instâncias). Cada pastilha: posição de repouso, cor (paleta de vidro + ouro), normal levemente aleatória.
- Estado por pastilha como **função do tempo**: `rest → lift (z sobe, gira) → flock (segue uma curva-alvo da figura) → return (mola até rest)`. Atribua pastilhas a figuras pela proximidade da silhueta-alvo.
- Shader: Blinn-Phong com mapa de ambiente simples; ouro com especular alto e cor quente; vidro com leve transmissão (cor + fresnel).
- Som: cada pastilha que volta = clique curto (ruído filtrado + ressonância), com densidade controlada (máx. N cliques por frame, agrupados).
```glsl
// vertex: pos = mix(restPos, flockPos(t, id), lift(t, id)); rot = flip(t, id)
```

## Armadilhas
- Instancing obrigatório (milhares de draw calls travam).
- Leitura: figuras precisam de silhueta forte e poucas cores; o fundo volta a ser "parede" entre atos.
- Determinismo: cada pastilha com seed própria; nada de `Math.random` por frame.

## Bastões
As pastilhas se juntam no formato do próximo objeto (logo, ponto, retângulo) e "assentam"; ou a parede inteira se desfaz em bando para a próxima cena.

## Prompt-semente
"Filme de <N> s, quadrado, num único HTML com WebGL2 e JS puro, sem arquivos externos: um mosaico de vidro e folha de ouro cujas pastilhas nunca foram coladas — levantam, viram, voam em bando formando <figuras> e voltam ao lugar com um clique. Som sintetizado no navegador."

**Status**: testado no vídeo "Biblioteca de estilos" (08/11/2026). Código: `assets/kit2/src/b/ch6.tsx` · cena `MosaicS`.

**Lições do teste**: canvas 2D (64×36 pastilhas) foi suficiente — WebGL não foi necessário; pastilhas sorteadas voam em arco e viram (lado dourado) para formar texto.

**Auditoria (09/11/2026)** (composição / ofício / movimento / legibilidade / fidelidade): 4,5 / 4,5 / 4 / 4 / 4,5. Passa.
