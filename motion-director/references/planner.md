# Planner — qual estilo para cada trecho

## 1. Classifique cada trecho do roteiro

| Tipo de conteúdo | Sinais no roteiro |
|---|---|
| `pergunta` | hipótese, provocação, gancho |
| `conceito` | "o que é", mecanismo, analogia |
| `processo` | etapas, fluxo, "como funciona" |
| `numero` | uma métrica, comparação, tendência |
| `cronologia` | datas, eras, "antes e depois" |
| `lugar` | cidades, rotas, mapas |
| `fala` | entrevista, depoimento, vlog (há footage) |
| `produto` | UI, app, demo, tutorial de software |
| `historia` | personagens, fábula, emoção |
| `celebracao` | conquista, marco, aniversário |
| `anuncio` | lançamento, CTA, convite |
| `ambiente` | loop, fundo, transição contemplativa |
| `noticia` | vários itens curtos em sequência |

## 2. Afinidade (3 = ótimo, 2 = bom, 1 = possível; vazio = evite)

| estilo \ tipo | perg | conc | proc | num | crono | lugar | fala | prod | hist | celeb | anunc | amb | notic |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| led | 3 | | | 1 | | | | | | 2 | 3 | 1 | 2 |
| flat | 2 | 3 | 2 | 1 | 1 | 1 | | | 2 | | | 2 | |
| collage | 1 | | 1 | | 2 | 1 | 1 | 1 | 3 | 2 | 2 | 1 | |
| ink | | 1 | | | 3 | 1 | | | 2 | | | 1 | |
| journey | | 2 | 3 | | 1 | | | 2 | 1 | | | 1 | |
| uimorph | | | 2 | 1 | | | 1 | 3 | | | 2 | 1 | |
| demo | | | 2 | | | | | 3 | | | 1 | | |
| datastory | | 1 | | 3 | 2 | | | | | | | | 1 |
| stroke | | 3 | 2 | 1 | | | | 1 | | | | | |
| archival | | | | | 2 | | 3 | | 2 | | | | 1 |
| extrude3d | 1 | | | | | | | 1 | | 2 | 3 | 2 | |
| hype | 2 | | | 1 | | | | 2 | | 2 | 3 | | 1 |
| pixel | 1 | 1 | 1 | | 1 | 1 | | | 3 | 2 | 1 | 3 | |
| blender3d | | 1 | | | 3 | 3 | | 2 | 2 | | 1 | 2 | |
| creator | 2 | | | | | | 3 | 1 | 1 | 1 | 2 | | 2 |
| geomap | | | 1 | 1 | 2 | 3 | | | 2 | | | 1 | 1 |
| manim | | 3 | 2 | 3 | | | | | | | | | |
| sand | | | | | 3 | 1 | | | 3 | 2 | | 2 | |
| mosaic | 1 | | | | | | | | 2 | 2 | 2 | 3 | |
| toon3d | | | | 1 | | | | 1 | 1 | 3 | 2 | | |
| anime | 2 | | | | | | | | 3 | 2 | 3 | | |
| sketch | 1 | 3 | 3 | 2 | 1 | 1 | 1 | 1 | 1 | | | | 1 |
| particles | 1 | 2 | | 2 | | 1 | | | 1 | | 1 | 3 | |
| shadow | | | | | 2 | | | | 3 | | | 2 | |
| comic | 2 | 2 | 1 | | 1 | | 1 | | 3 | 1 | 1 | | 1 |
| news | 1 | | | 2 | 1 | | 1 | | | | 2 | | 3 |
| screencast | | | 2 | | | | 1 | 3 | | | | | |

## 3. Ajustes da pontuação

- **+2** se o estilo já foi escolhido como **base** do vídeo (coesão).
- **+1** por material do usuário que o estilo aproveita (footage → `archival`/`creator`; gravação de tela → `screencast`; dados → `datastory`/`manim`).
- **−2** se o tom pedido conflita (ex.: `toon3d`/`anime` para "sóbrio"; `sand`/`shadow` para "energético").
- **−3** se um perfil de marca proíbe (ex.: Hub → `pixel`, `mosaic` por usar quadrados).
- **−1** por custo `$$$` quando o prazo é curto.
- Empate → o de menor custo.

## 4. Orçamento de variedade

| Duração | Estilos |
|---|---|
| até 30 s | 1 (+ 1 acento) |
| 30–90 s | 1 base + até 2 acentos |
| 90 s – 5 min | 1 base + até 3 acentos |
| catálogo/reel de estilos | sem limite, mas um bastão comum |

Escolha primeiro o **estilo-base** (maior soma no vídeo todo), depois os acentos só onde a afinidade do base for ≤ 1.

## 5. Saída para o usuário

```
| # | trecho (tempo) | tipo | estilo | por quê (1 linha) | passagem para o próximo |
```
+ "Alternativas: (a) tudo em <base> — mais coeso; (b) trocar X por Y — mais energético."

## Prontidão de qualidade (entra na pontuação)
- Estilo com cena de ouro aprovada no portão (`quality.md` §1): **+1** na pontuação. É mais rápido e mais seguro.
- Estilo marcado ⚠ (hoje: `broll`, `pixel`) ou sem cena de ouro (reserva): **−1**. Se for escolhido, reserve tempo para 2 rodadas de crítica e diga ao usuário.
- Estilo que pede pessoas: só com footage real, Open Peeps ou abstração assumida (`quality.md` §4.1). Sem um desses, não escolha.
- Estilo com fórmulas: só com tipografia matemática (`tex2svg.mjs`).
