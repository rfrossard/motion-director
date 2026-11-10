# Matemático — Manim (`manim`)

**Look**: fundo escuro, tipografia LaTeX, equações que se transformam termo a termo (TransformMatchingTex), gráficos e geometria precisos, cores semânticas consistentes (uma cor por variável), câmera que dá zoom no detalhe.
**Usos**: aulas, conceitos técnicos, finanças/estatística, lógica, provas visuais, papers.
**Exemplos**: "Manim lesson on derivatives" (@LinearUncle, 7,5 min com edge-tts), "Riemann hypothesis explainer" (@hyuki), "Gradient descent 3D explainer" (@anirockshady). Hermes tem o skill `manim-video`.

## Instalação (Manim Community)
```bash
python3 -m venv .venv && . .venv/bin/activate
pip install manim            # requer ffmpeg, cairo, pango (brew install cairo pango) e LaTeX (MacTeX/BasicTeX) para MathTex
manim --version
```

## Técnica
```python
from manim import *
class Derivada(Scene):
    def construct(self):
        eq = MathTex(r"f'(x)", "=", r"\lim_{h\to 0}", r"\frac{f(x+h)-f(x)}{h}")
        eq.set_color_by_tex("h", ORANGE)
        self.play(Write(eq)); self.wait(0.5)
        ax = Axes(x_range=[-1, 3], y_range=[-1, 9]).to_edge(DOWN)
        g = ax.plot(lambda x: x**2, color=BLUE)
        self.play(eq.animate.to_edge(UP), Create(ax), Create(g))
        # tangente que desliza com um ValueTracker
        x = ValueTracker(0.5)
        tan = always_redraw(lambda: ax.get_secant_slope_group(x.get_value(), g, dx=0.001, secant_line_length=3, secant_line_color=ORANGE))
        self.add(tan); self.play(x.animate.set_value(2.5), run_time=3)
```
```bash
manim -qh --fps 30 -r 1920,1080 cena.py Derivada   # saída em media/videos/...
```
- Narração: Piper/edge-tts por cena; sincronize `self.wait()` com a duração real de cada áudio (meça e gere o script com as durações).
- Ritmo: uma ideia por cena; pausas de 0,5–1 s após cada transformação.

## Armadilhas
- Sem LaTeX instalado, `MathTex` falha — use `Text` ou instale BasicTeX.
- Cores semânticas: mantenha as mesmas cores para as mesmas variáveis no vídeo todo.
- Confira cada conta e definição; erros matemáticos destroem a credibilidade.

## Bastões
Uma equação se transforma numa forma (círculo/linha) que é o bastão; o gráfico encolhe até virar um ponto.

## Prompt-semente
"Use Manim (Community) para explicar <conceito> para <público>: uma ideia por cena, equações que se transformam termo a termo, cores fixas por variável, exemplo numérico, pausas para pensar, narração <TTS> sincronizada pela duração real dos áudios. 1080p30."

**Status**: v2 (09/11/2026), aprovada em 2 rodadas de crítica contra o padrão 3Blue1Brown. Código: `assets/kit2/engines/manim/mola2.py` (`Mola2`); fórmulas em `engines/manim/tex/formulas.json` → `scripts/tex2svg.mjs`.

**Lições do teste**:
- A v1 usava a fórmula em fonte mono (`MarkupText`). Ficou com cara de terminal, e o `Write` rabiscava.
- A v2 tipografa com MathJax → SVG (sem instalar LaTeX) e carrega com `SVGMobject(..., stroke_width=0)`. Cada variável tem cor fixa via `\color{#hex}`, o que permite achar subpartes pela cor (ex.: chave sob os caminhos verdes do decaimento).
- `TransformMatchingShapes` entre EDO e solução embaralha os glifos; mostre a derivação em linhas (EDO ⇒ solução).
- `DecimalNumber` exige LaTeX; use `Text` com `always_redraw`.
- A cena precisa de um sistema físico sincronizado com o gráfico, do envelope tracejado, de um seletor do parâmetro e das curvas-fantasma.
- Ajuste a duração ao slot com `self.wait(max(0.5, DUR − self.time))` e imprima o instante do recolhimento para checar contra o cartão de invocação.
