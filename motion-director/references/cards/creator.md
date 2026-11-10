# Edição punchy de criador (`creator`)

**Look**: o vídeo da pessoa falando, cortado seco (silêncios e muletas removidos), zooms "punch" nas frases-chave, legendas animadas grandes palavra a palavra com destaque de cor, emojis/ícones e B-roll curto, SFX (whoosh, pop, ding), música animada baixa.
**Usos**: Reels, TikTok, Shorts, YouTube, LinkedIn pessoal, depoimentos, aulas curtas.
**Exemplos**: "Talking-head clip cut into a punchy edit" (@sab8a, 581 salvos), "Raw clip cut into a snappy social edit" (@sab8a).

## Pipeline
1. **Transcrever** com timestamps por palavra (`assets/kit-scripts/transcribe.mjs` → `words.py`).
2. **Cortes**: remover pausas > 0,35 s e muletas ("é…", "tipo", "né", repetições) — gere uma EDL `[{src_in, src_out}]`; mantenha 2–4 frames de respiro. Preserve sentido e não corte no meio de palavra.
3. **Ritmo visual**: a cada 2–4 s um evento (zoom 1.0→1.15 em 6 frames com mola, troca de enquadramento, B-roll, gráfico). Alterne zoom in/out para disfarçar jump cuts.
4. **Legendas**: 1–3 palavras por vez, fonte grossa (Archivo/Inter Black 80–110 px), contorno ou caixa, palavra atual em cor de destaque, entrada com pop (escala 0.8→1 em 4 frames). Zona segura vertical: longe da UI da plataforma (embaixo e direita).
5. **Gráficos**: ícones/emojis e números que aparecem quando citados; setas; "lower third" com nome.
6. **Som**: SFX nos eventos (skill `sound-effects`), música a −20/−24 LUFS sob a fala, fala normalizada a −16 LUFS (redes).
7. Formato: 9:16 1080×1920 por padrão; reenquadre seguindo o rosto (centro do rosto por detecção ou objectPosition manual por trecho).

## Técnica (Remotion)
```tsx
// EDL de cortes → sequências encadeadas
let at = 0;
{edl.map((c, i) => { const len = Math.round((c.out - c.in) * fps); const el = (
  <Sequence key={i} from={at} durationInFrames={len}>
    <OffthreadVideo src={SRC} startFrom={Math.round(c.in * fps)} style={{transform: `scale(${zoomAt(i)})`}} />
  </Sequence>); at += len; return el; })}
// confira na versão instalada se o prop é startFrom ou trimBefore
```

## Armadilhas
- Não mude o sentido da fala ao cortar; nada de juntar frases que mudam o significado.
- Legenda nunca sobre a boca/olhos; contraste AA.
- Zoom em footage de baixa resolução pixeliza — limite a 1.2× em 1080p.

## Bastões
Jump cut no downbeat; zoom punch que termina num objeto/gráfico que vira o próximo estilo.

## Prompt-semente
"Corte este vídeo em uma edição punchy de <30–60> s para <plataforma>: remova silêncios e muletas, zooms nos pontos-chave, legendas grandes palavra a palavra com destaque, ícones quando citados, SFX e música baixa. 9:16, fala a −16 LUFS."

**Status**: testado no vídeo "Biblioteca de estilos" (08/11/2026). Código: `assets/kit2/src/b/ch1.tsx` · cena `CreatorV`.

**Lições do teste**: EDL automática a partir das palavras (junta lacunas < 0,22 s, remove repetições), zoom punch por palavra-chave, legenda 1–3 palavras com destaque, `Freeze` no fim para não ficar preto.

**Auditoria (09/11/2026)** (composição / ofício / movimento / legibilidade / fidelidade): 4 / 4 / 4,5 / 4 / 4. Passa. Cuide para a legenda não cobrir o rosto.
