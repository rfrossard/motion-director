# Screencast com zoom automático (`screencast`)

**Look**: gravação **real** da tela, apresentada dentro de uma moldura (janela com sombra sobre fundo gradiente/papel de parede), câmera que dá **zoom suave onde o cursor clica** e acompanha o movimento, cursor maior e suavizado, cliques com anel discreto, digitação acelerada, legendas/anotações curtas. Ritmo calmo (movimentos de 1,5–3 s, ease-in-out).
**Usos**: tutoriais de software, demos de produto/protótipo real, "como eu faço X", onboarding, bug reports bonitos.
**Exemplos**: "Mac desktop teaser for a notch browser" (@jake11moran — câmera contínua sobre o desktop, metade da velocidade padrão, motion blur), "Promo with real product screenshots" (@zigapoto), "Remotion showreel of a developer portfolio site" (@wani_shola).

## Pipeline
1. **Gravar**: QuickTime/`screencapture -v` (macOS) ou Playwright gravando a página (`recordVideo`) **com log de eventos** (timestamp, x, y, tipo de clique/tecla). Sem log, detecte cliques pelo cursor visível (difícil) — prefira gravar com log.
2. **Plano de câmera** a partir dos eventos: para cada clique, um alvo (centro + zoom 1,6–2,2×); suavize com mola/criticamente amortecido; nunca mais de 1 zoom por 2 s; volte a 1× em pausas.
3. **Render** (Remotion): `<OffthreadVideo>` dentro de um container com `transform: translate/scale` vindo do plano; cursor redesenhado por cima (posição do log, suavizada) com tamanho constante na tela.
4. Acelere trechos mortos (2–4×) com indicador "⏩"; digitação a 1,5×.
5. Anotações: setas/rótulos que aparecem no clique; legenda da narração.

## Técnica
```tsx
const cam = cameraAt(frame / fps, events);          // {x, y, z} suavizado
<div style={{transform: `translate(${960 - cam.x * cam.z}px, ${540 - cam.y * cam.z}px) scale(${cam.z})`, transformOrigin: '0 0'}}>
  <OffthreadVideo src={staticFile('rec.mp4')} />
</div>
// texto embaçado sob zoom: grave em resolução nativa (Retina) e não use will-change no container escalado
```

## Armadilhas
- Grave em resolução alta; zoom de 2× em gravação 1080p fica mole.
- Esconda dados sensíveis (e-mails, tokens, nomes) antes de exportar — blur por região/tempo.
- Movimentos rápidos demais enjoam: limite a velocidade da câmera.

## Bastões
Zoom out até a janela virar um objeto (cartão) que segue para o próximo estilo; ou o próximo estilo nasce de dentro de um elemento clicado.

## Prompt-semente
"Transforme esta gravação de tela (com log de cliques) em um tutorial de <N> s: moldura de janela sobre fundo limpo, zoom suave em cada clique e acompanhamento do cursor, cursor grande suavizado, trechos mortos acelerados, anotações curtas e legendas. Movimentos de 1,5–3 s, sem cortes bruscos."

**Status**: testado no vídeo "Biblioteca de estilos" (08/11/2026). Código: `assets/kit2/scripts/record_screencast.mjs + engines/screencast/app.html` · cena `ScreencastS`.

**Lições do teste**: gravação REAL via Chrome headless + CDP com log de cursor; zoom 1,7× em torno de cada clique e cursor redesenhado; `Freeze` no último quadro.

**Auditoria (09/11/2026)** (composição / ofício / movimento / legibilidade / fidelidade): 4 / 4 / 4,5 / 4 / 4. Passa.
