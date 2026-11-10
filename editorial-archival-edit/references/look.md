# Look: parâmetros de partida

Valores iniciais. Ajuste olhando os testes, não às cegas. Guarde a versão final em `look.json` no projeto.

## Grade P&B "claro"

| Parâmetro | Valor inicial | Nota |
|---|---|---|
| Saturação | 0 | P&B neutro, sem tom sépia (no máximo um leve quente, de +2 a 3%, se o usuário quiser) |
| Ponto preto | 6–8% (lift) | pretos leitosos, nunca 0 |
| Ponto branco | 94–96% | brancos sem clipar |
| Contraste | 1,05–1,12 | suave |
| Exposição | +0,05 a +0,15 | "bright" B&W |
| Inserts de arquivo | mesmo grade, mais contraste local (1,15) e um pouco mais de grão | une o acervo |

Em CSS (Remotion): `filter: grayscale(1) contrast(1.08) brightness(1.08)`, com um `linear-gradient` cinza escuro em `mix-blend-mode: lighten` para levantar os pretos.

## Bloom e halação

- Só nas altas luzes: limiar ~0,75 de luminância e joelho suave.
- Raio ~1,5–2,5% da largura e intensidade de 0,25–0,4.
- Em Remotion, duplique a camada de vídeo com `filter: brightness(1.6) contrast(2.2) blur(18px)` (isso isola as altas luzes) e aplique em `mix-blend-mode: screen` com opacidade de 0,25–0,35.
- Halação: o mesmo truque, mais largo (blur de 40 px) e com opacidade de 0,1.

## Grão orgânico

O problema clássico é o grão "adesivo": um padrão parado ou deslizando por cima da imagem. Para evitar:
- **Novo a cada frame:** `seed` deriva do frame, sem repetir em ciclos curtos (nada de `frame % 8` aqui; use `frame % 997` só para vídeos com menos de ~40 s, ou `frame` direto).
- **Fino:** `baseFrequency` de 0,85–1,1 e `numOctaves` 2. Opacidade de 0,05–0,09 em `overlay`.
- **Menos nos extremos:** visível nos meios-tons e quase nada nos pretos e brancos (máscara por luminância, ou opacidade menor).
- **Ancorado:** se houver gate weave, aplique o mesmo deslocamento ao grão.

## Idade de cópia (só nos inserts)

- Gate weave: de 0,3 a 0,8 px de deslocamento aleatório por frame (`random(\`w${frame}\`)`).
- Poeira: de 0 a 3 pontos ou fibras por frame, com duração de 1 frame. Risco vertical raro (1 a cada ~4 s).
- Flicker de exposição: de ±1,5% a 2%, com ruído suave e sem piscar a tela toda.
- Vinheta: radial de 0,2–0,3.

## Tipografia (três famílias)

| Papel | Uso | Grátis/local | Sistema (Mac) |
|---|---|---|---|
| Grotesca | legendas, palavras de peso (700–800), UI | Inter, Archivo | Helvetica Neue |
| Serifa display | acentos em itálico, números grandes, títulos | Bodoni Moda, Playfair Display | Didot, Bodoni 72 |
| Mono | fontes, datas, créditos, máquina de escrever | IBM Plex Mono, JetBrains Mono | Menlo, SF Mono |

- O peso pesado é um *peso* da grotesca, não uma quarta família.
- Nas legendas, a grotesca fica em branco 700 com sombra suave. A palavra de acento entra em serifa itálica a 1,2× do tamanho.
- Números grandes vão em serifa display. Abaixo deles: subtítulo em itálico (0,2×), qualificador em grotesca caixa-alta com tracking de 0,16em (0,06×) e fonte em mono (0,05×, opacidade de 0,7).
- Fontes de dados em mono, pequenas e discretas.

## Movimento do texto

- **Entrada padrão "soft":** em 0,32 s, expo-out em `y` (de 0,32em a 0), `blur` (de 9 px a 0) e opacidade (rápida, cerca de 4,5× a velocidade).
- Outras entradas, por ordem de preferência: `rise`, `wipe` por máscara, `type` (máquina de escrever, com mono), `draw` (para setas) e `flicker` (raro).
- **Deriva contínua:** palavras grandes derivam devagar durante toda a vida da camada (0,02–0,05em/s) e atravessam cortes sem reiniciar.
- **Stop-motion seletivo:** quantize o tempo *daquela camada* para 8, 10 ou 12 fps: `tq = Math.floor(t * 12) / 12`. Vídeo e grão continuam no fps cheio.
- **Saídas:** corte seco ou blur curto (0,15 s). Nunca um fade longo.

## Composição

- O rosto é zona proibida para texto: deixe uma margem de ~8% ao redor.
- Respeite as safe zones da plataforma no vertical (interface do Instagram e do TikTok embaixo e à direita).
- Texto atrás da pessoa funciona com palavras grandes (≥ 18% da altura), parcialmente encobertas pela cabeça ou pelos ombros, mas ainda legíveis.
- Split screen: o insert ocupa 50% (às vezes 40%). Divisória seca, sem borda. Quem apresenta é recentralizado no seu painel.

## Som

- Fala original intocada, com normalização final em −14 LUFS para redes.
- Música (se houver) abaixada sob a fala (ducking de −12 a −18 dB) e sem letra.
- Foley sutil nos inserts (projetor, papel, obturador) só se houver arquivos livres.
