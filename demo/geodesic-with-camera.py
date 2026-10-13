import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import solve_ivp
from geometry.calculations import parallel_translation_system, geodesic_system
import geometry.surfaces as surfaces

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

u_min = 0
u_max = 2 * np.pi
v_min = 0
v_max = np.pi
num_of_u = 20
num_of_v = 20
surface = surfaces.Sphere(u_min, u_max, num_of_u, v_min, v_max, num_of_v)

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

# Отрисовка координатных линий
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

# Точка с координатами (u0, v0)
(dot2d,) = ax1.plot([0], [0], "ro", zorder=10)
(dot3d,) = ax2.plot([0], [0], [0], "ro", zorder=10)

# Канонический базис
vec_u = ax2.quiver(0, 0, 0, 0, 0, 0, color="red")
vec_v = ax2.quiver(0, 0, 0, 0, 0, 0, color="blue")
# Вектор нормали в точке
vec_normal = ax2.quiver(0, 0, 0, 0, 0, 0, color="green")

# Направляющий вектор (или нужен направляющий вектор кривой?)
vec_eta = ax2.quiver(0, 0, 0, 0, 0, 0, color="magenta")

# TODO: вектор взгляда
# TODO: слайдер для угла поворота

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

    x0, y0, z0 = surface.transform(u0, v0)
    vec_ru0 = surface.r_u(u0, v0)
    vec_rv0 = surface.r_v(u0, v0)
    vec_eta0 = a * vec_ru0 + b * vec_rv0

    # Начальные условия системы ОДУ
    # Параметры: TODO
    # TODO: наверное, можно вынести в geometry.math
    Y0 = [u0, v0, a, b]  
    t_span = (0.0, np.pi)  # Интервал, на котором ищем решение системы
    t_eval = np.linspace(
        t_span[0], t_span[1], 100
    )  # Массив временных точек, где мы хотим получить решение
    sol = solve_ivp(
        geodesic_system, t_span, Y0, args=(surface.Christoffel_Symbols,), t_eval=t_eval
    )

    gamma_dots_u = sol.y[0]
    gamma_dots_v = sol.y[1]

    gamma_dots_3d_x, gamma_dots_3d_y, gamma_dots_3d_z = surface.transform(gamma_dots_u, gamma_dots_v)

    # чтобы использовалась существующая переменная, объявленная вне этой функции
    global vec_u  
    global vec_v
    global vec_eta

    # 1. Стираем старый вектор, если он существует
    if vec_u is not None:
        vec_u.remove()
    if vec_v is not None:
        vec_v.remove()
    if vec_eta is not None:
        vec_eta.remove()

    vec_u = ax2.quiver(x0, y0, z0, vec_ru0[0], vec_ru0[1], vec_ru0[2], color="red")
    vec_v = ax2.quiver(x0, y0, z0, vec_rv0[0], vec_rv0[1], vec_rv0[2], color="blue")
    vec_eta = ax2.quiver(x0, y0, z0, vec_eta0[0], vec_eta0[1], vec_eta0[2], color="magenta", linestyle="dashed")
    geodesic2D.set_data(gamma_dots_u, gamma_dots_v)
    geodesic.set_data_3d(gamma_dots_3d_x, gamma_dots_3d_y, gamma_dots_3d_z)

    fig.canvas.draw_idle()


slider_u.on_changed(update)
slider_v.on_changed(update)
slider_a.on_changed(update)
slider_b.on_changed(update)

update(0)

plt.show()
