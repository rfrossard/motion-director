# Catálogo de estilos

Todos os 27 estilos têm código testado: kit 1 (`assets/kit-src`, 11 cenas) e kit 2 (`assets/kit2`, 28 cenas, ver `assets/kit2/KIT2.md`).
Cada estilo tem um `id` (usado no plano e no `handoff.json`). "ouro" = cena aprovada no portão de qualidade (`quality.md` §1); parta sempre dela. "Executor" = o que você carrega para produzir.
Motor: **R** Remotion · **H** HTML + `seek(t)` + Playwright · **C** canvas próprio · **M** Manim · **B** Blender Python · **F** ffmpeg sobre footage.
Custo: $ simples (horas) · $$ médio · $$$ pesado (pipeline/ferramenta própria). Tudo grátis por padrão, salvo indicado.

## Existentes

| id | Estilo | Executor | Motor | Custo | Melhor para | Evitar quando | Bastão típico (entra → sai) |
|---|---|---|---|---|---|---|---|
| `led` | Painel de LED de pontos | kit `scenes/Led.tsx` | R | $ | perguntas, teasers, frases de impacto | texto longo | tela → pontos convergem num ponto |
| `flat` | Flat científico (Kurzgesagt-like) | `flat-science-explainer` · ouro kit2 `v3.tsx` `FlatV3` | R | $$ | ciência, mecanismos, escala | dados exatos | ponto → esfera; esfera → "foto" |
| `collage` | Colagem de papel rasgado | `paper-collage-film` · kit `Collage.tsx` | C/R | $$ | intros, bastidores, marcas, zines | tom sóbrio | foto colada → página rasga |
| `ink` | Nanquim e selo (linha do tempo) | ouro kit2 `v3.tsx` `InkV3` | R | $ | cronologias, contexto, "antes e depois" | muitos dados | papel → selo redondo |
| `journey` | Jornada em take único (herói por estações) | `explainer-engaging` · ouro kit2 `v2.tsx` `JourneyV2` | H/R | $$ | processos, fluxos, "como funciona" | conceitos sem etapas | bola ↔ bola |
| `uimorph` | UI morph (uma forma, cursor real) | `motion-broll` · kit `UiDemo.tsx` | H/R | $$ | produto, interações, B-roll de UI | sem produto/UI | bola → botão; cartão → tela cheia |
| `demo` | Demo calmo de produto (UI recriada filmada de perto) | `explainer-default` · ouro kit2 `v2.tsx` `DemoV2` | H | $$ | walkthrough 45–90 s | ritmo energético | — |
| `datastory` | Data story editorial | ouro kit2 `v3.tsx` `DataV3` | R | $ | um número, uma comparação | muitos números ao mesmo tempo | barra destaque → linha |
| `stroke` | Traço preciso (wireframe/estilo 03) | ouro kit2 `v3.tsx` `StrokeV3` | R | $ | papers, diagramas, arquitetura | emoção | linha → contorno → quadro |
| `archival` | Editorial de arquivo P&B (sobre vídeo real) | `editorial-archival-edit` · kit `Editorial.tsx` | R/F | $$ | entrevistas, depoimentos, documentário | sem footage | quadro → íris |
| `extrude3d` | 3D extrudado (logo/objeto em camadas) | kit `Future3D.tsx` | R+three | $$ | marcas, visão, transições | personagens | escuro → inunda de cor |
| `hype` | Anúncio no beat com HUD | `explainer-high-energy` · ouro kit2 `v3.tsx` `HypeV3` | H/R | $ | anúncios, teasers, CTA | conteúdo denso | inundação de cor ↔ ponto |

## Novos (fichas em `cards/`; os existentes hype, flat, datastory, stroke, ink, journey, demo e broll também têm ficha)

| id | Estilo | Executor | Motor | Custo | Melhor para | Evitar quando | Bastão típico |
|---|---|---|---|---|---|---|---|
| `pixel` | Pixel art 16-bit | `cards/pixel.md` · kit2 | C/R | $$ | loops, lofi, games, personagens, nostalgia | realismo, dados | pixel → bloco de cor; sprite sai pela borda |
| `blender3d` | Reconstrução 3D realista | `cards/blender3d.md` · kit2 | B | $$$ | história, lugares, arquitetura, produto 3D | prazo curto | câmera atravessa janela/objeto |
| `creator` | Edição punchy de criador (talking head) | `cards/creator.md` · kit2 | F/R | $$ | Reels/TikTok/YouTube, depoimentos | tom contemplativo | jump cut no beat; zoom punch |
| `geomap` | Mapa e terreno cinematográfico | `cards/geomap.md` · kit2 | R/H+three | $$$ | viagens, rotas, história, "onde" | conceitos abstratos | zoom do globo até o ponto / do ponto ao globo |
| `manim` | Matemático (3Blue1Brown-like) | `cards/manim.md` · kit2 (Manim via micromamba) | M | $$ | aulas, fórmulas, gráficos, lógica | emoção, produto | equação se transforma em forma |
| `sand` | Animação em areia | `cards/sand.md` · kit2 | C/R | $$ | histórias emotivas, homenagens, retrospectivas | UI, dados | areia varrida revela a próxima cena |
| `mosaic` | Mosaico de vidro e ouro | `cards/mosaic.md` · kit2 | H(WebGL2) | $$$ | arte, aberturas, cartões, contemplação | texto longo | pastilhas em bando formam o próximo objeto |
| `toon3d` | Toon 3D de game (recompensa/conquista) | `cards/toon3d.md` · kit2 | H/R+three | $$ | conquistas, marcos, aniversários, gamificação | diretoria/sóbrio | explosão de partículas → cor do nível |
| `anime` | Anime com cortes rápidos | `cards/anime.md` · kit2 | C/R | $$ | trailers, humor, histórias para redes | dados, explicação longa | linhas de velocidade / flash branco |
| `sketch` | Quadro branco e lápis | `cards/sketch.md` · kit2 | R/C | $ | tutoriais, resumos, data story à mão | luxo/premium | mão apaga o quadro / vira a folha |
| `particles` | Constelação de partículas | `cards/particles.md` · kit2 | H(WebGL)/R+three | $$ | cenários oníricos, dados densos, cosmos | texto pequeno | partículas se dispersam/condensam na próxima forma |
| `shadow` | Teatro de sombras | `cards/shadow.md` · kit2 | R/C | $ | fábulas, histórias pessoais, vertical | dados, UI | lâmpada apaga/acende; silhueta atravessa a tela |
| `comic` | Quadrinhos (HQ) | `cards/comic.md` · kit2 | R/C | $$ | humor, histórias, resumir um texto | tom solene | câmera atravessa o quadro seguinte |
| `news` | Telejornal / boletim | `cards/news.md` · kit2 | R | $ | recaps, notícias, resumos semanais | arte/contemplação | vinheta com faixa que varre a tela |
| `screencast` | Screencast com zoom automático | `cards/screencast.md` · kit2 | F/R | $$ | tutoriais de software, demos reais | sem gravação de tela | zoom out até a janela vira objeto |

## Reserva (sem ficha ainda — use `style-recipes.md` e `prompt-index.md`)

| id | Estilo | Perto de | Exemplo |
|---|---|---|---|
| `cutaway3d` | Corte técnico 3D (explodido) | `blender3d` | "3D film inside an AI data centre" (@Sayan_shanky) |
| `titles` | Abertura cinematográfica | `hype` | "Emmy-style title sequence" (@abhinayguptha), créditos (@goodside) |
| `riso` | Risograph (2 tintas, desregistro) | `collage` | "Risograph-style studio intro" (@rneayan) |
| `storybook` | Livro ilustrado aquarela | `flat` | "Journey of a photon" (@AstroTheWizard) |
| `musicmachine` | Máquina física musical | `journey` | colisões tocam notas (@kamstudiolabs), Für Elise (@kantamk) |
| `demoscene` | Demoscene / shader | `particles` | Second Reality demo (@gandamu_ml) |
| `ascii` | ASCII | `led` | skill `ascii-video` no Hermes |
| `brainrot` | Brainrot vertical caótico | `creator` | (@kloss_xyz) |
| `scope` | Osciloscópio / vetorial | `stroke` | (@rneayan) |
