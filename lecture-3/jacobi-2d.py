# Разбираюсь с матрицей Якоби, Якобианами и т.п.

import numpy as np
import matplotlib.pyplot as plt

# создаём сетку
x = np.linspace(-5, 5, 20)
y = np.linspace(-5, 5, 20)

X, Y = np.meshgrid(x, y)

# отображение u(x, y)
X2 = X + 0.5 * Y
Y2 = Y + 0.5 * np.sin(X)

# рисуем
plt.figure(figsize=(10, 5))

# исходная сетка
plt.subplot(1, 2, 1)
for i in range(len(x)):
    plt.plot(X[i, :], Y[i, :], 'gray')
    plt.plot(X[:, i], Y[:, i], 'gray')
plt.title("Исходная сетка")
plt.gca().set_aspect('equal')

# деформированная сетка
plt.subplot(1, 2, 2)
for i in range(len(x)):
    plt.plot(X2[i, :], Y2[i, :], 'blue')
    plt.plot(X2[:, i], Y2[:, i], 'blue')
plt.title("После отображения")
plt.gca().set_aspect('equal')

plt.show()