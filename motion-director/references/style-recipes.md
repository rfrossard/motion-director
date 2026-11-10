# Receitas por gênero

Destiladas dos prompts mais salvos de awesome-opus-5.5-video-prompts (CC BY 4.0; os autores estão em `prompt-index.md`). Cada receita traz a direção, a estrutura, a técnica e os gotchas. Adapte-as ao tema do usuário. Não copie o conteúdo dos vídeos originais.

---

## 1. UI morph loop (uma forma, nunca corta)
*Base: "One-shape UI morph loop", @twoclipping, o mais salvo da coleção.*
- **Direção:** UI motion nível Dribbble. Um único elemento muda de tamanho, raio e cor enquanto o conteúdo troca com um blur curto. Um cursor real clica e arrasta. Canvas cinza quente claro, componentes P&B, uma fonte de UI (Geist). Springs com overshoot mínimo. A câmera dá zoom para cada estado ocupar o quadro.
- **Estrutura:** 120 BPM, 7 compassos, algo em cada beat: botão → loader → check → dynamic island → player → slider → toggle → tabs → gráfico → ⌘K → toast → botão.
- **Técnica:** as duas bordas do indicador de tab andam em springs diferentes (a borda da frente estica antes). Drags são manipulação direta: durante o arraste, o valor vem da posição do cursor; ao soltar, volta com spring.
- **Gotchas:** `will-change` em algo que a câmera escala deixa o texto borrado. Texto que troca dentro de um container em morph precisa de tempos próprios de entrada e saída. No loop, o último frame é igual ao primeiro.

## 2. Launch film em um take (estilo keynote)
*Base: "Apple-keynote style launch film", @twoclipping, e "Minimal product launch", @twoclipping.*
- **Direção:** 2D, um take contínuo. Nada faz fade, blur ou corte: os objetos mudam de forma. O texto sobe de uma linha-máscara, os ícones nascem de zero com spring, as barras se desenham e uma forma preta inunda o quadro e se contrai na próxima cena. Off-white quente, UI preta e uma ou duas fontes (Archivo largo 800 para o wordmark, Geist para a UI).
- **Variante minimal:** uma ideia por plano, muito espaço vazio, uma cor de acento, footage real (nunca cards placeholder) e texto sem ponto final.
- **Estrutura:** 120 BPM, de 10 a 54 beats. Gancho palavra a palavra nos beats → uma palavra vira a UI → o drop abre uma cena escura → um movimento por compasso → logo → preto.
- **Técnica:** footage real extraída para JPEG a 30 fps e trocada por frame (o `seek` aguarda o decode). Carrossel 3D com reflexo no chão e whip com motion blur.
- **Gotchas:** opacidade ou filter num elemento `preserve-3d` achata a cena e mostra as duas faces; aplique o fade no wrapper. Meça as posições em runtime para os match cuts.
- **Pesquisa:** quando o produto é real, pesquise o site, extraia a proposta de valor real e use a UI, as cores e a tipografia dele.

## 3. Showreel / résumé reel (15 s)
*Base: @shneural, @darel023, @lukasersil e @prasenx.*
- **Direção:** gancho forte no primeiro segundo. Depois, uma sequência de técnicas distintas (kinetic type, jogo de formas, movimentos de câmera, mudanças de cor, 3D) e um frame final limpo e memorável. Cortado como se fosse música.
- **Técnica:** trilha sintetizada em código, sem samples, com cada corte no beat. 1920×1080 a 60 fps.
- **Gotcha:** "art-directed, não uma coleção de efeitos". Escolha uma paleta e um sistema de tipos e passe por eles. O pedido de uma linha dá resultados variados; transforme-o num brief.

## 4. Kinetic type bumper (identidade de criador)
*Base: "Kinetic type bumper", @techhalla.*
- **Formato:** 1080×1080, 20 s exatos, em loop, 60 fps.
- **Paleta estrita:** fundo #0A0A0A, magenta, verde ácido e branco só para leitura. Nenhum outro matiz.
- **Tipos (use os três):** display ultra-condensado black (1 a 4 palavras), grotesca urbana para hits secundários e mono para rótulos e "migalhas de prompt". Tracking do display de −40 a −80, mono +20.
- **Mensagem travada:** as frases exatas, na ordem. Nada de slogans de enchimento.
- **Técnica:** spring por glifo (y, opacidade e blur), com stagger de 1/16 de nota. Embaralhamento de letras com Fisher–Yates com seed, que se encaixa no beat. Wipe por máscara em que a linha que sai é a máscara. Desregistro de impressão (±2–4 px, magenta e verde a 40%) só nos frames de impacto. Respiração final (escala 1 → 1,012 → 1).

## 5. Pixel art (sprite ou diorama em loop)
*Base: "Pixel art wizard", @majidmanzarpour; "Pixel character dodging meteors", @riku720720; "Paris night diorama", @minosdevs.*
- **Render:** canvas lógico de 128×96, 160×90 ou 480×270, levado a tela cheia por escala inteira, com `imageSmoothingEnabled=false` e `image-rendering: pixelated`. Coordenadas inteiras. Sem sub-pixel, anti-aliasing, gradientes ou `shadowBlur`.
- **Paleta fixa** de 24 a 32 cores. Todo pixel sai dela.
- **Personagem:** procedural, com pose parametrizada (ângulos, bounce, lean). Interpole suave e **quantize** para a grade a cada frame, para parecer animação a 8–12 fps mesmo rodando a 60. Squash & stretch só de 1 a 2 pixels inteiros. Highlight de 1 px no topo e à esquerda, sombra de 1 px embaixo e à direita.
- **Animação:** máquina de estados (IDLE → CHARGE → CAST → RECOVER). Partículas em pool pré-alocado, que trocam de índice de paleta até sumir.
- **Diorama em loop:** camadas de trás para frente, dithering ordenado no céu, chuva em 3 profundidades, que muda de cor ao passar por uma luz. Tudo é função de `t mod D`, com frequências inteiras.

## 6. Explicador (educação)
*Base: "What is a Transformer", @dotey; "Atmospheric circulation in line art", @akokoi1; "LLM context window", @joaoli13; "Recursion in nine styles", @emollick.*
- **Direção:** simples para quem é leigo, mas com detalhe real (mecanismo, um pouco de matemática). Line art leve e divertida funciona muito bem. KaTeX para fórmulas.
- **Som:** TTS grátis (Edge TTS ou Piper) e legendas, bilíngues se for preciso.
- **Técnica:** um conceito por cena, com rótulos no idioma do público. Distinga visualmente as entidades que o público confunde (por exemplo, a janela de entrada e a de saída).
- **Variação criativa:** uma explicação autorreferente em que cada parte troca radicalmente de estilo (recursão).
- Para um flat científico, use `flat-science-explainer`. Para matemática, Manim.

## 7. Histórico / documental
*Base: "Battle of Austerlitz", @WinterArc2125; "Chinese civilization chronicle", @dotey; "1906 Market Street in Blender", @alexalbert__; "Sand animation of US history", @Michaelzsguo.*
- **Direção:** um filme histórico cinematográfico que por acaso é renderizado em código, não um infográfico nem um jogo de estratégia. Pinturas de época como inspiração de atmosfera (céus, fumaça, escala).
- **A trilha como relógio:** o BPM acelera com as eras e cada corte cai no beat. Os instrumentos evoluem com a época.
- **Dois estilos alternados** (por exemplo, nanquim em papel e ouro sobre preto). Padrões ornamentais que evoluem por era. HUD fixo com selo, era e régua de linha do tempo.
- **Fontes antes do modelo:** para reconstruções, monte primeiro um arquivo de fontes (mapas, fotos, filmes de época) com o nível de confiança de cada fato. Os geradores procedurais montam a cena a partir dos dados.
- **Gotchas:** mapas só esquemáticos. Não desenhe pessoas reais contemporâneas. Confira as datas antes de entregar.
- **Outras texturas:** areia (sand art), origami ou doodle sem texto (compreensível em qualquer língua) e linha simples bem-humorada.

## 8. Music video / lyric video
*Base: "Claude Pop", @donaldjewkes; "Demoscene", @gandamu_ml; "Kinetic typography MV", @itnavi2022; "Brushstroke dance", @petergostev.*
- **Primeiro:** analise a faixa (seções, beats, letra com timestamps). Sincronia e adequação de cada cena à atitude da seção são essenciais.
- **Letra:** não ilustre literalmente cada verso. Prefira referências, conceitos e metáforas do universo do tema.
- **Estéticas que funcionam em código:** papel com retícula, manga e pixel print, pinceladas largas, demoscene (shaders e plasma) e tipografia dançante.
- **Pipeline misto (opcional, pago):** footage base gerada, mais animação de letra em JS por cima e sound design. Crie a style sheet primeiro, coerente com o modelo de imagem disponível.
- **Gotchas:** boca "cantando" jittery parece erro; prefira expressões. Braços em poses estranhas parecem bug. Corte o silêncio ou os beats que sobram no final.

## 9. Mundos 3D, shaders e partículas
*Base: "Glass and gold mosaic", @LCSlates; "Morphing journey creature→cosmos", @leo_xiaolei; "Fireworks show", @FornYapayZeka; "Infinite zoom through vintage objects", @koldo2k.*
- **Mosaico vivo:** as figuras são bandos de tiles que levantam, viram, voam e voltam ao lugar com um clique. WebGL2 sem bibliotecas, som sintetizado no browser.
- **Jornada em morph:** cada cena se transforma na próxima por morph, partículas, escala, push de câmera ou continuidade de cor e de movimento. Visual de divulgação científica feito à mão: linhas com leve tremor, formas orgânicas, creme #F2E8CF e cenas cósmicas em navy e roxo, com gradientes contidos. Proibido: ilustração SaaS genérica, cyberpunk, poluição de neon e gradientes de IA.
- **Infinite zoom:** zoom exponencial a velocidade constante (a duração de cada segmento é proporcional a log(zoom)). Cada portal (lente, lupa, espelho) contém o próximo mundo, com corte invisível quando ele preenche o quadro. Parallax por camada de profundidade (escala = câmera^Z). Recortes animados "on twos".
- **Fogos e partículas:** projete o ritmo, a profundidade, a luz sobre o entorno e um final memorável, não explosões iguais multiplicadas. Pese algumas ideias e escolha a mais forte em vídeo.

## 10. Histórias, curtas e personagens
*Base: "2D short with dialogue", @ALSK_ai; "Sketchbook", @kloss_xyz; "Mobile game reward", @op7418.*
- **Curta 2D:** história coerente, diálogo e som. Pode usar agentes em paralelo por cena, desde que a style bible seja compartilhada.
- **Sketchbook:** um caderno em Three.js com page curl real, luz de abajur e uma leve deriva de câmera na mão. Cada página se desenha traço a traço com a ponta do lápis visível. Caligrafia inventada, sem fontes. Score de piano de feltro sintetizado, com som de lápis e papel sincronizado.
- **Recompense de jogo mobile:** objeto 3D real (Three.js), com toon shading de 3 a 4 passos e três luzes (key, sky e rim na cor do tier). Contorno por pós-processo (normal + depth), não por backface escalado. Cinco estágios que não se pulam e a cor muda a cada tier. Arte original, sem imitar IP de jogos existentes.

## 11. Remix de talking head
*Base: "Talking-head → line-art explainer", @AxtonLiu; "Punchy edit", @sab8a; "Podcast with explainer animations", @stokebuilder.*
- **Line art no B-roll:** a pessoa vai para um PiP redondo no canto, sem cobrir as legendas, e o quadro principal desenha o conceito que está sendo falado. Áudio, legendas e duração originais intocados.
- **Edição punchy:** remova silêncios e muletas, adicione legendas no estilo da referência, gráficos e música.
- **Podcast:** encontre de 35 a 50 momentos para animações em tela cheia, com quem fala em PiP. Antes, uma style bible e um kit de componentes compartilhados. Pipeline em três papéis: um agente acha os momentos, outros constroem e um juiz avalia uma vez a consistência e a relevância. Refazer só o que for grosseiramente ruim, sem loops de refação.
- **Regras:** copy fiel ao que foi dito. Cada gráfico fica dentro de um trecho de áudio sem corte, com alguns segundos de rosto entre os gráficos.
- Para o visual P&B de arquivo, use `editorial-archival-edit`.

## 12. "Opus sobre si mesmo" e meta-vídeos
*Base: @goodside, @kloss_xyz e @Gorden_Sun.*
- Créditos de abertura de um filme imaginário (nomes inventados, homenagem a um estilo de autor), um caderno de pensamentos ou um personagem editando um vídeo em take único.
- Funciona quando há ponto de vista e humor. Use a marca da Anthropic e do Claude apenas como referência temática; não imite a identidade oficial em material que pareça oficial.
