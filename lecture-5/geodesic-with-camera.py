import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys
from scipy.integrate import solve_ivp

# Камера

# 11.10.2026
# Так, пора приступать к отрисовке вида из камеры (точнее, сначала с отрисовки первых лучей, исходящих из камеры).

# Алгоритм примерно такой:
# В текущей касательной плоскости ищем ортонормированный базис.
# В нём строим единичный вектор направления ()
# При движении куда-либо параллельно переносим вектор взгляда вдоль геодезической, по которой движемся
# Вопросы: 
# Как понять, что делаем шаг длины delta_s? Всегда ведь один и тот же шаг делаем? И это, по сути, будет шаг
# При смещении в новой плоскости снова расчитываем ортонормированный базис?
# Или, может, при движении параллельно переносить и ортонормированный базис?

# хз, получится ли сделать именно в этой программе сам вид, но основные моменты нужно сделать
# Что должно быть:
# Ортонормированный базис в касательной плоскости
# Вектор направления
# Веер лучей из камеры + отрисовка геодезических для каждого из этих лучей (или каждого 10)

# План максимум: 
# 1. Отрисовка текстуры на 2д плоскости (координатной)
# 2. Отрисовка текстуры поверхности
# 3. Отрисовка того, что видит камера. 
# Только интересно, как понять, что именно должно быть в каждом вертикальном пикселе - 
# пиксель после прохождения определенного расстояния или что-то сложнее? 
# В случае обычного рейтрейсинга был такой алгоритм:
#   1. Есть камера, она находится на высоте cam.h
#   2. Есть экран, у него задана высота в размерах пространства
#   3. Для каждого из пикселей экрана расчитывается его положение в 3д мире игры и берется точка пересечения прямой, 
#   проходящей через камеру и экран на данной высоте, и плоскости, и берется цвет пикселя данной точки на плоскости.
# Тут, очевидно, такой же алгоритм не реализовать, нужна какая-то его версия.

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

    # Вторые частные производные по u
    def Xuu(self, u, v):
        return np.ones_like(u)

    def Yuu(self, u, v):
        return np.ones_like(u)

    def Zuu(self, u, v):
        return np.zeros_like(u)

    def Xvu(self, u, v):
        return np.ones_like(u)

    def Yvu(self, u, v):
        return np.ones_like(u)

    def Zvu(self, u, v):
        return np.zeros_like(u)

    # Вторые частные производные по v
    def Xuv(self, u, v):
        return np.ones_like(v)

    def Yuv(self, u, v):
        return np.ones_like(v)

    def Zuv(self, u, v):
        return np.zeros_like(u)

    def Xvv(self, u, v):
        return -np.ones_like(v)

    def Yvv(self, u, v):
        return 2 * v

    def Zvv(self, u, v):
        return -np.sin(v)


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
        Gamma[0][0][0] * u_t * xi_u
        + Gamma[0][1][0] * u_t * xi_v
        + Gamma[1][0][0] * v_t * xi_u
        + Gamma[1][1][0] * v_t * xi_v
    )

    dot_xi_v = -(
        Gamma[0][0][1] * u_t * xi_u
        + Gamma[0][1][1] * u_t * xi_v
        + Gamma[1][0][1] * v_t * xi_u
        + Gamma[1][1][1] * v_t * xi_v
    )

    return [dot_xi_u, dot_xi_v]


# Система параллельного переноса (для момента времени t)
# Y - вектор состояния решения, состоит из четырёх элементов:
#   u, v - текущие координаты
#   dot_u, dot_v - производные координатных функций кривой (по t) в точке
def geodesic_system(t, Y, christoffel_func):
    u, v, dot_u, dot_v = Y
    Gamma = christoffel_func(u, v)  # получаем символы Кристоффеля в текущей точке (u, v)

    # Считаем вторые производные (ускорения) из системы уравнений
    # Обратите внимание на знаки "минус", так как мы перенесли Г в правую часть
    # И на законные двойки перед смешанными слагаемыми!
    ddot_u = -(
        Gamma[0][0][0] * dot_u**2 + 
        2 * Gamma[0][1][0] * dot_u * dot_v + 
        Gamma[1][1][0] * dot_v**2
    )

    ddot_v = -(
        Gamma[0][0][1] * dot_u**2 + 
        2 * Gamma[0][1][1] * dot_u * dot_v + 
        Gamma[1][1][1] * dot_v**2
    )

    return [dot_u, dot_v, ddot_u, ddot_v]


u_min = 0
u_max = 2 * np.pi
v_min = 0
v_max = np.pi
num_of_u = 20
num_of_v = 20
surface = Sphere(u_min, u_max, num_of_u, v_min, v_max, num_of_v)

#u_min = -5
#u_max = 5
#v_min = -5
#v_max = 5
#num_of_u = 40
#num_of_v = 40
#surface = SurfaceWithCollinearVectors(u_min, u_max, num_of_u, v_min, v_max, num_of_v)

U, V, X, Y, Z, Xu, Yu, Zu, Xv, Yv, Zv = surface.get_data_to_draw()

# Фигуры
fig = plt.figure(figsize=(14, 6))
plt.subplots_adjust(bottom=0.25)

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2, projection="3d")

t_min = 0
t_max = np.sqrt(np.pi)
t_curve = np.linspace(t_min, t_max, 30)
# u_curve, v_curve = curve(t_curve)
# x_curve = surface.X(u_curve, v_curve)
# y_curve = surface.Y(u_curve, v_curve)
# z_curve = surface.Z(u_curve, v_curve)
# curve2d = ax1.plot(u_curve, v_curve, zorder=10, color="green")
# curve3d = ax2.plot(x_curve, y_curve, z_curve, zorder=10, color="green")

(dot2d,) = ax1.plot([0], [0], "ro", zorder=10)
(dot3d,) = ax2.plot([0], [0], [0], "ro", zorder=10)

# Слайдер t
# ax_t = fig.add_axes([0.25, 0.01, 0.5, 0.03])
# slider_t = Slider(ax=ax_t, label="Параметр t", valmin=t_min, valmax=t_max, valinit=0)
# Слайдер для точки (u, v)
ax_u = fig.add_axes([0.25, 0.1, 0.5, 0.03])
ax_v = fig.add_axes([0.25, 0.13, 0.5, 0.03])
slider_u = Slider(ax=ax_u, label="Координата u", valmin=u_min, valmax=u_max, valinit=1)
slider_v = Slider(ax=ax_v, label="Координата v", valmin=v_min, valmax=v_max, valinit=1)

# Слайдеры для вектора a*ru(u_0) + b*rv(b_0)
ax_a = fig.add_axes([0.25, 0.04, 0.5, 0.03])
ax_b = fig.add_axes([0.25, 0.07, 0.5, 0.03])
slider_a = Slider(ax=ax_a, label="Параметр a", valmin=-10, valmax=10, valinit=1)
slider_b = Slider(ax=ax_b, label="Параметр b", valmin=-10, valmax=10, valinit=1)

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
# ax2.plot_surface(X, Y, Z, cmap="viridis", alpha=0.6)
ax2.plot_wireframe(X, Y, Z, color="gray", linewidth=0.5)
ax2.set_title("После отображения")
#ax2.set_aspect("equal")
ax2.set_xlabel("Ось X", fontsize=12, color="red")
ax2.set_ylabel("Ось Y", fontsize=12, color="green")
ax2.set_zlabel("Ось Z", fontsize=12, color="blue", labelpad=10)

# Канонический базис
vec_u = ax2.quiver(0, 0, 0, 0, 0, 0, color="red")
vec_v = ax2.quiver(0, 0, 0, 0, 0, 0, color="blue")
# Вектор нормали в точке
vec_normal = ax2.quiver(0, 0, 0, 0, 0, 0, color="green")

# Направляющий вектор (или нужен направляющий вектор кривой?)
vec_eta = ax2.quiver(0, 0, 0, 0, 0, 0, color="magenta")
# Начальный вектор в точке
vec_xi_0 = ax2.quiver(0, 0, 0, 0, 0, 0, color="red")
# Начальный вектор при параллельном переносе вдоль кривой
vec_xi_t = ax2.quiver(0, 0, 0, 0, 0, 0, color="magenta")

# Геодезическая
geodesic2D, = ax1.plot([], [], color="green", linestyle="dashed")
geodesic, = ax2.plot([], [], [], color="green", linestyle="dashed")


# Update function
def update(val):
    # t = slider_t.val
    u0 = slider_u.val
    v0 = slider_v.val
    a = slider_a.val
    b = slider_b.val
    p0 = [u0, v0]
    p0t = surface.transform(p0[0], p0[1])

    dot2d.set_data([p0[0]], [p0[1]])

    dot3d.set_data([p0t[0]], [p0t[1]])
    dot3d.set_3d_properties([p0t[2]])  # Для 3D оси Z обновляется отдельно

    x0, y0, z0 = surface.X(u0, v0), surface.Y(u0, v0), surface.Z(u0, v0)
    xu0, yu0, zu0 = surface.Xu(u0, v0), surface.Yu(u0, v0), surface.Zu(u0, v0)
    xv0, yv0, zv0 = surface.Xv(u0, v0), surface.Yv(u0, v0), surface.Zv(u0, v0)
    vec_ru0 = np.array([xu0, yu0, zu0])
    vec_rv0 = np.array([xv0, yv0, zv0])
    # x, y, z = surface.X(u, v), surface.Y(u, v), surface.Z(u, v)
    # xu, yu, zu = surface.Xu(u, v), surface.Yu(u, v), surface.Zu(u, v)
    # xv, yv, zv = surface.Xv(u, v), surface.Yv(u, v), surface.Zv(u, v)
    # vec_ru = np.array([xu, yu, zu])
    # vec_rv = np.array([xv, yv, zv])
    vec_eta0 = a * vec_ru0 + b * vec_rv0

    # xi_0 = [a, b] # Начальные координаты касательного вектора [xi_u0, xi_v0]

    Y0 = [u0, v0, a, b]  # Начальные условия системы ОДУ
    t_span = (0.0, np.pi)  # Интервал, на котором ищем решение системы
    t_eval = np.linspace(
        t_span[0], t_span[1], 100
    )  # Массив временных точек, где мы хотим получить решение
    sol = solve_ivp(
        geodesic_system, t_span, Y0, args=(surface.Christoffel_Symbols,), t_eval=t_eval
    )

    gamma_dots_u = sol.y[0]
    gamma_dots_v = sol.y[1]
    print(gamma_dots_u[-1], gamma_dots_v[-1])
    gamma_dots_3d_x, gamma_dots_3d_y, gamma_dots_3d_z = (
        surface.X(gamma_dots_u, gamma_dots_v),
        surface.Y(gamma_dots_u, gamma_dots_v),
        surface.Z(gamma_dots_u, gamma_dots_v),
    )

    # vec_xit = xi_t_u * vec_ru + xi_t_v * vec_rv
    # print("dot = ", np.dot(vec_xit, vec_xit))

    global vec_u  # чтобы использовалась существующая переменная, объявленная вне этой функции
    global vec_v
    global vec_eta
    global vec_xi_0
    global vec_xi_t
    #global geodesic

    # 1. Стираем старый вектор, если он существует
    if vec_u is not None:
        vec_u.remove()
    if vec_v is not None:
        vec_v.remove()
    if vec_eta is not None:
        vec_eta.remove()
    # if vec_xi_0 is not None:
    #    vec_xi_0.remove()
    # if vec_xi_t is not None:
    #    vec_xi_t.remove()

    vec_u = ax2.quiver(x0, y0, z0, xu0, yu0, zu0, color="red")
    vec_v = ax2.quiver(x0, y0, z0, xv0, yv0, zv0, color="blue")
    # vec_xi_0 = ax2.quiver(x0, y0, z0, vec_xi0[0], vec_xi0[1], vec_xi0[2], color="magenta", linestyle="dashed")
    # vec_xi_t = ax2.quiver(x, y, z, vec_xit[0], vec_xit[1], vec_xit[2], color="magenta")
    vec_eta = ax2.quiver(
        x0,
        y0,
        z0,
        vec_eta0[0],
        vec_eta0[1],
        vec_eta0[2],
        color="magenta",
        linestyle="dashed",
    )
    geodesic2D.set_data(gamma_dots_u, gamma_dots_v)
    geodesic.set_data_3d(gamma_dots_3d_x, gamma_dots_3d_y, gamma_dots_3d_z)

    fig.canvas.draw_idle()


slider_u.on_changed(update)
slider_v.on_changed(update)
slider_a.on_changed(update)
slider_b.on_changed(update)

update(0)

plt.show()
