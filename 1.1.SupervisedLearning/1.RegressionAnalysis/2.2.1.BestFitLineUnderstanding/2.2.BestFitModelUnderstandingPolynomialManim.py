from manim import *
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# --- Texts and Colors ---
TEXTS = {
    "title": ("Polynomial Regression", "#FF7A00", 34),
    "dataset": ("This is the dataset we got for training", YELLOW, 22),
    "scatter": ("When we plot the data, we see it is scattered", BLUE, 22),
    "curve_hint": ("Even though scattered, data looks curved → Non-linear", RED, 22),
    "linear_bad": ("Linear line does not cover points well\n(dots are far from the line)", YELLOW, 22),
    "linear_bad_impact": ("Not covering the dots or far away from the dot's\nmakes inaccurate prediction", YELLOW, 22),
    "transform": ("Apply Polynomial Features:\n  x → [x, x²]", GREEN, 22),
    "poly_good": ("Now most points are close to the curve → better fit", ORANGE, 22),
    "poly_good_impact": ("Point's closer to curve, improves accuracy of prediction", ORANGE, 22),
}

class PolynomialRegressionDemo(Scene):
    def play_and_wait(self, *args, **kwargs):
        """Wait for Enter key before playing animation."""
        input("👉 Press Enter to continue...")
        self.play(*args, **kwargs)

    def construct(self):
        # === Title ===
        title = Text(TEXTS["title"][0], font_size=TEXTS["title"][2], color=TEXTS["title"][1]).to_edge(UP)
        self.add(title)

        # ----------------------------
        # Generate Dataset
        # ----------------------------
        np.random.seed(42)
        X = np.linspace(0, 10, 20)  # more points
        y = 0.5 * X**2.5 + 3*X + 5 + np.random.normal(0, 10, size=X.shape)

        # ----------------------------
        # 1️⃣ Scatter Plot
        # ----------------------------
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 180, 20],
            axis_config={"color": GREY},
            x_length=6, y_length=4
        ).shift(DOWN*0.5 + LEFT*2)

        labels = axes.get_axis_labels(x_label="x", y_label="y")

        caption = Text(TEXTS["scatter"][0], font_size=TEXTS["scatter"][2], color=TEXTS["scatter"][1]).to_edge(DOWN)

        self.play(Create(axes), Write(labels))
        dots = VGroup(*[Dot(axes.c2p(x, y_), color=BLUE, radius=0.04) for x, y_ in zip(X, y)])
        self.play(FadeIn(dots, lag_ratio=0.05), Write(caption))
        self.play_and_wait(FadeOut(caption))

        # ----------------------------
        # 2️⃣ Emphasize curve trend
        # ----------------------------
        caption = Text(TEXTS["curve_hint"][0], font_size=TEXTS["curve_hint"][2], color=TEXTS["curve_hint"][1]).to_edge(DOWN)
        self.play(Write(caption))
        self.play_and_wait(FadeOut(caption))

        # ----------------------------
        # 3️⃣ Fit Linear Regression
        # ----------------------------
        lin_reg = LinearRegression()
        lin_reg.fit(X.reshape(-1, 1), y)
        X_line = np.linspace(0, 10, 200)
        y_line = lin_reg.predict(X_line.reshape(-1, 1))

        linear_graph = axes.plot_line_graph(
            X_line, y_line,
            line_color=RED,
            stroke_width=2,
            add_vertex_dots=False
        )

        self.play(Create(linear_graph))

        # ----------------------------
        # 4️⃣ Show residuals (distances)
        # ----------------------------
        residual_lines = VGroup()
        for xi, yi in zip(X, y):
            pred_y = lin_reg.predict([[xi]])[0]
            line = Line(axes.c2p(xi, yi), axes.c2p(xi, pred_y), color=GREY, stroke_width=1)
            residual_lines.add(line)

        caption = Text(TEXTS["linear_bad"][0], font_size=TEXTS["linear_bad"][2], color=TEXTS["linear_bad"][1]).to_edge(DOWN)

        self.play_and_wait(Create(residual_lines), Write(caption))
        self.play_and_wait(FadeOut(caption))

        caption = Text(TEXTS["linear_bad_impact"][0], font_size=TEXTS["linear_bad_impact"][2], color=TEXTS["linear_bad_impact"][1]).to_edge(DOWN)
        self.play_and_wait(Write(caption))
        self.play_and_wait(FadeOut(caption), FadeOut(residual_lines))

        # ----------------------------
        # 5️⃣ Polynomial Features
        # ----------------------------
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X.reshape(-1, 1))

        header = ["x", "y", "x²"]
        table_data = [[f"{x:.1f}", f"{y_: .1f}", f"{x**2:.1f}"] for x, y_ in zip(X[:6], y[:6])]

        poly_table = Table([header] + table_data, include_outer_lines=True).scale(0.5).to_edge(RIGHT).shift(DOWN*0.5)

        caption2 = Text(TEXTS["transform"][0], font_size=TEXTS["transform"][2], color=TEXTS["transform"][1]).next_to(poly_table, DOWN)

        self.play_and_wait(Create(poly_table), Write(caption2))
        self.play_and_wait(FadeOut(poly_table), FadeOut(caption2))

        # ----------------------------
        # 6️⃣ Polynomial Regression Fit
        # ----------------------------
        poly_reg = LinearRegression()
        poly_reg.fit(X_poly, y)
        y_poly = poly_reg.predict(poly.fit_transform(X_line.reshape(-1, 1)))

        poly_graph = axes.plot_line_graph(
            X_line, y_poly,
            line_color=GREEN,
            stroke_width=2,
            add_vertex_dots=False
        )

        self.play_and_wait(Create(poly_graph))
        self.play_and_wait(FadeOut(linear_graph))

        # ----------------------------
        # 7️⃣ Emphasize closer fit
        # ----------------------------
        caption = Text(TEXTS["poly_good"][0], font_size=TEXTS["poly_good"][2], color=TEXTS["poly_good"][1]).to_edge(DOWN)
        self.play_and_wait(Write(caption))

        residual_lines_poly = VGroup()
        for xi, yi in zip(X[::3], y[::3]):  # take every 3rd point
            pred_y = poly_reg.predict(poly.fit_transform([[xi]]))[0]
            line = Line(
                axes.c2p(xi, yi),
                axes.c2p(xi, pred_y),
                color=ORANGE,
                stroke_width=1
            )
            residual_lines_poly.add(line)

        self.play_and_wait(Create(residual_lines_poly))
        self.play_and_wait(FadeOut(caption))

        caption = Text(TEXTS["poly_good_impact"][0], font_size=TEXTS["poly_good_impact"][2], color=TEXTS["poly_good_impact"][1]).to_edge(DOWN)
        self.play_and_wait(Write(caption))
