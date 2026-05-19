# Разбираюсь с матрицей Якоби, Якобианами и т.п.

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# Хочу отрисовать исходную сетку, искаженную сетку, расчитать матрицу Якоби, Якобиан в каждой точке
# Направление искажения в каждой точке (добавить слайдер для x, y, z)

# Ага, Якобиан - это штука, которая в каждой точке показывает, куда примерно (приближаем линейной функцией) примерно будет искажаться, 
# двигаться точка при применении преобразования.

# Что хорошо бы нарисовать:
# Точку, куб вокруг неё и то, как этот куб преобразуется при движении точки

# Преобразование
def transform(X, Y, Z):
    # скручивание
    X_new = X * np.cos(Z) + Y * np.sin(Z)
    Y_new = Y * np.cos(Z) - X * np.sin(Z)
    Z_new = Z
    return X_new, Y_new, Z_new

# Матрица Якоби
def jacobian(x, y, z):
    return np.array([
        [np.cos(z), np.sin(z), -x*np.sin(z) + y*np.cos(z)],
        [-np.sin(z), np.cos(z), -y*np.sin(z) - x*np.cos(z)],
        [0, 0, 1]
    ])

# Функция отрисовки сетки
def draw_grid(ax, X, Y, Z, **kwargs):
    # Линии вдоль оси X (проходим по y и z)
    for j in range(num_of_dots_y):
        for k in range(num_of_dots_z):
            ax.plot(X[j, :, k], Y[j, :, k], Z[j, :, k], **kwargs)

    # Линии вдоль оси Y (проходим по x и z)
    for i in range(num_of_dots_x):
        for k in range(num_of_dots_z):
            ax.plot(X[:, i, k], Y[:, i, k], Z[:, i, k], **kwargs)

    # Линии вдоль оси Z (проходим по x и y)
    for i in range(num_of_dots_x):
        for j in range(num_of_dots_y):
            ax.plot(X[j, i, :], Y[j, i, :], Z[j, i, :], **kwargs)

# Функция отрисовки куба
def draw_cube(ax, X, Y, Z, **kwargs):
    for j in range(2):
        for k in range(2):
            ax.plot(X[j, :, k], Y[j, :, k], Z[j, :, k], **kwargs)
    for i in range(2):
        for k in range(2):
            ax.plot(X[:, i, k], Y[:, i, k], Z[:, i, k], **kwargs)
    for i in range(2):
        for j in range(2):
            ax.plot(X[j, i, :], Y[j, i, :], Z[j, i, :], **kwargs)

def draw_point(ax, x, y, z, **kwargs):
    ax.scatter(x, y, z, **kwargs)

# Число точек по каждой из осей
num_of_dots_x = 5
num_of_dots_y = 5
num_of_dots_z = 10

x = np.linspace(0, 1, num_of_dots_x)
y = np.linspace(0, 1, num_of_dots_y)
z = np.linspace(0, np.pi * 2, num_of_dots_z)
# Исходная сетка
X, Y, Z = np.meshgrid(x, y, z)
# Преобразованная сетка
Xt, Yt, Zt = transform(X, Y, Z)

# Отрисовка
fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': '3d'}, figsize=(12, 6))

ax1.set_position([0.2, 0.15, 0.55, 0.8]) 
ax2.set_position([0.55, 0.15, 0.55, 0.8]) 

ax_x = fig.add_axes([0.03, 0.85, 0.3, 0.1])
ax_y = fig.add_axes([0.03, 0.70, 0.3, 0.1])
ax_z = fig.add_axes([0.03, 0.55, 0.3, 0.1])
x_slider = Slider(ax = ax_x, label = 'Значение x', valmin = 0, valmax = 1, valinit = 0)
y_slider = Slider(ax = ax_y, label = 'Значение y', valmin = 0, valmax = 1, valinit = 0)
z_slider = Slider(ax = ax_z, label = 'Значение z', valmin = 0, valmax = np.pi * 2, valinit = 0)

label_pos = x_slider.label.get_position()
x_slider.label.set_position((0.23, label_pos[1]+0.45))
label_pos = y_slider.label.get_position()
y_slider.label.set_position((0.23, label_pos[1]+0.45))
label_pos = z_slider.label.get_position()
z_slider.label.set_position((0.23, label_pos[1]+0.45))

ax1.set_title("Исходная сетка")
ax2.set_title("Сетка под действием отображения")

# 3. Update function
def update(val):
    ax1.cla()
    ax2.cla()

    # исходная сетка
    draw_grid(ax1, X, Y, Z, color='grey', alpha=0.6, lw=1)

    x = x_slider.val
    y = y_slider.val
    z = z_slider.val
    p0 = [x, y, z]
    eps = 0.4
    xc = np.linspace(-eps, eps, 2)
    yc = np.linspace(-eps, eps, 2)
    zc = np.linspace(-eps, eps, 2)
    # Куб 
    Dx, Dy, Dz = np.meshgrid(xc, yc, zc)
    # Куб вокруг точки
    Xc, Yc, Zc = Dx + p0[0], Dy + p0[1], Dz + p0[2]

    draw_point(ax1, p0[0], p0[1], p0[2], marker='o', color='red', linewidth=2)
    draw_cube(ax1, Xc, Yc, Zc, color='red', alpha=0.6, lw=2)

    # деформированная сетка
    draw_grid(ax2, Xt, Yt, Zt, color='blue', alpha=0.3, lw=1)
    # преобразованная точка
    p0t = transform(p0[0], p0[1], p0[2])
    draw_point(ax2, p0t[0], p0t[1], p0t[2], marker='o', color='red', linewidth=2)
    # Куб при линейном приближении с помощью матрицы Якоби
    cube_shape = Dx.shape # Форма куба

    cube = np.stack([
        Dx.ravel(),
        Dy.ravel(),
        Dz.ravel()
    ], axis=1)

    cube_transformed = (jacobian(p0[0], p0[1], p0[2]) @ cube.T).T + p0t
    Dxt, Dyt, Dzy = cube_transformed.T.reshape(3, *cube_shape)
    draw_cube(ax2, Dxt, Dyt, Dzy, color='green', alpha=0.6, lw=2)
    # Куб при применении операции трансформации
    Xct, Yct, Zct = transform(Xc, Yc, Zc)
    draw_cube(ax2, Xct, Yct, Zct, color='red', alpha=0.6, lw=2)

    # set_box_aspect tells Matplotlib that the physical display box shouldn't be a squashed square canvas anymore; 
    # it forces the Z-axis of the plot window to be physically 6 times longer than the X and Y axes.
    ax1.set_box_aspect((1, 1, 2))
    # ax.set_aspect('equal') guarantees that a step of 1 looks identical in length on the screen 
    # whether it is on the X, Y, or Z axis.
    ax1.set_aspect('equal')
    ax2.set_box_aspect((3, 3, 6))
    ax2.set_aspect('equal')

    fig.canvas.draw_idle()

x_slider.on_changed(update)
y_slider.on_changed(update)
z_slider.on_changed(update)
update(0)

plt.show()
