from manim import *
import numpy as np

LAR = "#FF6200"
config.background_color = "#0b0d12"

def mola(t, z, w=8.0):
    if z >= 1:
        return 1 - np.exp(-w * t) * (1 + w * t)
    wd = w * np.sqrt(1 - z * z)
    return 1 - np.exp(-z * w * t) * (np.cos(wd * t) + (z * w / wd) * np.sin(wd * t))

class Mola(Scene):
    def construct(self):
        eq = MarkupText(
            'x(t) = 1 − e<sup>−ζωt</sup> [ cos(ω<sub>d</sub>t) + <span fgcolor="#FF6200">ζ</span>ω/ω<sub>d</sub> · sin(ω<sub>d</sub>t) ]',
            font="Menlo", font_size=30)
        eq.to_edge(UP, buff=0.6)
        sub = Text("a mola que move cada animação desta biblioteca", font="Helvetica Neue", font_size=26, color=GRAY_B).next_to(eq, DOWN, buff=0.3)
        self.play(Write(eq), run_time=2.2)
        self.play(FadeIn(sub, shift=UP * 0.2))
        ax = Axes(x_range=[0, 1.2, 0.2], y_range=[0, 1.6, 0.4], x_length=7.2, y_length=3.8,
                  axis_config={"color": GRAY_C, "include_tip": False}).shift(LEFT * 1.6 + DOWN * 0.9)
        alvo = DashedLine(ax.c2p(0, 1), ax.c2p(1.2, 1), color=GRAY_D)
        lx = Text("t (s)", font="Menlo", font_size=20, color=GRAY_B).next_to(ax.x_axis, DOWN, buff=0.15).align_to(ax.x_axis, RIGHT)
        z = ValueTracker(0.3)
        curva = always_redraw(lambda: ax.plot(lambda t: mola(t, z.get_value()), x_range=[0, 1.2], color=LAR, stroke_width=5))
        zlab = always_redraw(lambda: MarkupText(f'<span fgcolor="#FF6200">ζ</span> = {z.get_value():.2f}'.replace('.', ','), font="Menlo", font_size=34).next_to(ax, RIGHT, buff=0.5).shift(UP * 1.2))
        # a bola que segue a curva (vertical) — mostra o overshoot
        trilho = Line(ax.c2p(0, 0) + RIGHT * 11.4, ax.c2p(0, 1.6) + RIGHT * 11.4, color=GRAY_D)
        tt = ValueTracker(0)
        bola = always_redraw(lambda: Dot(trilho.get_start() + (trilho.get_end() - trilho.get_start()) * mola(tt.get_value(), z.get_value()) / 1.6, radius=0.16, color=LAR))
        self.play(Create(ax), Create(alvo), FadeIn(lx), run_time=1.2)
        self.add(curva, zlab, trilho, bola)
        for val, nota in [(0.3, "muito elástico"), (0.82, "overshoot mínimo\n(padrão do kit)"), (1.0, "amortecimento crítico")]:
            if abs(z.get_value() - val) > 1e-3:
                self.play(z.animate.set_value(val), run_time=1.6)
            n = Text(nota, font="Helvetica Neue", font_size=22, color=GRAY_A).next_to(zlab, DOWN, buff=0.3).align_to(zlab, LEFT)
            self.play(FadeIn(n, shift=UP * 0.15), run_time=0.4)
            tt.set_value(0)
            self.play(tt.animate.set_value(1.2), run_time=1.8, rate_func=linear)
            self.wait(0.4)
            self.play(FadeOut(n), run_time=0.3)
        self.play(z.animate.set_value(0.82), run_time=1.0)
        caixa = SurroundingRectangle(zlab, color=LAR, buff=0.15)
        self.play(Create(caixa)); self.wait(1.0)
        # saída: tudo se recolhe num ponto laranja (bastão)
        ponto = Dot(ORIGIN, radius=0.08, color=LAR)
        self.play(*[FadeOut(m) for m in [ax, alvo, lx, curva, zlab, trilho, bola, caixa, sub]], Transform(eq, ponto), run_time=1.2)
        self.wait(4.2)   # tempo do cartão de invocação (sobreposto no Remotion)
