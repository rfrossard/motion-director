# Barra de qualidade: portão obrigatório

Nenhuma cena entra no vídeo, e nenhum vídeo é entregue, sem passar por este portão. Isso vale para o master e para qualquer skill de estilo chamado direto.
Origem: em 08–09/11/2026 a 1ª versão de 13 das 27 cenas da biblioteca "funcionava", mas ficou abaixo das referências. Todas foram refeitas pelo método abaixo.

## 0. O portão em uma linha
**Referência → começar do padrão-ouro → ≥ 2 rodadas de crítica (todos os critérios ≥ 4) → regras duras → auditoria do MP4 final com `scripts/audit.py check` passando.**
Se o prazo não permitir, avise o usuário de qual cena ficou abaixo e por quê. Nunca entregue calado.

## 1. Comece do padrão-ouro, nunca do zero nem da v1
Cada estilo tem uma cena aprovada no kit 2 (`assets/kit2/src/b/`). Copie, adapte o conteúdo e mantenha os traços de qualidade.
As versões v1 (`ch1`–`ch6`: `HypeV`, `Toon3DV`, `AnimeV`, `FlatS`, `JourneyS`, `SketchS`, `ComicS`, `DataS`, `StrokeS`, `InkS`, `ShadowS`, `DemoS`; `engines/manim/mola.py`) ficam só como exemplo do que **não** aceitar.

| estilo | padrão-ouro | referência | traços obrigatórios |
|---|---|---|---|
| hype | `v3.tsx` `HypeV3` | skill explainer-high-energy | forma que atravessa todos os cortes (faísca → linha → ponto que inunda); slam com máscaras a 1/16 de beat; trio cinético (2 beats cada, fundos próprios, palavra contornada em padrão, visor com rótulo, palavra manuscrita); visual-assinatura; HUD de visor em todas as cenas |
| toon3d | `v3.tsx` `Toon3DV3` | game show brilhante (emollick) | geometria com bevel (nunca caixas cruas); metal e luz interna; letreiro em 4 camadas (extrusão, contorno, brilho, gradiente com corte duro); squash no toque; estrelas e retícula; barra de status |
| flat | `v3.tsx` `FlatV3` | `flat-science-explainer/references/style-guide.md` | zoom de escala contínuo; cel shading (sombra recortada) e luz de borda em toda forma; glow; partículas em 3 camadas; mascotes geométricos; granulação + vinheta; rótulos com linha-guia |
| datastory | `v3.tsx` `DataV3` | caderno editorial (groundcontrol) | papel com textura e cruzetas; manchete em itálico serifado; número-herói grande; colunas hachuradas, destaque em cor; carimbo; anotação à mão com seta; fonte citada |
| stroke | `v3.tsx` `StrokeV3` | estilo 03 do Hub / desenho técnico | câmera perto percorrendo os nós enquanto o traço desenha; ícones em linha (nunca caixa vazia); cotas; laço de revisão com ponto viajante; grade sutil |
| ink | `v3.tsx` `InkV3` | caderno editorial (groundcontrol) | pincel com pressão (perfect-freehand); câmera seguindo a ponta; ícones esboçados (rough.js); horas manuscritas; carimbo; título escrito à mão |
| shadow | `v3.tsx` `ShadowV3` | teatro de sombras (Reiniger) | silhueta Open Peeps de corpo inteiro; camadas de papel com parallax mais claras que a figura; moldura de teatro; luz que muda com a história |
| sketch | `sketch2.tsx` `SketchV2` | explicadores de quadro branco (lemomo, mattbean) | papel pontilhado; selos numerados; escrita traço a traço com lápis visível; marca-texto hachurado; apresentadora Open Peeps; apagador na saída |
| comic | `v2.tsx` `ComicV2` | HQ (madpencil) | moldura em retícula; faixa de título; mesmo personagem Open Peeps em todos os quadros com expressões diferentes; balões com cauda; onomatopeias contornadas; câmera lendo quadro a quadro |
| anime | `v2.tsx` `AnimeV2` | trailer anime (ishuagra02) | cidade noturna, lua, chuva; títulos com brilho; painéis diagonais com aura; impact frame; protagonista = footage real tratado (duotone) |
| journey | `v2.tsx` `JourneyV2` | explainer-engaging | grafite pontilhado; herói com halo e rastro; estações = cartões de UI realistas que reagem; câmera ~1,5× que recua no fim |
| demo | `v2.tsx` `DemoV2` | explainer-default | app inteiro recriado (chat com checklist + prévia); câmera de perto que segue a digitação e desliza; botão com clique e progresso |
| manim | `engines/manim/mola2.py` `Mola2` | 3Blue1Brown | fórmulas **tipografadas** (MathJax → SVG, `scripts/tex2svg.mjs`; nunca fonte mono); cada variável com cor fixa (ζ laranja, ω azul, decaimento verde); derivação visível; sistema físico sincronizado com o gráfico; envelope/guias; ValueTracker com seletor; curvas-fantasma |
| demais 14 (creator, led, particles, extrude3d, news, geomap, blender, archival, broll, podcast, screencast, sand, collage, pixel, mosaic) | cenas do kit 2 em `ch1`–`ch6`, `Archival.tsx` | fichas em `cards/` | aprovadas na auditoria (3,5–4,5). B-roll de podcast e pixel são as mais fracas: ao usá-las, faça a rodada de crítica com atenção redobrada |

## 2. Referência antes de desenhar
- Pegue 3–5 frames de bons vídeos do estilo. Use os vídeos da coleção (`prompt-index.md`: `media.video_hd` do `site/data.json`) e extraia com ffmpeg `-ss <t> -frames:v 1`. Monte `work/sheets/refs_<estilo>.png`.
- Escreva os 4–6 traços de qualidade da referência (a coluna "traços obrigatórios" acima é o ponto de partida).

## 3. Rodadas de crítica (mínimo 2)
Em cada rodada, faça stills de 3 momentos da cena (entrada, meio, clímax) e uma tira de movimento (8 frames, um a cada 3), e ponha tudo **na mesma imagem** que a referência.
**Defeitos antes das notas:** liste no mínimo 3 defeitos concretos (o que, onde, por quê) antes de pontuar. Nota 5 só se a lista honesta for "nenhum".
O autor tende a se dar notas generosas: na biblioteca, cenas aceitas como 3,5–4 viraram 2–3 numa segunda olhada contra a referência.
Notas de 1 a 5:
| critério | pergunta |
|---|---|
| composição | a tela está cheia e equilibrada? há um foco claro? |
| ofício | o traço/forma parece feito por profissional ou "programado"? |
| movimento | o ritmo e as entradas têm intenção? a câmera se move com motivo? |
| legibilidade | texto e números se leem no tamanho final? nada cortado ou sobreposto? |
| fidelidade | os traços obrigatórios estão presentes? |
Qualquer critério abaixo de 4 → corrija e repita. Guarde o antes/depois em `work/sheets/`.
**Revisor independente:** na rodada final de cada cena e na auditoria do MP4, quando houver ferramenta de subagente, peça a avaliação a um subagente novo.
- Ele recebe só as folhas, a referência e a lista de traços obrigatórios; não recebe o código nem a sua opinião.
- Use as notas dele, não as suas.
- Sem subagente disponível, escreva `revisor: autor` no `scores.md` e diga isso ao usuário.

**Adaptar uma cena de ouro a outro conteúdo** reabre o portão: a estrutura (câmera, camadas, ritmo) fica, mas texto, dados e densidade mudam. Refaça as 2 rodadas.

## 4. Regras duras (cada uma já derrubou uma cena)
1. **Pessoas nunca desenhadas do zero em SVG.** Ordem de preferência:
   1. footage real do usuário (recorte com `object-separation`, tratamento duotone/P&B);
   2. **Open Peeps** (`react-peeps`, MIT, arte CC0);
   3. folha de personagem gerada (paga, com OK e custo);
   4. abstração assumida (mascote geométrico, silhueta).

   O `viewBox` do Open Peeps depende da pose:
   - bustos: `{x:'0', y:'0', width:'850', height:'935'}`;
   - em pé apontando (sem pernas visíveis): `{x:'-60', y:'-20', width:'1400', height:'1500'}`;
   - **corpo inteiro com pernas: `{x:'-100', y:'-20', width:'1400', height:'2470'}`**, porque com 1500 a figura é cortada na cintura.

   Silhueta: `strokeColor` = `backgroundColor` = cor da tinta, com fundo mais claro que ela.
2. **Composição cheia.** Nada de poucos elementos pequenos num fundo vazio:
   - câmera perto (1,4–2×) que percorre a cena e só recua no fim;
   - elementos ocupando ≥ 60 % do quadro no clímax.
3. **Receita do estilo.** Antes de codar, releia os obrigatórios do skill de origem e da tabela acima. Faltou um, a nota de fidelidade é ≤ 3.
4. **Legibilidade mínima a 1080p:**
   - corpo e rótulos ≥ 22 px (em 9:16, ≥ 30 px);
   - rótulos de gráfico 22–24 px;
   - nota de fonte/crédito ≥ 18 px;
   - texto nunca cortado pela borda nem sobreposto ao cartão de invocação ou à legenda;
   - margem segura: nenhum texto a menos de 60 px da borda (exceto molduras e HUD intencionais). No Manim, mantenha o conteúdo em |y| ≤ 3,3.
5. **Matemática sempre tipografada:** MathJax → SVG (`scripts/tex2svg.mjs`, `\color{#hex}` por variável) no Manim (`SVGMobject`) e no Remotion (`<Img>`). Proibido fórmula em fonte mono ou `MarkupText`.
   - `TransformMatchingShapes` entre fórmulas diferentes embaralha os glifos: mostre a derivação em linhas (EDO em cima, ⇒, solução embaixo).
   - `DecimalNumber`/`MathTex` exigem LaTeX: use `Text` redesenhado com `always_redraw`.
6. **Fontes de traço (EMS felix/read) não têm º, · nem —.** `hand.tsx` lança erro no render se faltar glifo. Reescreva o texto ("primeiro", vírgula, dois-pontos) ou componha o glifo em `build_hand_fonts.mjs`.
7. **Zoom exponencial:** mova o alvo com `kc = (Z/z − 1)/(Z − 1)`, não com o mesmo easing do zoom; senão o objeto sai do quadro no meio.
8. **Clipes de motor externo** (Manim, Blender, gravação) devem caber na janela da cena: meça a duração e garanta que o conteúdo termine antes do cartão de invocação (`dur − 146` frames). No Manim, use `self.wait(max(0.5, DUR − self.time))` no fim.
9. **Transições:** o flash do momento-assinatura é curto (≤ 6 frames) e colorido, nunca cinza. Nenhum frame vazio por mais de 10 frames fora de holds intencionais.

## 5. Auditoria do MP4 final (obrigatória antes de entregar)
```
python scripts/audit.py extract out/video.mp4      # cenas (sheet_NN), passagens antes/meio/depois (trans_NN), movimento (motion_NN) + scores.md
# revisor (de preferência independente) lista defeitos e dá notas em work/audit/scores.md: cenas (5 critérios) e passagens (1 nota)
python scripts/audit.py check                      # código 1 se faltar nota/defeito, se algo < 4, ou 5 com defeito listado
```
- Rode com o ambiente global: `~/.local/share/motion-director/env/bin/python scripts/audit.py …` (o script acha o ffmpeg completo sozinho).
- Cena reprovada: volte ao §3 só para ela, re-renderize e audite de novo.
- Na entrega, inclua as folhas e o `scores.md`, e diga ao usuário as notas mais baixas.

## 6. Passagens e movimento (o que still parado não mostra)
- **Passagem:** os dois lados precisam ter conteúdo. Proibido o frame "depois" ser tela vazia, preta ou só moldura; a cena que entra já começa com algo desenhado.
  Achado da autoavaliação: hype → creator (celular preto depois do flash) e journey → manim (escurece e entra eixo vazio).
- **Movimento:** numa tira de 8 frames, algo precisa mudar de forma perceptível, salvo hold intencional ≤ 1 s com motivo. Holds longos e estáticos (abertura, LED) custam nota de movimento.

## 7. Áudio (eu não ouço: meça e peça ao usuário)
- Medidas obrigatórias: LUFS integrado −16 a −19, LRA ≤ 6, pico ≤ −0,8 dBFS, LUFS por cena (`measure_scenes.py`), dentro de ±4 LU entre cenas.
- Cortes e SFX no beat (erro ≤ 1 frame). Música sob fala ≥ 12 dB abaixo da voz.
- A trilha sintetizada (`score2.py`) é funcional, não é trilha de qualidade. Para entrega final, prefira música licenciada ou gerada (paga, com OK) e diga isso ao usuário.
- Sempre entregue 3–5 timestamps para o usuário ouvir (passagens e picos). Nunca diga "soa bem".

## 8. Ferramentas
- **Feito à mão:**
  - `rough.js` (formas e hachuras), `perfect-freehand` (traço com pressão) e fontes de traço único EMS (OFL, via `hersheytext`), com acentos e "→" compostos (`scripts/build_hand_fonts.mjs` → `handfonts.json`).
  - Módulo pronto: `src/b/hand.tsx` (`Written`, `Rough`, `Pencil`, `missingGlyphs`).
- **Matemática:** `scripts/tex2svg.mjs` (mathjax-full 3.2.2, Apache-2.0) e `engines/manim/tex/formulas.json`.
- **Verificar uma página/fonte isolada:** `scripts/shot_html.mjs`.
- **Stills em lote:** `scripts/stills.mjs`. **Auditoria:** `scripts/audit.py`.
