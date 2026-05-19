import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 7)
y = np.linspace(-2, 2, 5)
X, Y = np.meshgrid(x, y)

# Матрица нулей, чтобы не было цветной заливки ячеек
Z = np.zeros(X.shape)

# Рисуем только границы ячеек сетки
plt.pcolormesh(X, Y, Z, edgecolor='grey', facecolor='none', linewidth=1)

plt.axis('equal')
plt.show()
