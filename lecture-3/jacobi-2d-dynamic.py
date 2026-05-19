import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Функция отрисовки квадрата
def draw_square(ax, X, Y, **kwargs):
    for i in range(len(X)):
        ax.plot(X[i, :], Y[i, :], **kwargs)
    for i in range(len(X)):
        ax.plot(X[:, i], Y[:, i], **kwargs)

def draw_curved_square(ax, X, Y, **kwargs):
    ax.plot(X[0, :], Y[0, :], **kwargs)
    ax.plot(X[len(X)-1, :], Y[len(X)-1, :], **kwargs)
    ax.plot(X[:, 0], Y[:, 0], **kwargs)
    ax.plot(X[:, len(X)-1], Y[:, len(X)-1], **kwargs)

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

X, Y = np.meshgrid(x, y) # Исходное пространство
Xt, Yt = transform(X, Y) # Преобразованное пространство

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

#ax1.set_position([0.2, 0.15, 0.55, 0.8]) 
#ax2.set_position([0.55, 0.15, 0.55, 0.8]) 

ax_x = fig.add_axes([0.2, 0.1, 0.5, 0.05])
ax_y = fig.add_axes([0.2, 0.05, 0.5, 0.05])
ax_eps = fig.add_axes([0.2, 0.00, 0.5, 0.05])
x_slider = Slider(ax = ax_x, label = 'Значение x', valmin = -5, valmax = 5, valinit = 0)
y_slider = Slider(ax = ax_y, label = 'Значение y', valmin = -5, valmax = 5, valinit = 0)
eps_slider = Slider(ax = ax_eps, label = 'Значение eps', valmin = 0, valmax = 5, valinit = 0.4)

# Update function
def update(val):
    ax1.cla()
    ax2.cla()

    # исходная сетка
    for i in range(len(x)):
        ax1.plot(X[i, :], Y[i, :], 'gray')
    for i in range(len(y)):
        ax1.plot(X[:, i], Y[:, i], 'gray')
    ax1.set_title("Исходная сетка")
    ax1.set_aspect('equal')

    point_x = x_slider.val
    point_y = y_slider.val
    p0 = [point_x, point_y]
    eps = eps_slider.val
    xc = np.linspace(-eps, eps, 2)
    yc = np.linspace(-eps, eps, 2)
    # Квадрат со стороной 2*eps
    Dx, Dy = np.meshgrid(xc, yc)
    # Квадрат вокруг точки
    Xc, Yc = Dx + p0[0], Dy + p0[1]

    ax1.scatter(p0[0], p0[1], marker='o', color='red', linewidths=2)
    draw_square(ax1, Xc, Yc, color='red', alpha=0.6, lw=2)

    # деформированная сетка
    for i in range(len(x)):
        ax2.plot(Xt[i, :], Yt[i, :], 'blue', alpha=0.6)
    for i in range(len(y)):
        ax2.plot(Xt[:, i], Yt[:, i], 'blue', alpha=0.6)
    ax1.set_title("После отображения")
    ax2.set_aspect('equal')

    p0t = transform(p0[0], p0[1])
    ax2.scatter(p0t[0], p0t[1], marker='o', color='red', linewidths=2)

    # Квадрат при линейном приближении с помощью матрицы Якоби
    square_shape = Dx.shape
    square = np.stack([
        Dx.ravel(),
        Dy.ravel(),
    ], axis=1)

    square_transformed = (jacobian(p0[0], p0[1]) @ square.T).T + p0t
    Dxt, Dyt = square_transformed.T.reshape(2, *square_shape)
    draw_square(ax2, Dxt, Dyt, color='green', alpha=1, lw=2)
    # Квадрат при применении операции трансформации
    xc = np.linspace(-eps, eps, 10)
    yc = np.linspace(-eps, eps, 10)
    # Квадрат со стороной 2*eps
    Dx, Dy = np.meshgrid(xc, yc)
    Xc, Yc = Dx + p0[0], Dy + p0[1]
    Xct, Yct = transform(Xc, Yc)
    draw_curved_square(ax2, Xct, Yct, color='red', alpha=0.6, lw=2)

    fig.canvas.draw_idle()

x_slider.on_changed(update)
y_slider.on_changed(update)
eps_slider.on_changed(update)
update(0)


plt.show()