import matplotlib.pyplot as plt
import numpy as np

# Пример отрисовки параметризированной поверхности

# Создание параметров
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
U, V = np.meshgrid(u, v)

# Уравнения поверхности (сфера)
X = np.cos(U) * np.sin(V)
Y = np.sin(U) * np.sin(V)
Z = np.cos(V)

# Отрисовка
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis')
plt.show()
