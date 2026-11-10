---
name: editorial-archival-edit
description: "Editar um vídeo já gravado (talking head, vlog, entrevista) em estilo editorial de arquivo: preto e branco claro, grão orgânico leve, bloom suave, colagens de material de arquivo, tipografia cinética com 3 famílias, stop-motion seletivo, texto atrás da pessoa e telas divididas que deslizam. Feito em Remotion sobre o vídeo original. Use quando pedirem 'edição editorial', 'archival look', 'estilo documentário de arquivo', 'texto atrás de mim', 'edita meu vídeo com grão e P&B'."
---

# Editorial archival edit

Edição de vídeo real, não animação do zero. O material do usuário é a base: a fala, as pausas, a ordem dos clipes, a duração, a proporção e o som original **ficam como estão**, a menos que o usuário peça outra coisa. O estilo vem por cima.

Reescrito para Remotion a partir da gramática do skill `editorial-film-edit`, distribuído por @kaye_creatives no tutorial do Higgsfield. Valem as regras do `remotion-video-studio`: licença Remotion para empresas, chaves só no `.env`, nunca dizer "renderizado" sem renderizar e nunca inventar dados. Converse no idioma do usuário.

Antes de construir, leia `references/look.md` (parâmetros do visual) e `references/remotion-recipes.md` (componentes).

## 0 · Ambiente (antes de prometer um MP4)

Verifique e diga numa linha o que tem e o que falta:
- `ffprobe` no material: duração, fps, resolução, codec e áudio. O projeto herda **o fps e a resolução do original**, sem upscale.
- Node 22+, Remotion já instalado ou instalável, e as fontes (ver `look.md`).
- Recorte da pessoa (matte), necessário para texto atrás dela. Prefira o skill `object-separation` (SAM 2 local, com máscara por frame). As alternativas são `rembg` (por frame, lento) e MediaPipe Selfie Segmentation. Se nada roda, avise e ofereça a versão sem texto atrás.
- Som: para foley e SFX nos inserts, use o skill `sound-effects`, que tem biblioteca CC0 e mix medido. Ele preserva a fala original.
- Transcrição: whisper.cpp via `@remotion/install-whisper-cpp`, com modelo multilíngue para pt-BR.

Se faltar algo essencial, diga exatamente o que é e o caminho mínimo para resolver. Não entregue HTML, código ou plano como se fosse vídeo pronto.

## 1 · Leitura do material (autônoma)

1. Transcreva com timestamps por palavra e corrija contra o áudio. Se uma frase importante estiver ininteligível, pergunte; não invente.
2. Monte o **mapa de tempo**: `fonte → programa`, com os cortes já embutidos entre takes. Ao voltar de um B-roll, nunca mostre frames soltos do take vizinho.
3. Tire frames a cada ~2 s e olhe: onde está o rosto, onde há espaço negativo para texto, onde a pessoa gesticula.
4. Escreva a **direção** num parágrafo e mostre ao usuário: metáforas de arquivo para *este* tema, quais palavras viram tipografia e onde entram splits. Depois siga montando, perguntando só o que bloqueia.

## 2 · Gramática (o que define o estilo)

- **Grade:** P&B claro e neutro (pretos levantados, brancos que respiram). Nada de P&B "esmagado". Bloom suave só nas altas luzes, grão orgânico novo a cada frame e ancorado na imagem, gate weave sutil e vinheta leve.
- **Inserts de arquivo:** fotos ou trechos de época relevantes ao tema, tratados todos iguais (mesmo grade, grão e idade de cópia), para parecer um único acervo. Colagens expressivas: recortes com borda de papel, retícula, sobreposições e máscaras. Use CRT, lab e máquinas só quando o tema for tecnologia; escolha os objetos pelo assunto.
- **Tipografia:** só três papéis e três famílias.
  1. **Grotesca** (fala e palavras de peso).
  2. **Serifa display** (italic para acentos `*assim*` e números grandes).
  3. **Mono** (fontes, datas e créditos).
  Entradas suaves: expo-out com um pouco de blur e subida, sem overshoot. Legendas palavra a palavra no tempo da fala.
- **Stop-motion seletivo:** só algumas camadas (um recorte, uma palavra) animam "on twos" (8–12 fps), enquanto o vídeo e o grão seguem no fps cheio.
- **Texto atrás da pessoa:** a palavra fica entre o fundo e o recorte da pessoa. Use em 2 a 4 momentos-chave, não no vídeo todo.
- **Split screen:** só aparece junto com quem apresenta. Entra empurrando suave (~0,4 s, sine in-out). A pessoa é recortada de novo, nunca espremida. O insert mantém o próprio enquadramento.
- **Densidade:** em vídeos longos, menos inserts e mais tempo de leitura. Deixe a pessoa respirar entre os gráficos.

Proibido: crossfades genéricos, flashes de tela inteira, zoom punch-in no rosto sem motivo, glitch RGB, LUTs "cinema" alaranjados, fontes além das três e texto sobre o rosto ou a boca.

## 3 · B-roll e direitos

- Prefira o material do usuário. Depois, acervos com licença clara: Internet Archive (Prelinger, domínio público), Wikimedia Commons, Library of Congress, NASA, Pexels e Pixabay. Guarde a origem e a licença de cada um em `CREDITS.md`.
- Pinterest e Instagram servem como referência de estilo, nunca como fonte de B-roll. Não diga que viu um link que não conseguiu abrir.
- Imagem gerada por IA é opcional, só com orçamento combinado e confirmação de custo. Nunca a apresente como registro histórico.
- Nomes, números, interfaces e citações na tela precisam bater com a fala.

## 4 · Testes curtos antes do export completo

Renderize trechos de 3 a 5 s de: um B-roll claro, um escuro, o grade P&B, uma palavra grande, um split e um texto atrás da pessoa. Olhe as bordas da máscara, a legibilidade no tamanho final e se o grão parece filme e não um adesivo por cima. Ajuste e só então exporte tudo.

Trabalhe em camadas separadas (fonte → inserts → texto → máscaras → som). Em revisões, **salve a versão anterior** como `v<N>` antes de mexer.

## 5 · Conferência e entrega

- Assista ao export inteiro e confira:
  - movimento do grão e do texto, os dois lados de cada transição e as bordas das máscaras;
  - sincronia de fala e legenda;
  - ausência de frames pretos, congelados ou esticados e de barras;
  - limites das legendas.
- `ffprobe`: duração, fps e resolução iguais às do original (salvo pedido).
- Contact sheets ajudam, mas não substituem assistir. Não declare como aprovado um teste que não rodou.
- Entregue: o MP4, o projeto Remotion editável (com assets ou lista exata de dependências), `CREDITS.md` e uma lista curta do que mudou e do que ficou limitado.
  - Se houver música, entregue também uma versão sem ela.
  - Se só a imagem mudou, mantenha o som aprovado.
- Guarde os parâmetros de estilo (`look.json`) separados das mídias e timecodes do projeto, para reutilizar no próximo vídeo.

## Portão de qualidade (biblioteca local; obrigatório)
Este skill faz parte da biblioteca coordenada pelo `motion-director`. Mesmo chamado direto, siga `~/.claude/skills/motion-director/references/quality.md`:
1. Parta do padrão-ouro do estilo `archival`: `~/.claude/skills/motion-director/assets/kit2/src/b/Archival.tsx`. Não comece do zero.
2. Antes de codar, monte uma folha de referência do estilo e liste os traços obrigatórios.
3. Faça no mínimo 2 rodadas de crítica com stills, com todos os critérios (composição, ofício, movimento, legibilidade, fidelidade) ≥ 4.
4. Aplique as regras duras: pessoas nunca desenhadas do zero em SVG (footage real → Open Peeps → abstração), composição cheia e legibilidade mínima de 22 px a 1080p.
5. Antes de entregar, rode a auditoria do MP4 (`assets/kit2/scripts/audit.py extract` → notas → `check`).

Específico deste estilo:
- footage real é o protagonista; nada de pessoas desenhadas em SVG
- legendas e texto atrás da pessoa legíveis (≥ 22 px a 1080p), nunca cortados
- crédito da fonte das imagens sempre na tela
