import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ipywidgets import interact, FloatSlider

# -------------------------------
# Параметризация поверхности
# -------------------------------

def r(u, v):
    x = u
    y = v
    z = np.sin(u) * np.cos(v)
    return x, y, z


# -------------------------------
# Глобальная поверхность
# -------------------------------

u = np.linspace(-3, 3, 100)
v = np.linspace(-3, 3, 100)

U, V = np.meshgrid(u, v)
X, Y, Z = r(U, V)


# -------------------------------
# Локальная сетка
# -------------------------------

eps = 0.5
n_lines = 7
n_pts = 50

offsets = np.linspace(-eps, eps, n_lines)
t = np.linspace(-eps, eps, n_pts)


def make_local_grid(u0, v0):
    UV_lines = []

    for du in offsets:
        UV_lines.append((
            u0 + du*np.ones_like(t),
            v0 + t
        ))

    for dv in offsets:
        UV_lines.append((
            u0 + t,
            v0 + dv*np.ones_like(t)
        ))

    return UV_lines


def lines_to_plotly_2d(lines):
    Xs, Ys = [], []

    for u_line, v_line in lines:
        Xs.extend(u_line)
        Ys.extend(v_line)

        Xs.append(None)
        Ys.append(None)

    return Xs, Ys


def lines_to_plotly_3d(lines):
    Xs, Ys, Zs = [], [], []

    for u_line, v_line in lines:
        x, y, z = r(u_line, v_line)

        Xs.extend(x)
        Ys.extend(y)
        Zs.extend(z)

        Xs.append(None)
        Ys.append(None)
        Zs.append(None)

    return Xs, Ys, Zs


# -------------------------------
# Отрисовка
# -------------------------------

def draw(u0=0.0, v0=0.0):

    grid = make_local_grid(u0, v0)

    uv_x, uv_y = lines_to_plotly_2d(grid)
    xyz_x, xyz_y, xyz_z = lines_to_plotly_3d(grid)

    px, py, pz = r(u0, v0)

    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "xy"}, {"type": "surface"}]],
        subplot_titles=("Параметрическая плоскость", "Поверхность")
    )

    # --------------------------------
    # Левая картинка (u,v)
    # --------------------------------

    fig.add_trace(
        go.Scatter(
            x=uv_x,
            y=uv_y,
            mode="lines",
            line=dict(color="red")
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Scatter(
            x=[u0],
            y=[v0],
            mode="markers",
            marker=dict(size=10)
        ),
        row=1,
        col=1
    )

    # --------------------------------
    # Правая картинка (поверхность)
    # --------------------------------

    fig.add_trace(
        go.Surface(
            x=X,
            y=Y,
            z=Z,
            opacity=0.7,
            showscale=False
        ),
        row=1,
        col=2
    )

    fig.add_trace(
        go.Scatter3d(
            x=xyz_x,
            y=xyz_y,
            z=xyz_z,
            mode="lines",
            line=dict(color="red", width=4)
        ),
        row=1,
        col=2
    )

    fig.add_trace(
        go.Scatter3d(
            x=[px],
            y=[py],
            z=[pz],
            mode="markers",
            marker=dict(size=5)
        ),
        row=1,
        col=2
    )

    fig.update_layout(
        width=1200,
        height=600,
        showlegend=False
    )

    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
        row=1,
        col=1
    )

    fig.show()


interact(
    draw,
    u0=FloatSlider(min=-3, max=3, step=0.05, value=0),
    v0=FloatSlider(min=-3, max=3, step=0.05, value=0)
);
