import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Функция отрисовки квадрата
def draw_square(X, Y, **kwargs):
    for i in range(2):
        plt.plot(X[i, :], Y[i, :], **kwargs)
    for i in range(2):
        plt.plot(X[:, i], Y[:, i], **kwargs)

# Преобразование
def transform(X, Y):
    X_new = X + 0.5 * Y
    Y_new = Y + 0.5 * np.sin(X)
    return X_new, Y_new

# Матрица Якоби
def jacobian(x, y):
    return np.array([
        [1, 0.5],
        [0.5*np.cos(x), 1],
    ])

# создаём сетку
x = np.linspace(-5, 5, 20)
y = np.linspace(-5, 5, 20)

X, Y = np.meshgrid(x, y)
X2, Y2 = transform(X, Y)

#fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw={'projection': '3d'}, figsize=(10, 6))

# рисуем
plt.figure(figsize=(10, 6))

# исходная сетка
plt.subplot(1, 2, 1)
for i in range(len(x)):
    plt.plot(X[i, :], Y[i, :], 'gray')
for i in range(len(y)):
    plt.plot(X[:, i], Y[:, i], 'gray')
plt.title("Исходная сетка")
plt.gca().set_aspect('equal')

point_x = 0
point_y = 0
p0 = [point_x, point_y]
eps = 0.4
xc = np.linspace(-eps, eps, 2)
yc = np.linspace(-eps, eps, 2)
# Куб 
Dx, Dy = np.meshgrid(xc, yc)
# Куб вокруг точки
Xc, Yc = Dx + p0[0], Dy + p0[1]

plt.scatter(p0[0], p0[1], marker='o', color='red', linewidths=2)
draw_square(Xc, Yc, color='red', alpha=0.6, lw=2)

# деформированная сетка
plt.subplot(1, 2, 2)
for i in range(len(x)):
    plt.plot(X2[i, :], Y2[i, :], 'blue')
    plt.plot(X2[:, i], Y2[:, i], 'blue')
plt.title("После отображения")
plt.gca().set_aspect('equal')

p0t = transform(p0[0], p0[1])
plt.scatter(p0t[0], p0t[1], marker='o', color='red', linewidths=2)

# Квадрат при линейном приближении с помощью матрицы Якоби
square_shape = Dx.shape
square = np.stack([
    Dx.ravel(),
    Dy.ravel(),
], axis=1)

square_transformed = (jacobian(p0[0], p0[1]) @ square.T).T + p0t
Dxt, Dyt = square_transformed.T.reshape(2, *square_shape)
draw_square(Dxt, Dyt, color='green', alpha=0.6, lw=2)
# Куб при применении операции трансформации
Xct, Yct = transform(Xc, Yc)
draw_square(Xct, Yct, color='red', alpha=0.6, lw=2)


plt.show()