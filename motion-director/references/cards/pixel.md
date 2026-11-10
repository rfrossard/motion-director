# Pixel art 16-bit (`pixel`)

**Look**: sprites e cenários desenhados num canvas lógico pequeno e escalados por fator inteiro, sem suavização. Paleta fixa (24–32 cores), dithering ordenado nos gradientes, contorno de 1 px, luz de 1 px no topo/esquerda e sombra na base/direita.
**Usos**: loops lofi, cenas de game, personagens, aberturas nostálgicas, cartões.
**Exemplos**: "Pixel art wizard casting a spell" (@majidmanzarpour, 2,6 mil salvos), "Pixel-art Paris night diorama lofi loop" (@minosdevs), "Pixel character dodging meteors" (@riku720720).

## Gramática de movimento
- Anima a 8–12 desenhos/s mesmo a 30/60 fps: interpole parâmetros (pose, posição) e **quantize** para a grade a cada frame.
- Squash & stretch só de 1–2 pixels inteiros. Tremor de câmera de 1–2 px em impactos.
- Máquina de estados para personagens (IDLE → CHARGE → ACTION → RECOVER). Partículas em pool, trocando índice de paleta até sumir.
- Dioramas: camadas de trás para frente, parallax por camada em pixels inteiros, tudo função de `t mod D` para loop perfeito.

## Técnica (Remotion ou HTML)
```tsx
// canvas lógico 320x180 → escala 6 = 1920x1080
const LW = 320, LH = 180, S = 6;
const PAL = ['#0b0b1e','#1b1b3a','#2e2a5e', /* … 24–32 cores … */];
useLayoutEffect(() => {
  const g = low.getContext('2d')!; g.imageSmoothingEnabled = false;
  g.fillStyle = PAL[0]; g.fillRect(0, 0, LW, LH);
  const t = Math.floor((frame / fps) * 12) / 12;        // 12 desenhos/s
  drawScene(g, t);                                       // só fillRect em coordenadas inteiras
  const out = ref.current!.getContext('2d')!; out.imageSmoothingEnabled = false;
  out.drawImage(low, 0, 0, LW * S, LH * S);
}, [frame]);
// CSS do canvas final: image-rendering: pixelated
// dithering ordenado (Bayer 4x4) para céus: if (k > BAYER[y%4][x%4]/16) cor A senão cor B
```

## Passos
1. Defina canvas lógico, paleta e lista de sprites (tamanho em células).
2. Desenhe sprites proceduralmente (runs de pixels) ou a partir de matrizes de string.
3. Parametrize poses; anime parâmetros; quantize.
4. Fundo com dithering; luzes com halos pré-renderizados em sprites.
5. Loop: frequências inteiras sobre `D` segundos.

## Armadilhas
- Nada de `shadowBlur`, gradiente, rotação livre ou coordenada fracionária — quebra o pixel.
- Fonte de texto: bitmap font própria (5x7) ou uma pixel font OFL (ex.: "Press Start 2P", "Silkscreen").
- Escala sempre inteira; letterbox com a cor 0 da paleta.

## Bastões
Entra: a cena "pixeliza" (reduza a resolução lógica em degraus 1920→480→240→LW). Sai: um sprite cruza a borda; ou um bloco de cor da paleta cresce e inunda.

## Prompt-semente
"Pixel art 16-bit de <cena>, canvas lógico 320×180 escalado ×6 sem suavização, paleta fixa de 28 cores, dithering ordenado no céu, animação a 12 desenhos/s com poses quantizadas, loop perfeito de <D> s, sem gradientes nem blur."

**Status**: testado no vídeo "Biblioteca de estilos" (08/11/2026). Código: `assets/kit2/src/b/ch6.tsx` · cena `PixelS`.

**Lições do teste**: canvas lógico 320×180 ×6, dithering Bayer, 12 desenhos/s; texto em canvas exige `useFonts()`.

**Auditoria (09/11/2026)** (composição / ofício / movimento / legibilidade / fidelidade): 3,5 / 3,5 / 4 / 4 / 4. **Não passa.** A cena é quase estática e a figura na janela é translúcida. Antes de usar: personagem em sprite com animação de ciclo (gato, pessoa sentada ao PC), parallax de 3 camadas na janela, chuva/neve e luz piscando, e uma ação no beat. Faça 2 rodadas de crítica.
