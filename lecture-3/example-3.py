import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys

# Пытаюсь отрисовать исходную U-V сетку и соответствующую ей X-Y-Z поверхность

# Создание параметров
u = np.linspace(-5, 5, 30)
v = np.linspace(-5, 5, 30)

# Преобразование
def transform(U, V):
    X = U
    Y = V
    Z = np.sin(U) * np.cos(V)
    return X, Y, Z

U, V = np.meshgrid(u, v) # Исходное пространство
X, Y, Z = transform(U, V) # Преобразованное пространство

# Фигуры
fig = plt.figure(figsize=(14, 6))
plt.subplots_adjust(bottom=0.25)  # Leave room at the bottom for sliders

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2, projection='3d')

dot2d, = ax1.plot([0], [0], 'ro', zorder=10) 
dot3d, = ax2.plot([0], [0], [0], 'ro', zorder=10)

ax_u = fig.add_axes([0.25, 0.1, 0.5, 0.03])
ax_v = fig.add_axes([0.25, 0.05, 0.5, 0.03])
u_slider = Slider(ax = ax_u, label = 'Координата u', valmin = -5, valmax = 5, valinit = 0)
v_slider = Slider(ax = ax_v, label = 'Координата v', valmin = -5, valmax = 5, valinit = 0)

# Отрисовка исходной сетки
for i in range(len(u)):
    ax1.plot(U[i, :], V[i, :], 'gray', alpha=0.3)
for i in range(len(v)):
    ax1.plot(U[:, i], V[:, i], 'gray', alpha=0.3)
ax1.set_title("Исходная сетка")
ax1.set_aspect('equal')

# Отрисовка преобразованной сетки
ax2.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)
ax2.set_title("После отображения")
ax2.set_aspect('equal')

# Update function
def update(val):
    point_u = u_slider.val
    point_v = v_slider.val
    p0 = [point_u, point_v]
    p0t = transform(p0[0], p0[1])

    dot2d.set_data([p0[0]], [p0[1]])

    dot3d.set_data([p0t[0]], [p0t[1]])
    dot3d.set_3d_properties([p0t[2]]) # Для 3D оси Z обновляется отдельно
    
    fig.canvas.draw_idle()

u_slider.on_changed(update)
v_slider.on_changed(update)

update(0)

plt.show()