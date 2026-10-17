import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.integrate import solve_ivp
from geometry.calculations import parallel_translation_system, geodesic_system, projection, angle, decomposition
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

# 17.10:
# Так, кажется, за первый базисный вектор ортонормированного базиса имеет смысл брать 
# единичный вектор по направлению взгляда, а второй - перпендикулярный ему и находящийся справа.
# Тогда при любом повороте вектора направления, все сущности (в частности, веер лучей поля зрения) будут зависеть толькок от направления луча

# Что-то не могу придумать нормальный алгоритм для поиска вектора, 
# перпендикулярного e1 и находящегося справа
# Тупой алгоритм:
# 1. Ищем ортонормированный базис ru, rv
# 2. Выражаем в нём e1
# 3. Через синус (матрица поворота) ищем e2
# Но мне кажется, есть что-то проще.
# Как зная базисные вектора плоскости и имея какой-то вектор, 
# найти другой перпендикулярный вектор такой же длины, повёрнутый на 90 градусов по часовой стрелке?



u_min = 0
u_max = 2 * np.pi
v_min = 0
v_max = np.pi
num_of_u = 20
num_of_v = 20
t_span_max = np.pi
surface = surfaces.Sphere(u_min, u_max, num_of_u, v_min, v_max, num_of_v)

#u_min = -5
#u_max = 5
#v_min = -5
#v_max = 5
#num_of_u = 40
#num_of_v = 40
#t_span_max = 50
#surface = surfaces.SurfaceWithCollinearVectors(u_min, u_max, num_of_u, v_min, v_max, num_of_v)

#u_min = -5
#u_max = 5
#v_min = -5
#v_max = 5
#num_of_u = 40
#num_of_v = 40
#t_span_max = 10
#surface = surfaces.Plane(u_min, u_max, num_of_u, v_min, v_max, num_of_v)

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
ax_alpha = fig.add_axes([0.25, 0.04, 0.5, 0.03])
slider_alpha  = Slider(ax=ax_alpha , label="Угол альфа", valmin=0, valmax=2 * np.pi, valinit=0)

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
ax2.set_aspect("equal")
ax2.set_xlabel("Ось X", fontsize=12, color="red")
ax2.set_ylabel("Ось Y", fontsize=12, color="green")
ax2.set_zlabel("Ось Z", fontsize=12, color="blue", labelpad=10)

# Точка с координатами (u0, v0)
(dot2d,) = ax1.plot([0], [0], "ro", zorder=10)
(dot3d,) = ax2.plot([0], [0], [0], "ro", zorder=10)

# Канонический базис
quiver_vec_u = ax2.quiver(0, 0, 0, 0, 0, 0, color="red")
quiver_vec_v = ax2.quiver(0, 0, 0, 0, 0, 0, color="blue")
# Базис камеры
quiver_vec_e1 = ax2.quiver(0, 0, 0, 0, 0, 0, color="red")
quiver_vec_e2 = ax2.quiver(0, 0, 0, 0, 0, 0, color="blue")
# Вектор нормали в точке
quiver_vec_normal = ax2.quiver(0, 0, 0, 0, 0, 0, color="green")

# Прообраз канонического базиса
quiver_2d_vec_u = ax1.quiver(0, 0, 0, 0, color="red")
quiver_2d_vec_v = ax1.quiver(0, 0, 0, 0, color="blue")
# Прообраз ортонормированного базиса камеры
quiver_2d_e1 = ax1.quiver(0, 0, 0, 0, color="darkred")
quiver_2d_e2 = ax1.quiver(0, 0, 0, 0, color="darkblue")

# Направляющий вектор (или нужен направляющий вектор кривой?)
#quiver_vec_eta = ax2.quiver(0, 0, 0, 0, 0, 0, color="magenta")

angles = []
quivers_view_rays = []
geodesics = []
# Угол обзора
fov_angle_degrees = 60
fov_angle = np.pi * fov_angle_degrees / 180
num_of_rays = 10
delta_fov_angle = fov_angle / num_of_rays
angle = -fov_angle/2
while angle <= fov_angle/2:
  quivers_view_rays.append(ax2.quiver(0, 0, 0, 0, 0, 0, color="indigo"))
  angles.append(angle)
  angle += delta_fov_angle
  geodesic, = ax2.plot([], [], [], color="green", linestyle="dashed")
  geodesics.append(geodesic)

# Геодезическая
geodesic2D, = ax1.plot([], [], color="green", linestyle="dashed")
geodesic, = ax2.plot([], [], [], color="green", linestyle="dashed")

# Update function
def update(val):
    # t = slider_t.val
    u0 = slider_u.val
    v0 = slider_v.val
    alpha = slider_alpha.val
    p0 = [u0, v0]
    p0t = surface.transform(p0[0], p0[1])

    dot2d.set_data([p0[0]], [p0[1]])

    dot3d.set_data([p0t[0]], [p0t[1]])
    dot3d.set_3d_properties([p0t[2]])  # Для 3D оси Z обновляется отдельно

    x0, y0, z0 = surface.transform(u0, v0)
    vec_ru = surface.r_u(u0, v0)
    vec_rv = surface.r_v(u0, v0)

    # Ортонормируем канонический базис
    vec_ru_norm = vec_ru / np.linalg.norm(vec_ru)
    vec_rv_norm = vec_rv - projection(vec_rv, vec_ru_norm)
    vec_rv_norm = vec_rv_norm / np.linalg.norm(vec_rv_norm)

    # Строем ортонормированный базис относительно направления взгляда
    # Я так понимаю, не получится однозначно сказать, что такое "влево" и что такое "вправо"
    # Идея: работать с базисом в исходном пространстве. 
    # Точнее, понятие "по часовой стрелке" или "против часовой стрелки" 
    # использовать именно в контексте этого пространства
    vec_e1 = +np.cos(alpha) * vec_ru_norm + np.sin(alpha) * vec_rv_norm
    vec_e2 = -np.sin(alpha) * vec_ru_norm + np.cos(alpha) * vec_rv_norm

    # Разложение базиса камеры на исходный (для отрисовки в 2д)
    e1_2d = decomposition(vec_e1, vec_ru, vec_rv)
    e2_2d = decomposition(vec_e2, vec_ru, vec_rv)

    # print(np.linalg.norm(vec_e1), np.linalg.norm(vec_e2))

    # Пусть e2 будет вектором взгляда (тогда e1 в исходном пространстве, по идее, 
    # будет находиться на 90 градусов по часовой)

    # TODO: что-то туплю, система решается для координат в исходном базисе или в каноническом?
    # a = -np.sin(alpha)
    # b = np.cos(alpha)
    # print(a, b, e2_2d)
    # Да, кажется, правильно именно через e2_2d - поскольку это разложение по ru, rv, а символы считаются именно по этим векторам

    # Начальные условия системы ОДУ
    # Параметры: TODO
    # TODO: наверное, можно вынести в geometry.math
    Y0 = [u0, v0, e2_2d[0], e2_2d[1]] 
    t_span = (0.0, t_span_max)  # Интервал, на котором ищем решение системы
    t_eval = np.linspace(
        t_span[0], t_span[1], 100
    )  # Массив временных точек, где мы хотим получить решение
    sol = solve_ivp(
        geodesic_system, t_span, Y0, args=(surface.Christoffel_Symbols,), t_eval=t_eval
    )

    gamma_dots_u = sol.y[0]
    gamma_dots_v = sol.y[1]

    gamma_dots_3d_x, gamma_dots_3d_y, gamma_dots_3d_z = surface.transform(gamma_dots_u, gamma_dots_v)

    gammas_dots = []

    vec_view = vec_e2
    view_vectors = []
    for angle in angles:
        # Растягиваем пропорционально углу отставания от вектора взгляда (в касательной плоскости)
        tmp_vec_view = vec_view + np.linalg.norm(vec_view) * np.tan(angle) * vec_e1
        view_vectors.append(tmp_vec_view)
        tmp_vec_view_decomp = decomposition(tmp_vec_view, vec_ru, vec_rv)
        Y0 = [u0, v0, tmp_vec_view_decomp[0], tmp_vec_view_decomp[1]]
        t_span = (0.0, t_span_max)  # Интервал, на котором ищем решение системы
        t_eval = np.linspace(
            t_span[0], t_span[1], 100
        )  # Массив временных точек, где мы хотим получить решение
        sol = solve_ivp(
            geodesic_system, t_span, Y0, args=(surface.Christoffel_Symbols,), t_eval=t_eval
        )
        g_dots_u = sol.y[0]
        g_dots_v = sol.y[1]

        gammas_dots.append(surface.transform(g_dots_u, g_dots_v))

    # чтобы использовалась существующая переменная, объявленная вне этой функции
    global quiver_vec_u  
    global quiver_vec_v
    global quiver_vec_e1
    global quiver_vec_e2
    global quiver_2d_vec_u  
    global quiver_2d_vec_v
    global quiver_2d_e1
    global quiver_2d_e2
    global quivers_view_rays
    #global quiver_vec_eta

    # 1. Стираем старый вектор, если он существует
    if quiver_vec_u is not None:
        quiver_vec_u.remove()
    if quiver_vec_v is not None:
        quiver_vec_v.remove()
    if quiver_vec_e1 is not None:
        quiver_vec_e1.remove()
    if quiver_vec_e2 is not None:
        quiver_vec_e2.remove()
    if quiver_2d_vec_u is not None:
        quiver_2d_vec_u.remove()
    if quiver_2d_vec_v is not None:
        quiver_2d_vec_v.remove()
    if quiver_2d_e1 is not None:
        quiver_2d_e1.remove()
    if quiver_2d_e2 is not None:
        quiver_2d_e2.remove()
    for i in range(len(angles)):
        if quivers_view_rays[i] is not None:
            quivers_view_rays[i].remove()

    quiver_vec_u = ax2.quiver(x0, y0, z0, vec_ru[0], vec_ru[1], vec_ru[2], color="red")
    quiver_vec_v = ax2.quiver(x0, y0, z0, vec_rv[0], vec_rv[1], vec_rv[2], color="blue")
    quiver_vec_e1 = ax2.quiver(x0, y0, z0, vec_e1[0], vec_e1[1], vec_e1[2], color="darkred")
    quiver_vec_e2 = ax2.quiver(x0, y0, z0, vec_e2[0], vec_e2[1], vec_e2[2], color="darkblue")
    
    # По умолчанию в 2д вектора почему-то рисуются без пропорционального растяжения, 
    # поэтому приходится вручную настраивать
    quiver_2d_vec_u = ax1.quiver(u0, v0, 1, 0, color="red",  angles='xy', scale_units='xy', scale=1,)
    quiver_2d_vec_v = ax1.quiver(u0, v0, 0, 1, color="blue",  angles='xy', scale_units='xy', scale=1,)
    quiver_2d_e1 = ax1.quiver(u0, v0, e1_2d[0], e1_2d[1], color="darkred", angles='xy', scale_units='xy', scale=1,)
    quiver_2d_e2 = ax1.quiver(u0, v0, e2_2d[0], e2_2d[1], color="darkblue",  angles='xy', scale_units='xy', scale=1,)
    #quiver_vec_eta = ax2.quiver(x0, y0, z0, vec_eta0[0], vec_eta0[1], vec_eta0[2], color="magenta", linestyle="dashed")
    geodesic2D.set_data(gamma_dots_u, gamma_dots_v)
    geodesic.set_data_3d(gamma_dots_3d_x, gamma_dots_3d_y, gamma_dots_3d_z)

    for i in range(len(angles)):
        quivers_view_rays[i] = ax2.quiver(x0, y0, z0, view_vectors[i][0], view_vectors[i][1], view_vectors[i][2], color="indigo")
        geodesics[i].set_data_3d(gammas_dots[i][0], gammas_dots[i][1], gammas_dots[i][2])

    fig.canvas.draw_idle()


slider_u.on_changed(update)
slider_v.on_changed(update)
slider_alpha.on_changed(update)

update(0)

plt.show()
