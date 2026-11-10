---
name: flat-science-explainer
description: "Vídeos explicativos animados no estilo 'Kurzgesagt-like': ilustração vetorial plana, cores saturadas sobre fundos profundos, brilho suave, personagens simples e movimento sempre vivo, feitos em Remotion. Use quando o usuário pedir um vídeo ou animação 'estilo Kurzgesagt', 'in a Nutshell', 'flat design científico', 'explicador de ciência', 'cosmic zoom' ou algo parecido."
---

# Flat Science Explainer (inspirado em Kurzgesagt)

Este skill especializa o `remotion-video-studio`. Siga o fluxo do studio (**Ambiente → Entrevista → Roteiro → Stills → Render → Entrega**) e todas as regras rígidas dele: grátis por padrão, chaves só no `.env`, nunca dizer "renderizado" sem ter renderizado, animação determinística e nada de dados inventados. As decisões abaixo já estão tomadas e encurtam a entrevista. Converse em pt-BR, a não ser que o usuário use outro idioma.

Antes de desenhar qualquer coisa, leia `references/style-guide.md` (paletas, formas, sombreamento e movimento). Antes de escrever componentes, leia `references/remotion-patterns.md` (padrões de código prontos).

## Linha vermelha: estilo, não cópia

O que se pode reproduzir é a *linguagem visual*: flat, geométrica, saturada, com brilho e humor. Nunca reproduza a obra do canal:
- Nada do nome "Kurzgesagt" nem do logo na tela, nos créditos ou nos metadados do vídeo. No prompt do usuário, "estilo Kurzgesagt" serve só como referência de briefing.
- Nada dos pássaros (o mascote), dos personagens recorrentes, de cenas recriadas quadro a quadro nem da trilha (Epic Mountain).
- Personagens, mascote e paleta são **originais** de cada projeto. Se o usuário pedir para copiar um frame, um personagem ou a música do canal, explique o limite e ofereça uma alternativa original no mesmo espírito.

## Decisões fixas (não pergunte de novo)

- **Motor:** Remotion + SVG em React. Ilustração 100% vetorial e procedural, desenhada em código. Sem imagens raster de terceiros. Three.js só se o usuário pedir.
- **Formato padrão:** explicador 16:9 de 60–120 s, a 30 fps e 1920×1080. Vertical 9:16 sob pedido, recompondo as cenas em vez de apenas cortar.
- **Estrutura narrativa** (template Explainer do studio, adaptado):
  1. **Gancho:** uma pergunta ou um fato contraintuitivo, em 5–8 s.
  2. **Escala:** situar o assunto com um zoom de escala (célula → corpo → planeta, ou o inverso).
  3. **Mecanismo:** como funciona, em 2–4 cenas, cada uma com uma única ideia visual.
  4. **Virada:** a complicação, o "mas…".
  5. **Fecho:** uma conclusão curiosa ou esperançosa, mais uma pergunta que fica.
- **Tom de narração:** calmo, curioso, com humor seco e frases curtas. Segunda pessoa ("você") é bem-vinda. Nada de jargão sem uma imagem que o explique.
- **Narração:** Piper local por padrão. ElevenLabs só se o usuário escolher, com as regras de custo e licença do studio.
- **Música:** ambiente sintetizada e calma (pads, arpejos suaves). Use uma faixa livre com licença conhecida ou Lyria (pago, com confirmação). Nunca use trilhas do canal.
- **Legendas:** queimadas, em fonte arredondada e caixa discreta. Ligadas por padrão no vertical e opcionais no 16:9.
- **Fontes:** livres e locais. Títulos em **Fredoka** ou **Baloo 2**, texto em **Nunito**. Registre todas em `CREDITS.md` (SIL OFL).
- **Dados e ciência:** todo fato científico precisa de fonte. Liste as fontes numa tabela do roteiro e em `SOURCES.md`. Números ilustrativos levam a marca "ilustrativo" na tela. Simplificações deliberadas ficam anotadas no roteiro.

## Entrevista (só o que falta)

Faça uma rodada só, com no máximo 4 perguntas:
1. Tema e a única ideia que o espectador deve levar (texto livre).
2. Duração e formato → 60 s · 90 s · 2–3 min · vertical de 30–45 s.
3. Paleta → ofereça as 3 paletas originais de `references/style-guide.md` que combinam com o tema (Abissal, Nebulosa, Bioluminescente, Savana Solar ou Ártico), mais "crie uma nova".
4. Som → narração (Piper, ElevenLabs, voz própria ou só texto) e música (sem música, arquivo próprio, faixa livre ou Lyria).

Pergunte sobre marca e uso comercial só se o vídeo for de uma organização (licença da Remotion, como no studio). Se o usuário disser "decide você", escolha, mostre as escolhas num bloco curto e peça um OK.

## Roteiro (portão de aprovação)

Use a tabela do studio com uma coluna extra: `# | tempo | visual / animação | câmera | texto na tela | narração | fonte`.
- **Visual:** descreva formas e metáforas concretas ("glóbulos brancos como pílulas azul-claras com olhos, patrulhando um vaso vermelho-escuro"), não abstrações.
- **Câmera:** parallax, zoom de escala, travelling lateral ou estática com elementos vivos.
- Uma ideia por cena. Cenas de 4–10 s. Pelo menos um momento de humor visual a cada 30 s.
- Confira o orçamento de palavras do studio (~2,3 palavras/s em pt-BR). Explicadores pedem um ritmo um pouco mais lento: mire em ~2,0.

Não construa nada antes da aprovação.

## Stills e o checklist de estilo

Renderize um still por cena e confira cada um contra o checklist antes de mostrar ao usuário:
- [ ] Fundo escuro e saturado, com gradiente sutil. Nunca preto puro nem branco puro.
- [ ] Toda forma tem sombreamento cel (sombra de forma em tom mais escuro do mesmo matiz) e uma luz de borda ou brilho.
- [ ] Sem contornos (strokes) nos objetos. A separação vem do contraste de valor.
- [ ] Um único ponto focal por quadro, com o acento mais quente ou mais claro nele.
- [ ] Partículas, estrelas ou poeira em 2–3 camadas de profundidade.
- [ ] Granulação (grain) leve por cima de tudo.
- [ ] Texto legível: no máximo 8 palavras por linha, com contraste AA.
- [ ] Nenhum elemento do canal original (logo, pássaros, personagens).

Ajuste o que falhar e só então peça o go/no-go.

## Render e entrega

Siga as fases 4 e 5 do studio. Para SFX (pops, whooshes, brilhos), rode o skill `sound-effects` sobre o MP4 final. Além do que o studio entrega, entregue:
- `SOURCES.md` com as fontes científicas citadas.
- `CREDITS.md` com fontes tipográficas, voz e música, e a nota "estilo visual original, inspirado na estética flat de explicadores científicos".
- Três frames-chave em PNG (início, meio e fim) para thumbnail.

## Portão de qualidade (biblioteca local; obrigatório)
Este skill faz parte da biblioteca coordenada pelo `motion-director`. Mesmo chamado direto, siga `~/.claude/skills/motion-director/references/quality.md`:
1. Parta do padrão-ouro do estilo `flat`: `~/.claude/skills/motion-director/assets/kit2/src/b/FlatV3`. Não comece do zero.
2. Antes de codar, monte uma folha de referência do estilo e liste os traços obrigatórios.
3. Faça no mínimo 2 rodadas de crítica com stills, com todos os critérios (composição, ofício, movimento, legibilidade, fidelidade) ≥ 4.
4. Aplique as regras duras: pessoas nunca desenhadas do zero em SVG (footage real → Open Peeps → abstração), composição cheia e legibilidade mínima de 22 px a 1080p.
5. Antes de entregar, rode a auditoria do MP4 (`assets/kit2/scripts/audit.py extract` → notas → `check`).

Específico deste estilo:
- zoom de escala contínuo (o alvo se move com `kc = (Z/z − 1)/(Z − 1)`)
- cel shading e luz de borda em toda forma; glow; partículas em 3 camadas; granulação e vinheta
- composição cheia: uma cena-mundo (objetos, máquinas, mascotes) ocupando o quadro, nunca 2–3 formas soltas num fundo vazio
- fórmulas tipografadas (MathJax → SVG), nunca em fonte mono
