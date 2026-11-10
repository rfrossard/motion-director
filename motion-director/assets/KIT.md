# Kit Remotion — as 11 cenas do vídeo "Onze formatos"

Código testado (render completo de 137 s verificado em 2026-11-08, Remotion 4.0.541). Origem: `~/Projects/videos/hub-formatos`.

> **Atenção (09/11/2026):** as cenas `Flat`, `Timeline` (ink), `Journey`, `DataStory`, `Paper` (stroke) e `Hype` deste kit são **v1** e ficaram abaixo do portão de qualidade.
> Para esses estilos, parta das cenas de ouro do kit 2 (`kit2/KIT2.md`, tabela "Estilo → cena de ouro").
> Este kit continua útil para a estrutura do vídeo do Hub (timeline, marca, `Editorial.tsx`, `Future3D.tsx`, `UiDemo.tsx`, `Led.tsx`).

## Usar
1. Crie o projeto: `mkdir meu-video && cd meu-video && cp ~/.claude/skills/motion-director/assets/{package.json,tsconfig.json,remotion.config.ts} . && cp -R ~/.claude/skills/motion-director/assets/kit-src src && mkdir -p scripts public/{fonts,brand,audio} && cp ~/.claude/skills/motion-director/assets/kit-scripts/* scripts/`
2. `npm install` (versões fixas no package.json).
3. Troque **`src/theme.ts`** (cores e famílias) — o kit vem com os tokens do Hub; para uso pessoal, ponha a sua paleta.
4. Fontes: copie os .woff2/.ttf para `public/fonts/` e ajuste `src/fonts.ts`.
5. Monte a sua sequência em `src/HubFormatos.tsx` (renomeie) usando `src/timeline.ts` para os inícios das seções.

## Cenas (`src/scenes/`)
| Arquivo | Estilo (`id`) | Entra com | Sai com |
|---|---|---|---|
| `Led.tsx` | `led` | tela de pontos | pontos → um ponto no centro |
| `Flat.tsx` | `flat` | ponto → esfera | (vira foto no Collage) |
| `Collage.tsx` | `collage` | cena anterior encolhe e vira foto | página rasga revelando a cena de baixo |
| `Timeline.tsx` | `ink` | papel creme | mergulho no selo (tela laranja) |
| `Journey.tsx` | `journey` | laranja contrai até a bola | bola ao centro |
| `UiDemo.tsx` | `uimorph` | bola → botão | cartão ocupa a tela |
| `DataStory.tsx` | `datastory` | tela clara | barra destaque → linha vertical |
| `Paper.tsx` | `stroke` | linha → contorno de documento | contorno → quadro 16:9 |
| `Editorial.tsx` | `archival` | quadro 16:9 | íris fecha |
| `Future3D.tsx` | `extrude3d` | escuro | laranja inunda a tela |
| `Hype.tsx` | `hype` | laranja | tudo recolhe num ponto |
| `Bookends.tsx` | abertura/fechamento | — | — |

`lib.ts`: molas em forma fechada, `softIn`, `dropIn` (stop-motion 12 desenhos/s), `tornRect` (papel rasgado), easing. `Label.tsx`: rótulo de formato.
`Editorial.tsx` lê `editorial-edl.json` (legendas, palavras cinéticas, splits) e `public/source/entrevista.mp4`; `Future3D.tsx` lê `brand-parts.json` (troque pelos paths do seu logo).

## Scripts (`kit-scripts/`)
- `score.py` — trilha sintetizada por seção (edite o bloco de cada seção; `DUR` = duração). `python3 scripts/score.py public/audio/score.wav [drive]`
- `measure.py` — LUFS (BS.1770), pico e sincronia de eventos de um WAV decodificado do MP4.
- `transcribe.mjs` → `words.py` → `make_edl.py` — transcrição local (whisper.cpp medium, pt) e EDL de legendas/cinéticas.
