import matplotlib.pyplot as plt
import numpy as np

# Пытаюсь отрисовать поверхность, у которой в каком-то месте скорости будут коллинеарны (но не нулевые)

# Создание параметров
u = np.linspace(-5, 5, 30)
v = np.linspace(-5, 5, 30)
U, V = np.meshgrid(u, v)

# Уравнения поверхности (например, сфера)
#X = U + V
#Y = (U + V)**2
#Z = (U - V)**2

# При  v = 0, вектора должны совпадать
X = U**2/2 + U*V - V**2/2   # dx/du = u + v,      dx/dv = u - v
Y = U**2/2 + U*V + V**3/3   # dy/du = u + v,      dy/dv = u + v^2
Z = U + np.sin(V)           # dz/du = 1,          dz/dv = cos(v)

X1 = u**2/2
Y1 = u**2/2
Z1 = u

# Отрисовка
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(X, Y, Z, color = 'green')
ax.plot(X1, Y1, Z1, color = 'red', linewidth = 8)
plt.show()
