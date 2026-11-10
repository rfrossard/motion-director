# Constelação de partículas (`particles`)

**Look**: a cena inteira é feita de milhares de pontos luminosos (sem preenchimentos sólidos); figuras em movimento deixam **rastros em fita**; profundidade por tamanho/brilho; aditivo sobre fundo escuro. Pode mudar de "hora do dia" mudando a paleta das partículas.
**Usos**: cenários oníricos, cidades e paisagens estilizadas, espaços de dados (embeddings, redes, mapas de calor), cosmos, aberturas.
**Exemplos**: "Particle-illustration Santa Monica beach" (@ishuagra02), "Word-seeded cosmic genesis" (@MiaAI_lab, 747 salvos), "Futuristic particle and kinetic type reel" (@kopert0x).

## Técnica (Three.js Points ou WebGL)
- Amostre superfícies/silhuetas: para cada objeto, gere N pontos sobre a malha (ou sobre um SVG rasterizado para 2,5D) com cor por altura/material.
- `THREE.Points` com `ShaderMaterial` (tamanho por distância, `AdditiveBlending`, `depthWrite: false`), 200k–1M pontos.
- Movimento como função do tempo: `pos = base + curlNoise(base * f + t * s) * amp` (pré-calcule campos se precisar).
- **Morph entre formas**: pareie índices das partículas da forma A e B (ordenadas por eixo ou por Z-order) e interpole com easing + desvio por ruído.
- Rastros: desenhe as últimas K posições (calculadas por t − k·dt, não acumuladas) com alpha decrescente.
- Dados: cada partícula = um registro (ex.: um paper, um usuário); posição de um UMAP/t-SNE pré-calculado; cor por grupo.

## Armadilhas
- Texto pequeno some no brilho; use poucas palavras grandes ou HTML por cima.
- Aditivo estoura em branco: limite brilho por partícula e use tonemapping.
- Render pesado: teste 2 s antes; reduza partículas fora de foco.

## Bastões
As partículas condensam na forma do próximo estilo (ponto, logo, retângulo) ou se dispersam a partir dela.

## Prompt-semente
"Ilustração em partículas de <cena/dados>: milhares de pontos luminosos em vez de preenchimentos, rastros em fita atrás do que se move, profundidade por tamanho e brilho, paleta que muda com <hora/tema>, morph entre <formas>. Three.js, função pura do tempo."

**Status**: testado no vídeo "Biblioteca de estilos" (08/11/2026). Código: `assets/kit2/src/b/ch3.tsx` · cena `ParticlesS`.

**Lições do teste**: 12 mil pontos em canvas com `lighter`; partícula = registro real (cada vídeo da coleção); alpha ≥0,6 senão some.

**Auditoria (09/11/2026)** (composição / ofício / movimento / legibilidade / fidelidade): 4 / 4 / 4 / 4 / 4. Passa depois de subir os rótulos das categorias de 18 para 24 px e os números para 36/48 px.
