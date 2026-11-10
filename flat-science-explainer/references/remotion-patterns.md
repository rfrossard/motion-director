# Padrões de Remotion para o estilo flat science

Confira as APIs na versão instalada (`node_modules/remotion/package.json` e remotion.dev/docs) antes de usar. Todas as animações derivam de `useCurrentFrame()`. A aleatoriedade usa `random(seed)` do pacote `remotion`, nunca `Math.random()`.

Organize os componentes em `components/flat/` dentro do projeto do studio, e os temas em `themes/flat-<paleta>.ts`.

## Tema

```ts
// themes/flat-nebulosa.ts
export const nebulosa = {
  bgTop: '#1A1446', bgBottom: '#0C0A26', mid: '#4B2C8F',
  accent: '#FF4F8B', accent2: '#FFC23D', light: '#F4EEFF', character: '#7FE3FF',
} as const;
export type FlatTheme = typeof nebulosa;
```

## Utilitário de tons (base → sombra e luz)

```ts
// components/flat/shade.ts — HSL simples, sem dependências
const hexToHsl = (hex: string) => {
  const n = parseInt(hex.slice(1), 16);
  const r = ((n >> 16) & 255) / 255, g = ((n >> 8) & 255) / 255, b = (n & 255) / 255;
  const max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2;
  if (max === min) return { h: 0, s: 0, l };
  const d = max - min, s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
  const h = max === r ? (g - b) / d + (g < b ? 6 : 0) : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return { h: h * 60, s, l };
};
const hsl = (h: number, s: number, l: number) =>
  `hsl(${(h + 360) % 360} ${Math.round(s * 100)}% ${Math.round(Math.min(1, Math.max(0, l)) * 100)}%)`;
export const shadow = (hex: string) => { const c = hexToHsl(hex); return hsl(c.h + 8, c.s, c.l - 0.18); };
export const highlight = (hex: string) => { const c = hexToHsl(hex); return hsl(c.h, c.s, c.l + 0.15); };
```

## Círculo com sombra cel, brilho e glow

```tsx
// components/flat/ShadedCircle.tsx
import { useId } from 'react';
import { shadow, highlight } from './shade';

export const ShadedCircle: React.FC<{ cx: number; cy: number; r: number; color: string; glow?: string }> =
  ({ cx, cy, r, color, glow }) => {
  const id = useId().replace(/:/g, '');
  return (
    <g>
      <defs>
        <clipPath id={`c${id}`}><circle cx={cx} cy={cy} r={r} /></clipPath>
        {glow && (
          <radialGradient id={`g${id}`}>
            <stop offset="0%" stopColor={glow} stopOpacity={0.5} />
            <stop offset="100%" stopColor={glow} stopOpacity={0} />
          </radialGradient>
        )}
      </defs>
      {glow && <circle cx={cx} cy={cy} r={r * 2.6} fill={`url(#g${id})`} style={{ mixBlendMode: 'screen' }} />}
      <circle cx={cx} cy={cy} r={r} fill={color} />
      <circle cx={cx + r * 0.28} cy={cy + r * 0.28} r={r} fill={shadow(color)} clipPath={`url(#c${id})`} />
      <ellipse cx={cx - r * 0.38} cy={cy - r * 0.42} rx={r * 0.18} ry={r * 0.12} fill={highlight(color)} opacity={0.9} />
    </g>
  );
};
```

## Flutuação, respiração e piscar

```tsx
// components/flat/motion.ts
import { random } from 'remotion';
export const float = (frame: number, seed: string, amp = 8, periodS = 4, fps = 30) => {
  const phase = random(seed) * Math.PI * 2;
  return Math.sin((frame / (periodS * fps)) * Math.PI * 2 + phase) * amp;
};
export const breathe = (frame: number, fps = 30) => 1 + Math.sin((frame / (3.5 * fps)) * Math.PI * 2) * 0.015;
// openness: 1 = aberto, 0 = fechado; pisca por ~4 frames a cada `every` frames
export const blink = (frame: number, seed: string, every = 120) => {
  const offset = Math.floor(random(seed) * every);
  const t = (frame + offset) % every;
  return t < 4 ? Math.abs(t - 2) / 2 : 1;
};
```

## Entrada com spring, squash e stretch

```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';
const PopIn: React.FC<{ delay?: number; children: React.ReactNode }> = ({ delay = 0, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - delay, fps, config: { damping: 12, mass: 0.8 } });
  const v = spring({ frame: frame - delay, fps, config: { damping: 8 } }); // oscila mais
  const squash = 1 + (v - s) * 0.4;  // estica e achata em torno do valor final
  return <g style={{ transform: `scale(${s / squash}, ${s * squash})`, transformBox: 'fill-box', transformOrigin: 'center bottom' }}>{children}</g>;
};
```

## Campo de estrelas em 3 camadas (com parallax)

```tsx
import { random, useCurrentFrame, useVideoConfig } from 'remotion';
export const Starfield: React.FC<{ count?: number; color: string; camX?: number }> = ({ count = 160, color, camX = 0 }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const layers = [0.15, 0.5, 1];
  return (
    <svg width={width} height={height} style={{ position: 'absolute' }}>
      {Array.from({ length: count }).map((_, i) => {
        const L = layers[i % 3];
        const x = (((random(`sx${i}`) * width - camX * L) % width) + width) % width;
        const y = random(`sy${i}`) * height;
        const r = (0.6 + random(`sr${i}`) * 1.6) * (0.5 + L);
        const tw = 0.5 + 0.5 * Math.sin(frame / (20 + random(`st${i}`) * 40) + i);
        return <circle key={i} cx={x} cy={y} r={r} fill={color} opacity={(0.25 + 0.6 * tw) * (0.4 + 0.6 * L)} />;
      })}
    </svg>
  );
};
```

## Zoom de escala contínuo

Ponha cada escala (célula, órgão, corpo, cidade, planeta…) aninhada num `<g>` com o fator da escala anterior. Um único `scale` exponencial percorre todas sem cortes.

```tsx
const frame = useCurrentFrame();
const k = 6;                        // fator entre níveis
const t = interpolate(frame, [0, 240], [0, 3], { easing: Easing.inOut(Easing.cubic), extrapolateRight: 'clamp' });
const zoom = Math.pow(k, t);        // 1 → 216
// <g transform={`translate(${W/2} ${H/2}) scale(${zoom})`}>
//   <Level0 />  <g transform={`scale(${1/k})`}><Level1 /> <g transform={`scale(${1/k})`}><Level2/>…</g></g>
// </g>
```

Esconda (opacity → 0) os níveis com tamanho efetivo menor que ~1 px ou maior que ~20× a tela, para não pesar o render.

## Granulação e vinheta (overlay final)

```tsx
export const Grain: React.FC<{ opacity?: number }> = ({ opacity = 0.06 }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ mixBlendMode: 'overlay', opacity, pointerEvents: 'none' }}>
      <svg width="100%" height="100%">
        <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={frame % 8} /></filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  );
};
export const Vignette = () => (
  <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.32) 100%)', pointerEvents: 'none' }} />
);
```

Um `seed` que varia de 0 a 7 dá uma granulação "viva" e ainda determinística.

## Fundo com gradiente

```tsx
<AbsoluteFill style={{ background: `linear-gradient(180deg, ${theme.bgTop}, ${theme.bgBottom})` }} />
```

## Ordem das camadas de uma cena

`Fundo` → `Starfield/poeira (fundo)` → `cenário de trás (menos contraste)` → `objeto principal + glow` → `personagens` → `partículas da frente` → `rótulos/texto` → `legendas` → `Vignette` → `Grain`.

## Performance

- Muitos `filter: blur` por frame deixam o render lento. Prefira `radialGradient` para glows.
- Para mais de 500 partículas, desenhe em `<canvas>` dentro de um componente que redesenha a partir de `frame`, mantendo o render determinístico.
- Renderize stills (`npx remotion still`) de cada cena antes do vídeo completo.
