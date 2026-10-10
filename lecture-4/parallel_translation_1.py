import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys
from scipy.integrate import solve_ivp

# Параллельный перенос вдоль кривой

# 10.10.2026
# Что должно быть:

# Задана поверхность
# Заданы координаты точки (u0, v0), слайдеры
# Отрисовывается канонический базис в точке
# Отрисовывается касательная плоскость в точке
# Отрисовывается кривая. Задана уравнениями вида:
#   u(t) = u0 + f(t), f(0) = 0,
#   v(t) = v0 + g(t), g(0) = 0,
# Отрисовывается точка кривой
# Отрисовывается слайдер t, хорошо бы, чтобы сбрасывался при изменении u0, v0
# Отрисовывается касательный вектор вдоль кривой(?)
#   (Получится ли сделать зависимости от t?)
# Отрисовываются проекции ускорения на касательную плоскость (правда, проекции чего именно)?


class Surface2D:  # Parent Class
    def __init__(
        self, u_start, u_end, num_of_u_points, v_start, v_end, num_of_v_points
    ):
        self.u = np.linspace(u_start, u_end, num_of_u_points)
        self.v = np.linspace(v_start, v_end, num_of_v_points)
        self.U, self.V = np.meshgrid(self.u, self.v)

    def get_data_to_draw(self):
        return

    def transform(self, u, v):
        return self.X(u, v), self.Y(u, v), self.Z(u, v)

    def jacobian(self, u, v):
        return np.array(
            [
                [self.Xu(u, v), self.Xv(u, v)],
                [self.Yu(u, v), self.Yv(u, v)],
                [self.Zu(u, v), self.Zv(u, v)],
            ]
        )

    def normal(self, u, v):
        du = np.array([self.Xu(u, v), self.Yu(u, v), self.Zu(u, v)])
        dv = np.array([self.Xv(u, v), self.Yv(u, v), self.Zv(u, v)])
        return np.cross(du, dv)

    def get_data_to_draw(self):
        X = self.X(self.U, self.V)
        Y = self.Y(self.U, self.V)
        Z = self.Z(self.U, self.V)
        Xu = self.Xu(self.U, self.V)
        Yu = self.Yu(self.U, self.V)
        Zu = self.Zu(self.U, self.V)
        Xv = self.Xv(self.U, self.V)
        Yv = self.Yv(self.U, self.V)
        Zv = self.Zv(self.U, self.V)

        return self.U, self.V, X, Y, Z, Xu, Yu, Zu, Xv, Yv, Zv

    def r_u(self, u, v):
        return (self.Xu(u, v), self.Yu(u, v), self.Zu(u, v))

    def r_v(self, u, v):
        return (self.Xv(u, v), self.Yv(u, v), self.Zv(u, v))

    def G(self, u, v):
        return np.array(
            [
                [
                    np.dot(self.r_u(u, v), self.r_u(u, v)),
                    np.dot(self.r_u(u, v), self.r_v(u, v)),
                ],
                [
                    np.dot(self.r_v(u, v), self.r_u(u, v)),
                    np.dot(self.r_v(u, v), self.r_v(u, v)),
                ],
            ]
        )

    def G_inverse(self, u, v):
        g = self.G(u, v)
        det = g[0][0] * g[1][1] - g[0][1] ** 2
        return (
            np.array(
                [
                    [g[1][1], -g[0][1]],
                    [-g[1][0], g[0][0]],
                ]
            )
            / det
        )

    def r_u(self, u, v):
        return (self.Xu(u, v), self.Yu(u, v), self.Zu(u, v))

    def r_v(self, u, v):
        return (self.Xv(u, v), self.Yv(u, v), self.Zv(u, v))

    def r_uu(self, u, v):
        return (self.Xuu(u, v), self.Yuu(u, v), self.Zuu(u, v))

    def r_uv(self, u, v):
        return (self.Xuv(u, v), self.Yuv(u, v), self.Zuv(u, v))

    def r_vu(self, u, v):
        return (self.Xvu(u, v), self.Yvu(u, v), self.Zvu(u, v))

    def r_vv(self, u, v):
        return (self.Xvv(u, v), self.Yvv(u, v), self.Zvv(u, v))

    # Матрица частных производных по i и j векторам
    def second_derivative_matrix(self, u, v):
        return np.array(
            [
                [self.r_uu(u, v), self.r_uv(u, v)],
                [self.r_vu(u, v), self.r_vv(u, v)],
            ]
        )

    # Символ Кристоффеля 2-го рода (хз, нужен ли будет 1-й)
    def _christoffel_symbol(self, i, j, k, g_inv, scnd_der_mtrx, r_u, r_v):
        # По формуле, которую вывел в конспекте
        return g_inv[k][0] * np.dot(scnd_der_mtrx[i][j], r_u) + g_inv[k][1] * np.dot(
            scnd_der_mtrx[i][j], r_v
        )

    # Символ кристоффеля (матрица 2x2x2, элемент - ijk)
    # TODO: Возможно, имеет смысл возвращать [k][i][j], но это потом
    def Christoffel_Symbols(self, u, v):
        # TODO: как-то оптимизировать расчёты,
        # так как тут два вычисления одного и того же
        g_inv = self.G_inverse(u, v)
        scnd_der_mtrx = self.second_derivative_matrix(u, v)
        r_u = self.r_u(u, v)
        r_v = self.r_v(u, v)
        res = np.zeros((2, 2, 2))
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    res[i][j][k] = self._christoffel_symbol(
                        i, j, k, g_inv, scnd_der_mtrx, r_u, r_v
                    )

        return res


class Sphere(Surface2D):
    def X(self, u, v):
        return np.cos(u) * np.sin(v)

    def Y(self, u, v):
        return np.sin(u) * np.sin(v)

    def Z(self, u, v):
        return np.cos(v)

    # Частные производные по u
    def Xu(self, u, v):
        return -np.sin(u) * np.sin(v)

    def Yu(self, u, v):
        return np.cos(u) * np.sin(v)

    def Zu(self, u, v):
        return np.zeros_like(u)

    # Частные производные по v
    def Xv(self, u, v):
        return np.cos(u) * np.cos(v)

    def Yv(self, u, v):
        return np.sin(u) * np.cos(v)

    def Zv(self, u, v):
        return np.ones_like(u) * -np.sin(v)

    # Вторые частные производные по u
    def Xuu(self, u, v):
        return -np.cos(u) * np.sin(v)

    def Yuu(self, u, v):
        return -np.sin(u) * np.sin(v)

    def Zuu(self, u, v):
        return np.zeros_like(u)

    def Xvu(self, u, v):
        return -np.sin(u) * np.cos(v)

    def Yvu(self, u, v):
        return np.cos(u) * np.cos(v)

    def Zvu(self, u, v):
        return np.zeros_like(u)

    # Вторые частные производные по v
    def Xuv(self, u, v):
        return -np.sin(u) * np.cos(v)

    def Yuv(self, u, v):
        return np.cos(u) * np.cos(v)

    def Zuv(self, u, v):
        return np.zeros_like(u)

    def Xvv(self, u, v):
        return -np.cos(u) * np.sin(v)

    def Yvv(self, u, v):
        return -np.sin(u) * np.sin(v)

    def Zvv(self, u, v):
        return np.ones_like(u) * -np.cos(v)

    def G(self, u, v):
        return np.array(
            [
                [np.sin(v) ** 2, 0],
                [0, 1],
            ]
        )

    def G_inverse(self, u, v):
        return np.array(
            [
                [1 / (np.sin(v) ** 2), 0],
                [0, 1],
            ]
        )


class SurfaceWithCollinearVectors(Surface2D):
    def X(self, u, v):
        return u**2 / 2 + u * v - v**2 / 2

    def Y(self, u, v):
        return u**2 / 2 + u * v + v**3 / 3

    def Z(self, u, v):
        return u + np.sin(v)

    # частные производные по u
    def Xu(self, u, v):
        return u + v

    def Yu(self, u, v):
        return u + v

    def Zu(self, u, v):
        return np.ones_like(u)

    # частные производные по v
    def Xv(self, u, v):
        return u - v

    def Yv(self, u, v):
        return u + v**2

    def Zv(self, u, v):
        return np.ones_like(u) * np.cos(v)


def curve(t):
    return 2 * t, 3 - t
def curve_dt(t):
    return 2, -1

# Система параллельного переноса (для момента времени t)
def parallel_translation_system(t, xi, curve_func, curve_dt_func, christoffel_func):
    # xi = [xi_u, xi_v]
    # curve_func(t) возвращает (u, v, dot_u, dot_v) для текущего момента времени
    xi_u, xi_v = xi
    u, v = curve_func(t)
    u_t, v_t = curve_dt_func(t)

    Gamma = christoffel_func(u, v) 
        
    # Производные d(xi_u)/dt и d(xi_v)/dt
    dot_xi_u = -(
        Gamma[0][0][0] * u_t * xi_u + 
        Gamma[0][1][0] * u_t * xi_v + 
        Gamma[1][0][0] * v_t * xi_u + 
        Gamma[1][1][0] * v_t * xi_v 
    )
                 
    dot_xi_v = -(
        Gamma[0][0][1] * u_t * xi_u + 
        Gamma[0][1][1] * u_t * xi_v + 
        Gamma[1][0][1] * v_t * xi_u + 
        Gamma[1][1][1] * v_t * xi_v 
    )
                 
    return [dot_xi_u, dot_xi_v]


u_min = 0
u_max = 2 * np.pi
v_min = 0
v_max = np.pi
num_of_u = 20
num_of_v = 20
surface = Sphere(u_min, u_max, num_of_u, v_min, v_max, num_of_v)

# u_min = -5
# u_max = 5
# v_min=-5
# v_max=5
# num_of_u=40
# num_of_v=40
# surface = SurfaceWithCollinearVectors(u_min, u_max, num_of_u, v_min, v_max, num_of_v)

U, V, X, Y, Z, Xu, Yu, Zu, Xv, Yv, Zv = surface.get_data_to_draw()

# Фигуры
fig = plt.figure(figsize=(14, 6))
plt.subplots_adjust(bottom=0.25)

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2, projection="3d")

t_min = 0
t_max = np.sqrt(np.pi)
t_curve = np.linspace(t_min, t_max, 30)
u_curve, v_curve = curve(t_curve)
x_curve = surface.X(u_curve, v_curve)
y_curve = surface.Y(u_curve, v_curve)
z_curve = surface.Z(u_curve, v_curve)
curve2d = ax1.plot(u_curve, v_curve, zorder=10, color="green")
curve3d = ax2.plot(x_curve, y_curve, z_curve, zorder=10, color="green")

(dot2d,) = ax1.plot([0], [0], "ro", zorder=10)
(dot3d,) = ax2.plot([0], [0], [0], "ro", zorder=10)

# Слайдер t
ax_t = fig.add_axes([0.25, 0.01, 0.5, 0.03])
slider_t = Slider(ax=ax_t, label="Параметр t", valmin=t_min, valmax=t_max, valinit=0)
# Слайдеры для вектора a*ru(u_0) + b*rv(b_0)
ax_a = fig.add_axes([0.25, 0.04, 0.5, 0.03])
ax_b = fig.add_axes([0.25, 0.07, 0.5, 0.03])
slider_a = Slider(ax=ax_a, label="Параметр a", valmin=0, valmax=10, valinit=1)
slider_b = Slider(ax=ax_b, label="Параметр b", valmin=0, valmax=10, valinit=1)

# Отрисовка координат
for i in range(num_of_u):
    ax1.plot(U[i, :], V[i, :], "gray", alpha=0.3)
for i in range(num_of_v):
    ax1.plot(U[:, i], V[:, i], "gray", alpha=0.3)
ax1.set_title("Исходная сетка")
ax1.set_aspect("equal")
ax1.set_xlabel("Ось U", fontsize=12, color="red")
ax1.set_ylabel("Ось V", fontsize=12, color="green")

# Отрисовка поверхности
#ax2.plot_surface(X, Y, Z, cmap="viridis", alpha=0.6)
ax2.plot_wireframe(X, Y, Z, color = 'gray', linewidth=0.5)
ax2.set_title("После отображения")
ax2.set_aspect("equal")
ax2.set_xlabel("Ось X", fontsize=12, color="red")
ax2.set_ylabel("Ось Y", fontsize=12, color="green")
ax2.set_zlabel("Ось Z", fontsize=12, color="blue", labelpad=10)

# Канонический базис
vec_u = ax2.quiver(0, 0, 0, 0, 0, 0, color="red")
vec_v = ax2.quiver(0, 0, 0, 0, 0, 0, color="blue")
# Вектор нормали в точке
vec_normal = ax2.quiver(0, 0, 0, 0, 0, 0, color="green")

# Направляющий вектор (или нужен направляющий вектор кривой?)
vec_eta = ax2.quiver(0, 0, 0, 0, 0, 0, color="red")
# Начальный вектор в точке
vec_xi_0 = ax2.quiver(0, 0, 0, 0, 0, 0, color="red")
# Начальный вектор при параллельном переносе вдоль кривой 
vec_xi_t = ax2.quiver(0, 0, 0, 0, 0, 0, color="magenta")

# Update function
def update(val):
    t = slider_t.val
    a = slider_a.val
    b = slider_b.val
    u0, v0 = curve(0)
    u, v = curve(t)
    p0 = [u, v]
    p0t = surface.transform(p0[0], p0[1])

    dot2d.set_data([p0[0]], [p0[1]])

    dot3d.set_data([p0t[0]], [p0t[1]])
    dot3d.set_3d_properties([p0t[2]])  # Для 3D оси Z обновляется отдельно

    x0, y0, z0 = surface.X(u0, v0), surface.Y(u0, v0), surface.Z(u0, v0)
    xu0, yu0, zu0 = surface.Xu(u0, v0), surface.Yu(u0, v0), surface.Zu(u0, v0)
    xv0, yv0, zv0 = surface.Xv(u0, v0), surface.Yv(u0, v0), surface.Zv(u0, v0)
    vec_ru0 = np.array([xu0, yu0, zu0])
    vec_rv0 = np.array([xv0, yv0, zv0])
    x, y, z = surface.X(u, v), surface.Y(u, v), surface.Z(u, v)
    xu, yu, zu = surface.Xu(u, v), surface.Yu(u, v), surface.Zu(u, v)
    xv, yv, zv = surface.Xv(u, v), surface.Yv(u, v), surface.Zv(u, v)
    vec_ru = np.array([xu, yu, zu])
    vec_rv = np.array([xv, yv, zv])
    vec_xi0 = a * vec_ru0 + b * vec_rv0

    t_span = (0.0, t)
    # Массив временных точек, где мы хотим получить решение
    t_eval = np.linspace(t_span[0], t_span[1], 100)

    xi_0 = [a, b] # Начальные координаты касательного вектора [xi_u0, xi_v0]

    sol = solve_ivp(
        parallel_translation_system, 
        t_span, xi_0, 
        args=(curve, curve_dt, surface.Christoffel_Symbols),
        t_eval=t_eval,
    )
    xi_t_u = a
    xi_t_v = b
    if t > 0:
        xi_t_u = sol.y[0][-1]
        xi_t_v = sol.y[1][-1]

    vec_xit = xi_t_u * vec_ru + xi_t_v * vec_rv
    print("dot = ", np.dot(vec_xit, vec_xit))

    global vec_u  # чтобы использовалась существующая переменная, объявленная вне этой функции
    global vec_v
    global vec_eta
    global vec_xi_0
    global vec_xi_t

    # 1. Стираем старый вектор, если он существует
    if vec_u is not None:
        vec_u.remove()
    if vec_v is not None:
        vec_v.remove()
    # if vec_eta is not None:
    #    vec_eta.remove()
    if vec_xi_0 is not None:
        vec_xi_0.remove()
    if vec_xi_t is not None:
        vec_xi_t.remove()

    vec_u = ax2.quiver(x, y, z, xu, yu, zu, color="red")
    vec_v = ax2.quiver(x, y, z, xv, yv, zv, color="blue")
    vec_xi_0 = ax2.quiver(x0, y0, z0, vec_xi0[0], vec_xi0[1], vec_xi0[2], color="magenta", linestyle="dashed")
    vec_xi_t = ax2.quiver(x, y, z, vec_xit[0], vec_xit[1], vec_xit[2], color="magenta")

    # Матрица первой фундаментальной формы
    print("")
    G_matrix = surface.G(u, v)
    matrix_string = "\n".join(
        "   ".join(f"{num:.5f}" for num in row) for row in G_matrix
    )
    print("Fisrt fundamental form:")
    print(matrix_string)
    G_inv_matrix = surface.G_inverse(u, v)
    matrix_string = "\n".join(
        "   ".join(f"{num:.5f}" for num in row) for row in G_inv_matrix
    )
    print("Inverse:")
    print(matrix_string)

    print("Christoffel_Symbols:")
    chr_symb = surface.Christoffel_Symbols(u, v)
    print(chr_symb)

    fig.canvas.draw_idle()


slider_t.on_changed(update)
slider_a.on_changed(update)
slider_b.on_changed(update)

update(0)

plt.show()
