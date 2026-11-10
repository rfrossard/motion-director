# Anime com cortes rápidos (`anime`)

**Look**: cel-shading de 2 tons com contorno, fundos pintados (céus com gradiente, nuvens grandes), **linhas de velocidade**, close extremo nos olhos, impact frames (inversão de cor por 1–2 frames — nunca tela cheia piscando repetidamente), texto onomatopeico, cortes de 0,3–1,5 s, câmera com shake e zoom.
**Usos**: trailers, humor, histórias e "compressed learning" para redes, recap de conquistas.
**Exemplos**: "Anime-style remake of Claude's Voynich film" (@emollick, 642 salvos), "Anime trailer: Claude vs ChatGPT battle" (@ishuagra02).

## Gramática de corte
- Estrutura de trailer: gancho (1 s) → apresentação do personagem (pose + nome) → conflito → montagem rápida no beat → clímax (impact frame + silêncio de 0,3 s) → título.
- Animação "on threes" (8 desenhos/s) para personagens; câmera e efeitos a 30 fps.
- Planos: close de olhos, plano americano com vento no cabelo, contra-plongée heroico, silhueta contra o sol.

## Técnica (2D em código)
- Personagens **originais** desenhados em SVG/Canvas por partes (cabeça, olhos grandes, cabelo em mechas que balançam por mola), sombra cel como forma recortada (`clipPath`).
- Linhas de velocidade: raios a partir de um ponto de fuga com comprimentos aleatórios por seed, girando levemente.
- Impact frame: inverta cores de **uma área** por 2 frames + tremor de 6 px; flash branco apenas parcial.
- Fundo: gradiente pintado + nuvens em camadas com parallax.
- Opção paga (com OK): gerar keyframes com modelo de imagem e animar por partes — ver regras de custo do master.

## Armadilhas
- Nada de personagens/estéticas de obras específicas (Naruto, Ghibli etc.); "anime" é a linguagem, não a franquia.
- Fotossensibilidade: sem flashes de tela cheia em sequência (máx. 3 por segundo e não em tela cheia).
- Boca "cantando" ou tremendo parece erro — prefira expressões estáticas que trocam por pose.

## Bastões
Linhas de velocidade convergem no centro (sai); impact frame que revela o próximo estilo (entra).

## Prompt-semente
"Trailer de <N> s em linguagem de anime original (sem imitar obras existentes) sobre <tema>: cel-shading 2 tons, linhas de velocidade, closes nos olhos, cortes rápidos no beat, impact frames localizados, título final. Personagens próprios desenhados em código."

**Status**: v2 (09/11/2026) aprovada em 2 rodadas de crítica contra referências da coleção. Código: `assets/kit2/src/b/v2.tsx` (cena `AnimeV2`).

**Lições do teste**: v1 tinha personagem desenhado à mão (fraco). v2: cidade à noite com lua e chuva, títulos com brilho, painéis diagonais com aura ("criador × render"), impact frame; o protagonista é footage real em duotone (política de personagens de `quality.md`).
