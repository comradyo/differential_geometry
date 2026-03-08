import matplotlib.pyplot as plt
import numpy as np

# Пытаюсь отрисовать поверхность, у которой в каком-то месте скорости будут коллинеарны (но не нулевые)

# Создание параметров
u = np.linspace(-10, 10, 100)
v = np.linspace(-10, 10, 100)
U, V = np.meshgrid(u, v)

# Уравнения поверхности
X = U + V
Y = U + V
Z = U * V

# Отрисовка
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
plt.show()
