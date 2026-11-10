# Mola v2 (09/11/2026), refeita no padrão 3Blue1Brown:
# - fórmulas tipografadas de verdade (MathJax → SVG via scripts/tex2svg.mjs, sem LaTeX instalado), variáveis com cor própria;
# - sistema físico (parede, mola, bloco) que oscila em sincronia com o gráfico;
# - EDO se transforma na solução; chave no termo de decaimento; envelope 1 ± e^(−ζωt) desenhado no gráfico;
# - seletor de ζ com curvas-fantasma dos valores anteriores; saída num ponto laranja (bastão).
from manim import *
import numpy as np

LAR, AZ, VD = "#FF6200", "#58C4DD", "#83C167"
TXT = "#F3F4F7"
config.background_color = "#0b0d12"
TEX = "manim/tex"
W = 8.0


def mola(t, z, w=W):
    if z >= 0.999:
        return 1 - np.exp(-w * t) * (1 + w * t)
    wd = w * np.sqrt(1 - z * z)
    return 1 - np.exp(-z * w * t) * (np.cos(wd * t) + (z * w / wd) * np.sin(wd * t))


def tex(name, h):
    m = SVGMobject(f"{TEX}/{name}.svg", height=h, stroke_width=0)
    return m


def zigzag(x0, x1, y, n=9, a=0.2):
    pts = [np.array([x0, y, 0]), np.array([x0 + 0.15, y, 0])]
    span = (x1 - 0.15) - (x0 + 0.15)
    for i in range(n):
        pts.append(np.array([x0 + 0.15 + span * (i + 0.5) / n, y + (a if i % 2 == 0 else -a), 0]))
    pts += [np.array([x1 - 0.15, y, 0]), np.array([x1, y, 0])]
    return VMobject(stroke_color=GREY_B, stroke_width=4).set_points_as_corners(pts)


class Mola2(Scene):
    def construct(self):
        # ---------- sistema físico ----------
        Y = -1.55
        parede = Line([-6.7, Y - 1.1, 0], [-6.7, Y + 1.1, 0], color=GREY_C, stroke_width=6)
        hach = VGroup(*[Line([-6.7, Y - 1.0 + i * 0.25, 0], [-6.95, Y - 1.2 + i * 0.25, 0], color=GREY_D, stroke_width=3) for i in range(9)])
        chao = Line([-6.95, Y - 0.5, 0], [-2.9, Y - 0.5, 0], color=GREY_D, stroke_width=3)
        X0, SPAN = -5.55, 1.55
        tt = ValueTracker(0)
        z = ValueTracker(0.3)
        bx = lambda: X0 + SPAN * mola(tt.get_value(), z.get_value())
        bloco = always_redraw(lambda: RoundedRectangle(corner_radius=0.08, width=0.9, height=0.9, fill_color=LAR, fill_opacity=1, stroke_width=0).move_to([bx() + 0.45, Y, 0]))
        mlab = always_redraw(lambda: Text("m", font="Helvetica Neue", font_size=30, weight=BOLD, color="#0b0d12").move_to([bx() + 0.45, Y, 0]))
        mol = always_redraw(lambda: zigzag(-6.7, bx(), Y))
        alvo_m = DashedLine([X0 + SPAN + 0.45, Y - 0.75, 0], [X0 + SPAN + 0.45, Y + 0.85, 0], color=GREY_B, dash_length=0.08).set_z_index(-1)
        alvo_l = Text("equilíbrio", font="Helvetica Neue", font_size=20, color=GREY_B).next_to(alvo_m, UP, buff=0.08)

        # ---------- equações ----------
        ode = tex("ode", 0.5).move_to([-3.2, 3.2, 0])
        self.play(Create(parede), Create(hach), Create(chao), run_time=0.8)
        self.add(mol, bloco, mlab)
        self.play(Write(ode), FadeIn(alvo_m), FadeIn(alvo_l), run_time=1.4)
        seta = Text("⇒", font="Helvetica Neue", font_size=40, color=GREY_B).move_to([-6.3, 2.1, 0])
        sol = tex("sol", 1.2).move_to([0.4, 2.1, 0])
        self.play(FadeIn(seta, shift=RIGHT * 0.2), Write(sol), run_time=1.6)
        # chave sob o termo de decaimento (os caminhos verdes da solução)
        verdes = VGroup(*[p for p in sol.family_members_with_points() if p.get_fill_color().to_hex().upper().startswith("#83C1")])
        chave = Brace(verdes, DOWN, buff=0.08, color=VD)
        cl = Text("decaimento", font="Helvetica Neue", font_size=24, color=VD).next_to(chave, DOWN, buff=0.08)
        wd = tex("wd", 0.5).move_to([3.6, 3.2, 0])
        self.play(GrowFromCenter(chave), FadeIn(cl, shift=UP * 0.1), FadeIn(wd, shift=UP * 0.1), run_time=0.9)

        # ---------- gráfico ----------
        ax = Axes(x_range=[0, 1.2, 0.2], y_range=[0, 1.8, 0.5], x_length=6.6, y_length=3.4,
                  axis_config={"color": GREY_C, "include_tip": False, "stroke_width": 2}).move_to([2.95, -1.5, 0])
        lx = Text("t", font="Helvetica Neue", font_size=24, slant=ITALIC, color=GREY_B).next_to(ax.x_axis, RIGHT, buff=0.12)
        ly = Text("x(t)", font="Helvetica Neue", font_size=24, slant=ITALIC, color=GREY_B).next_to(ax.y_axis, UP, buff=0.1)
        meta = DashedLine(ax.c2p(0, 1), ax.c2p(1.2, 1), color=GREY_D, dash_length=0.06)
        envs = always_redraw(lambda: VGroup(*[DashedVMobject(ax.plot(lambda t, s=s: 1 + s * np.exp(-z.get_value() * W * t), x_range=[0, 1.2], color=VD, stroke_width=2.5), num_dashes=40) for s in (1, -1)]))
        curva = always_redraw(lambda: ax.plot(lambda t: mola(t, z.get_value()), x_range=[0, 1.2], color=LAR, stroke_width=6))
        ponto = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), mola(tt.get_value(), z.get_value())), radius=0.09, color=WHITE).set_z_index(5))
        guia = always_redraw(lambda: DashedLine(ax.c2p(tt.get_value(), 0), ax.c2p(tt.get_value(), mola(tt.get_value(), z.get_value())), color=GREY_B, dash_length=0.05, stroke_width=1.5))
        self.play(FadeOut(chave), FadeOut(cl), Create(ax), FadeIn(lx), FadeIn(ly), Create(meta), run_time=1.1)
        self.play(Create(curva), FadeIn(envs), run_time=1.0)
        self.add(guia, ponto)

        # ---------- seletor de ζ ----------
        sl = NumberLine(x_range=[0, 1.2, 0.2], length=3.4, color=GREY_C, include_numbers=False, stroke_width=2).move_to([-4.4, 0.95, 0])
        sz = tex("zeta", 0.42).next_to(sl, LEFT, buff=0.25)
        tri = always_redraw(lambda: Triangle(fill_color=LAR, fill_opacity=1, stroke_width=0).scale(0.1).rotate(PI).next_to(sl.n2p(z.get_value()), UP, buff=0.02))
        val = always_redraw(lambda: Text(f"{z.get_value():.2f}".replace(".", ","), font="Helvetica Neue", font_size=34, weight=BOLD, color=LAR).next_to(sl, RIGHT, buff=0.3))
        self.play(Create(sl), FadeIn(sz), FadeIn(tri), FadeIn(val), run_time=0.7)

        notas = [(0.3, "elástico: passa do alvo e volta"), (0.82, "quase sem overshoot"), (1.0, "crítico: chega sem passar")]
        fantasmas = VGroup()
        self.add(fantasmas)
        for i, (v, nota) in enumerate(notas):
            if i:
                g = ax.plot(lambda t, zz=z.get_value(): mola(t, zz), x_range=[0, 1.2], color=LAR, stroke_width=3, stroke_opacity=0.28)
                fantasmas.add(g)
                tt.set_value(0)
                self.play(z.animate.set_value(v), run_time=0.8)
            n = Text(nota, font="Helvetica Neue", font_size=26, color=GREY_A)
            n.move_to([-6.75 + n.width / 2, 0.38, 0])
            self.play(FadeIn(n, shift=UP * 0.12), run_time=0.35)
            tt.set_value(0)
            self.play(tt.animate.set_value(1.2), run_time=1.6, rate_func=linear)
            self.play(FadeOut(n), run_time=0.3)

        tt.set_value(0)
        self.play(z.animate.set_value(0.82), FadeOut(fantasmas), run_time=0.9)
        self.play(tt.animate.set_value(1.2), run_time=1.2, rate_func=linear)
        caixa = SurroundingRectangle(VGroup(sz, sl, val), color=LAR, buff=0.18, corner_radius=0.08)
        kit = Text("padrão do kit", font="Helvetica Neue", font_size=26, color=LAR).next_to(caixa, DOWN, buff=0.15)
        self.play(Create(caixa), FadeIn(kit), run_time=0.7)
        self.wait(0.3)
        print('COLAPSO_EM', round(self.time, 2))

        # ---------- saída: tudo se recolhe num ponto laranja (bastão) ----------
        ponto_f = Dot(ORIGIN, radius=0.08, color=LAR)
        tudo = [seta, ode, ax, lx, ly, meta, envs, curva, ponto, guia, sl, sz, tri, val, caixa, kit, parede, hach, chao, mol, bloco, mlab, alvo_m, alvo_l, wd]
        self.play(*[FadeOut(m) for m in tudo], Transform(sol, ponto_f), run_time=1.1)
        self.wait(max(0.5, 24.7 - self.time))
