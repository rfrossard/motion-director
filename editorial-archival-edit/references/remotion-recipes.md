# Receitas Remotion para a edição editorial

Confira as APIs na versão instalada. Tudo deriva de `useCurrentFrame()`. A aleatoriedade usa `random(seed)` do `remotion`.

## Estrutura do projeto

```
src/
  Root.tsx            # Composition com fps/size do original (via calculateMetadata + parseMedia/ffprobe)
  Edit.tsx            # monta as camadas na ordem abaixo
  edl.json            # timeline: shots, inserts, type layers, splits (dados, não código)
  look.json           # parâmetros de look.md
  layers/ Grade.tsx Bloom.tsx Grain.tsx Weave.tsx Captions.tsx TypeLayer.tsx Split.tsx BehindText.tsx Insert.tsx
public/source/        # vídeo original, matte (PNG seq ou WebM com alpha), inserts
```

Ordem das camadas: `vídeo graduado` → `bloom` → `inserts` → `texto atrás` → `matte da pessoa` → `texto na frente / legendas` → `vinheta` → `grão`.

## Vídeo original intacto

```tsx
import { OffthreadVideo, staticFile, Sequence } from 'remotion';
// Um <Sequence> por trecho do mapa fonte→programa; trimBefore/startFrom conforme a versão instalada.
<OffthreadVideo src={staticFile('source/raw.mp4')} />
```

Use `OffthreadVideo` para precisão de frame no render. O áudio vem do próprio vídeo; não reencode a fala.

## Grade + bloom

```tsx
const Graded: React.FC<{ children: React.ReactNode; look: Look }> = ({ children, look }) => (
  <AbsoluteFill>
    <AbsoluteFill style={{ filter: `grayscale(1) contrast(${look.contrast}) brightness(${look.exposure})` }}>{children}</AbsoluteFill>
    {/* bloom: cópia isolando altas luzes */}
    <AbsoluteFill style={{ mixBlendMode: 'screen', opacity: look.bloom,
      filter: `grayscale(1) brightness(1.6) contrast(2.2) blur(${look.bloomRadius}px)` }}>{children}</AbsoluteFill>
    {/* lift dos pretos */}
    <AbsoluteFill style={{ background: `rgb(${look.blackLift},${look.blackLift},${look.blackLift})`, mixBlendMode: 'lighten' }} />
  </AbsoluteFill>
);
```

Renderizar o vídeo duas vezes (base e bloom) custa caro. Se ficar lento, faça o bloom só nos inserts e nas palavras grandes, ou pré-processe com `ffmpeg` (`split`, `curves`, `gblur`, `blend=screen`).

## Grão novo a cada frame

```tsx
export const Grain: React.FC<{ opacity: number; freq?: number }> = ({ opacity, freq = 0.95 }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ mixBlendMode: 'overlay', opacity, pointerEvents: 'none' }}>
      <svg width="100%" height="100%">
        <filter id="g"><feTurbulence type="fractalNoise" baseFrequency={freq} numOctaves={2} seed={frame} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" /></filter>
        <rect width="100%" height="100%" filter="url(#g)" />
      </svg>
    </AbsoluteFill>
  );
};
```

## Gate weave e poeira (só nos inserts)

```tsx
const frame = useCurrentFrame();
const wx = (random(`wx${frame}`) - 0.5) * 1.2, wy = (random(`wy${frame}`) - 0.5) * 1.2;
// <div style={{ transform: `translate(${wx}px, ${wy}px)` }}>…insert…</div>
const specks = Array.from({ length: Math.floor(random(`n${frame}`) * 4) }, (_, i) => ({
  x: random(`x${frame}-${i}`), y: random(`y${frame}-${i}`), r: 0.6 + random(`r${frame}-${i}`) * 2.2,
}));
```

## Texto: entrada soft, deriva contínua e stop-motion seletivo

```tsx
const expo = (u: number) => (u >= 1 ? 1 : 1 - Math.pow(2, -10 * u));
const clamp = (x: number) => Math.min(1, Math.max(0, x));

export const TypeLayer: React.FC<{ L: TypeSpec }> = ({ L }) => {
  const frame = useCurrentFrame(); const { fps } = useVideoConfig();
  let t = frame / fps;                                   // tempo de programa absoluto
  if (L.posterize) t = Math.floor(t * L.posterize) / L.posterize;   // stop-motion só nesta camada
  const u = (t - L.t0) / 0.32, e = expo(clamp(u));
  const drift = (t - L.t0) * (L.drift ?? 0.03);          // em/s, atravessa cortes
  if (t < L.t0 || t > L.t1) return null;
  return (
    <div style={{ position: 'absolute', left: L.x, top: L.y, fontSize: L.size,
      transform: `translateY(${(1 - e) * 0.32 + drift}em)`, filter: `blur(${(1 - e) * 9}px)`, opacity: clamp(u * 4.5) }}>
      {renderRuns(L.text) /* *palavra* → serifa itálica */}
    </div>
  );
};
```

As legendas palavra a palavra usam `@remotion/captions` (`createTikTokStyleCaptions` ou equivalente na versão instalada), com cada palavra entrando no seu timestamp.

## Texto atrás da pessoa

1. Gere o matte da pessoa por frame (offline):
   ```bash
   # opção simples (lenta) com rembg — extraia frames, recorte, remonte em WebM com alpha
   ffmpeg -i raw.mp4 -vf fps=<fps_do_original> frames/%05d.png
   rembg p frames/ matte/            # PNG com alpha
   ffmpeg -framerate <fps> -i matte/%05d.png -c:v libvpx-vp9 -pix_fmt yuva420p matte.webm
   ```
   Confira os flags com `rembg --help` na versão instalada. Para vídeos longos, gere o matte só nos trechos onde há texto atrás.
2. Componha nesta ordem: `vídeo` → `texto grande` → `<OffthreadVideo src="matte.webm" transparent />` (o recorte da pessoa, com o mesmo grade) → resto.
3. Revise as bordas do cabelo nos stills. Se ficarem serrilhadas, aplique um leve `blur(0.6px)` no matte.

## Split que desliza com quem apresenta

```tsx
// painel do insert entra empurrando; a pessoa é recortada de novo (object-position), nunca espremida
const p = interpolate(frame, [s.f0, s.f0 + 0.4 * fps], [0, 1], { easing: Easing.inOut(Easing.sin), extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
const insertW = W * s.at;                                  // ex.: 0.5
const insertX = s.side === 'right' ? W - insertW * p : -insertW * (1 - p);
// presenter: <div style={{ position:'absolute', left: s.side==='right'?0:insertX+insertW, width: W-insertW*p, overflow:'hidden' }}>
//   <OffthreadVideo style={{ width: W, height: H, objectFit: 'cover', objectPosition: `${faceX*100}% 50%` }} .../></div>
```

Use `faceX`, a posição horizontal do rosto medida nos frames, para recentralizar quem apresenta no painel.

## Colagem de arquivo

- **Recorte com borda de papel:** a imagem com `clipPath` irregular (polígono com ruído determinístico) sobre uma forma branca um pouco maior e `drop-shadow` suave.
- **Retícula:** um `radial-gradient` repetido em `mix-blend-mode: multiply` sobre o recorte P&B.
- **Entrada stop-motion:** posições quantizadas a 12 fps, uma rotação de −3° a +3° por desenho e 1 px de "boil".

## Testes rápidos

```bash
npx remotion still Edit out/test-split.png --frame=<f>
npx remotion render Edit out/test-5s.mp4 --frames=<f0>-<f1>
```
