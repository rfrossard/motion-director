# Mapa e terreno cinematográfico (`geomap`)

**Look**: globo ou terreno com relevo real visto de cima e em ângulo baixo, céu dramático, névoa, rotas que se desenham, marcadores e formações em movimento, rótulos discretos. "Filme que por acaso é renderizado em código", não infográfico.
**Usos**: viagens, rotas, história e batalhas, expansão de empresas, "onde fica", logística, clima.
**Exemplos**: "Battle of Austerlitz as a 5-minute film" (@WinterArc2125, 1.042 salvos, 394 mil views — terreno de satélite real e nascer do sol no lugar certo), "Battle of Dan-no-ura as a 3D TV special" (@tetumemo).

## Fontes de dados (grátis, conferir licença)
- Elevação: tiles Terrarium/AWS Terrain (Mapzen, domínio público em grande parte), SRTM/Copernicus DEM (NASA/ESA).
- Vetores: Natural Earth (domínio público) para países, rios e cidades; OpenStreetMap (ODbL, atribuição obrigatória).
- Imagem de satélite: só com licença clara (ex.: Sentinel-2, Copernicus — atribuição). Evite tiles comerciais.

## Técnica
- **2D estilizado** (rápido): projeção d3-geo (`geoOrthographic` para globo, `geoMercator` para região) em SVG/Canvas, hillshade pré-calculado de um DEM em PNG, câmera = escala + translate com easing exponencial (zoom de continente → cidade).
- **3D** (cinematográfico): Three.js com plano subdividido deslocado pelo DEM (heightmap em textura), luz direcional na posição real do sol (calcule azimute/elevação para data/hora/lugar), névoa exponencial, câmera em spline.
```js
// zoom de globo até um ponto a velocidade perceptual constante
const z = Math.exp(lerp(Math.log(z0), Math.log(z1), ease(k)));
// rota que se desenha: path SVG com pathLength=1 e strokeDashoffset = 1 - p
```
- Marcadores/formações: instâncias (InstancedMesh) movidas por dados de tempo; rótulos em HTML sobre a projeção.

## Armadilhas
- Atribua todas as fontes de dados na tela (pequeno) e no `CREDITS.md`.
- Não use fronteiras contestadas sem cuidado; em história, use as fronteiras da época ou deixe esquemático.
- DEMs grandes travam: recorte e reduza resolução antes.

## Bastões
Zoom do globo até o ponto (entra) / do ponto ao globo (sai); a rota vira uma linha que segue para o próximo estilo.

## Prompt-semente
"Filme cinematográfico em código sobre <tema/lugar>: terreno com relevo real (DEM público), luz do sol na posição real para <data/hora>, névoa, câmera aérea em spline, rotas que se desenham, poucos rótulos. Não deve parecer infográfico. Cite as fontes de dados."

**Status**: testado no vídeo "Biblioteca de estilos" (08/11/2026). Código: `assets/kit2/src/b/ch4.tsx` · cena `GeomapS`.

**Lições do teste**: globo d3-geo (world-atlas 110m) → arco → mergulho → terreno real (tiles Terrarium da AWS, hillshade calculado no canvas) com inclinação CSS; rótulos com deslocamento por lugar.

**Auditoria (09/11/2026)** (composição / ofício / movimento / legibilidade / fidelidade): 4,5 / 4,5 / 4,5 / 4 / 4,5. Passa.
