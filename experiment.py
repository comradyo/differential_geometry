import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 1. Генерируем базовые данные
num_curves = 5  # Размер массива кривых (статичен)
t = np.linspace(0, 2 * np.pi, 100)

def get_curve_data(phase):
    """Функция, возвращающая координаты для всех кривых в зависимости от фазы (слайдера)"""
    xs, ys, zs = [], [], []
    for i in range(num_curves):
        # Пример изменения геометрии кривых от индекса i и фазы
        x = np.sin(t + phase + i * 0.5)
        y = np.cos(t + phase + i * 0.5)
        z = t * (i + 1) / num_curves
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return xs, ys, zs

# 2. Инициализируем график
fig = plt.subplots_adjust(bottom=0.25) # Оставляем место внизу под слайдер
fig = plt.gcf()
ax = fig.add_subplot(111, projection='3d')

# Устанавливаем статические лимиты, чтобы оси не "прыгали" при обновлении
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_zlim(0, 2 * np.pi)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# 3. Создаем массив (список) 3D-кривых с начальными данными (phase=0)
initial_phase = 0.0
xs, ys, zs = get_curve_data(initial_phase)

curves = []
for i in range(num_curves):
    # ax.plot возвращает список из одного элемента Line3D, забираем его через [0]
    line, = ax.plot(xs[i], ys[i], zs[i], label=f'Кривая {i+1}')
    curves.append(line)

ax.legend()

# 4. Добавляем слайдер
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03]) # [left, bottom, width, height]
slider = Slider(ax_slider, 'Фаза', 0.0, 2 * np.pi, valinit=initial_phase)

# 5. Функция обновления (вызывается при движении слайдера)
def update(val):
    phase = slider.val
    new_xs, new_ys, new_zs = get_curve_data(phase)
    
    # Быстро обновляем координаты существующих линий без перерисовки всей сцены
    for i in range(num_curves):
        curves[i].set_data_3d(new_xs[i], new_ys[i], new_zs[i])
        
    fig.canvas.draw_idle() # Перерисовываем только холст

# Связываем слайдер с функцией обновления
slider.on_changed(update)

plt.show()
