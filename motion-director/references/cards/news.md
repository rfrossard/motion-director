# Telejornal / boletim (`news`)

**Look**: linguagem de TV: vinheta de abertura com faixas que varrem a tela, "lower thirds" (tarja com nome/título), letreiro (ticker) contínuo no rodapé, relógio/data, numeração de blocos ("3 de 7"), cartelas de manchete, mapa/gráfico de apoio, transições com "wipe" de faixa colorida.
**Usos**: recaps semanais, resumo de notícias de um tema, boletins automáticos (ex.: todo dia/toda semana), "o que aconteceu em…", recap da família/viagem em tom divertido.
**Exemplos**: "Steam new-release news roundup" (@gigabit_million — configurado para rodar toda manhã), "LLM progress in 2026, voice-prompted" (@nummanali).

## Estrutura
1. Vinheta (2–3 s) com nome do boletim e data.
2. Escalada: 3–5 manchetes em 1 linha cada, no beat.
3. Blocos: para cada item — cartela (título + fonte), 1 visual (imagem/gráfico/screenshot com licença), 1–2 frases, tarja.
4. Encerramento: "até a próxima" + data da próxima edição.

## Técnica (Remotion, alimentado por dados)
```ts
// props: { edicao: string, data: string, itens: [{titulo, resumo, fonte, url, imagem?}] }  (Zod)
// composição gerada a partir da lista: duração = vinheta + Σ(blocos) + encerramento
// ticker: texto contínuo com translateX = -(frame * px_por_frame) % largura
```
- Automação: um script coleta os itens (RSS/APIs), resume com fonte, gera o JSON de props e roda `npx remotion render`. Agende com o skill `schedule`/`loop` se o usuário pedir recorrência.
- Narração opcional (Piper/ElevenLabs) por bloco; legenda sempre.

## Armadilhas
- **Toda notícia com fonte** na tela e no `CREDITS.md`; nada de resumir além do que a fonte diz.
- Imagens de notícias têm direitos — use screenshots próprios, ícones, gráficos gerados, ou imagens com licença.
- Não imite a identidade de emissoras reais (vinhetas, logos, apresentadores).

## Bastões
A faixa da vinheta varre a tela (sai/entra); o ticker acelera e vira uma linha que segue para o próximo estilo.

## Prompt-semente
"Boletim em vídeo de <N> s sobre <tema/período>, com linguagem de telejornal original: vinheta, escalada de manchetes, blocos com cartela/visual/tarja/fonte, ticker no rodapé, encerramento. Gere a partir de um JSON de itens com fonte; legendas sempre."

**Status**: testado no vídeo "Biblioteca de estilos" (08/11/2026). Código: `assets/kit2/src/b/ch4.tsx` · cena `NewsS`.

**Lições do teste**: vinheta de faixas, escalada, blocos com tarja e fonte, ticker e relógio; esconda a tarja do bloco quando o cartão aparecer.

**Auditoria (09/11/2026)** (composição / ofício / movimento / legibilidade / fidelidade): 4 / 4 / 4 / 4 / 4,5. Passa. Os rótulos pequenos da tarja estão no limite (≥ 22 px).
