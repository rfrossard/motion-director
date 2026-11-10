# Guia de estilo: flat science explainer

## 1. Princípios

1. **Formas geométricas simples:** círculos, pílulas, retângulos arredondados e blobs. Cantos sempre arredondados. Nada de traço à mão.
2. **Valor antes de cor:** cada objeto tem 3 tons do mesmo matiz (base, sombra e luz). A sombra é uma forma recortada, sem gradiente difuso.
3. **Fundo profundo, acento vivo:** o fundo tem baixa luminosidade e alta saturação. O objeto principal leva o acento complementar.
4. **Luz que emite:** estrelas, células e telas brilham com um halo radial (glow) suave em `mix-blend-mode: screen`.
5. **Nada está parado:** tudo flutua, respira, pisca ou gira devagar, mesmo nas cenas "estáticas".
6. **Escala como narrativa:** a transição favorita é o zoom contínuo entre escalas.

## 2. Paletas originais

Cada paleta tem fundo (2 tons para o gradiente), meio, acento principal, acento secundário, luz e pele/personagem.

| Paleta | bg-top | bg-bottom | mid | accent | accent-2 | light | character |
|---|---|---|---|---|---|---|---|
| **Abissal** (oceano, biologia) | `#0B1B3F` | `#06102A` | `#1F4E8C` | `#FF7A3D` | `#2EE6C5` | `#E8F4FF` | `#FFC94D` |
| **Nebulosa** (espaço, física) | `#1A1446` | `#0C0A26` | `#4B2C8F` | `#FF4F8B` | `#FFC23D` | `#F4EEFF` | `#7FE3FF` |
| **Bioluminescente** (corpo, células) | `#2A0E2E` | `#14061A` | `#7A1E4F` | `#FF5D5D` | `#5DF2FF` | `#FFE9F0` | `#B8F25D` |
| **Savana Solar** (Terra, clima, história) | `#3B1F4A` | `#1E1030` | `#C2552E` | `#FFB23D` | `#3DD6A0` | `#FFF4DE` | `#FF8A5B` |
| **Ártico** (tecnologia, dados, IA) | `#0E2A3A` | `#071722` | `#1F6F8B` | `#FF6B3D` | `#9BF0FF` | `#F0FBFF` | `#FFD86B` |

Regras de uso:
- **Sombra:** escureça a base em ~18% de luminosidade e gire o matiz ~8° em direção ao azul ou violeta.
- **Luz de borda:** clareie a base em ~15% e use uma faixa fina no lado da fonte de luz.
- **Proporção:** ~70% fundo e meio, ~20% personagens e objetos, no máximo 10% de acento.
- Para criar uma paleta nova, mantenha o fundo com L < 20% e S > 50%, e escolha o acento perto do complementar do fundo.

## 3. Formas e sombreamento

- **Sombra cel:** desenhe a forma base. Por cima, desenhe a mesma forma deslocada (ex.: `dx=+0.15r`, `dy=+0.15r`) com a cor da sombra, recortada por `clipPath` da forma base.
- **Brilho especular:** um pequeno círculo ou elipse clara, em 10–20% do raio, no quadrante da luz.
- **Glow:** um `radialGradient` da cor de luz com opacidade 0,5 → 0, num raio de 2–3× o objeto.
- **Profundidade atmosférica:** as camadas de trás ficam mais próximas da cor do fundo (menos contraste) e um pouco menores.

## 4. Personagens (sempre originais)

- O corpo é uma pílula ou um blob, com no máximo 2 membros simples (bastões arredondados) ou nenhum.
- Olhos grandes, de branco + pupila, sem boca ou com uma boca mínima. A expressão vem das pálpebras (uma forma que corta o olho) e da inclinação do corpo.
- Tamanho pequeno em relação ao cenário, porque eles são "testemunhas" da escala.
- Defina um mascote por projeto (forma, cor e um traço distintivo). Ele não pode ser um pássaro de bico triangular nem lembrar os personagens do canal original.

## 5. Movimento

| Elemento | Movimento | Parâmetros típicos (30 fps) |
|---|---|---|
| Objeto em repouso | flutuação senoidal | amplitude de 4–10 px, período de 3–5 s, fase por `random(seed)` |
| Personagem | respiração (scaleY 1 → 1,03) e piscar | piscar a cada 3–6 s, por 4 frames |
| Entrada | `spring` com overshoot e squash & stretch | `damping` de 10–14, `mass` de 0,6–1 |
| Saída | escala → 0 com `Easing.in(Easing.back(1.5))` | 8–12 frames |
| Estrelas e partículas | cintilar (opacidade) e deriva lenta | 3 camadas, com velocidades 0,2× / 0,5× / 1× |
| Câmera | parallax por camada | a camada de frente move-se 1×, o meio 0,5× e o fundo 0,15× |
| Escala | zoom exponencial contínuo | `scale = Math.pow(k, t)`, sem nunca cortar |
| Stagger | grupos aparecem em cascata | 2–4 frames entre os elementos |

- O ritmo segue a narração: a ação principal cai na palavra-chave, não no início da frase.
- Evite movimentos lineares. Use sempre easing ou spring.

## 6. Texto na tela

- Pouco texto: palavra-chave, número ou rótulo.
- Títulos em Fredoka ou Baloo 2, peso 600–700. Rótulos em Nunito 700, em caixa alta e com tracking leve.
- Rótulos com linha guia fina (aqui o traço é permitido, porque é UI e não ilustração) e uma bolinha na ponta.

## 7. Acabamento

- Granulação: um `feTurbulence` com `baseFrequency` entre 0,8 e 1,0, por cima de tudo, com opacidade de 0,05–0,08 e `mix-blend-mode: overlay`.
- Vinheta: um radial escuro nas bordas com opacidade de 0,25–0,35.
- Transições: zoom de escala, "match cut" de forma (um círculo vira um planeta, que vira uma célula) ou um wipe orgânico com blob. Evite crossfade genérico.
