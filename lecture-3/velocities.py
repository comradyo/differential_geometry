import matplotlib.pyplot as plt
import numpy as np

# Пытаюсь отрисовать поверхность и её скорости в каждой точке

# Создание параметров
u = np.linspace(0, 2 * np.pi, 20)
v = np.linspace(0, np.pi, 20)
U, V = np.meshgrid(u, v)

# Уравнения поверхности (сфера)
X = np.cos(U) * np.sin(V)
Y = np.sin(U) * np.sin(V)
Z = np.cos(V)

# частные производные
Xu = -np.sin(U) * np.sin(V)
Yu = np.cos(U) * np.sin(V)
Zu = np.zeros_like(U)

Xv = np.cos(U) * np.cos(V)
Yv = np.sin(U) * np.cos(V)
Zv = np.ones_like(U) * -np.sin(V)

# Stack flattened arrays to get an array of coordinate pairs
# The shape will be (N*M, 2)
coordinates = np.stack((U.flatten(), V.flatten()), axis=1)

def surface_dots_coordinates(coordinates):
    x = lambda u, v: np.cos(u) * np.sin(v)
    y = lambda u, v: np.sin(u) * np.sin(v)
    z = lambda u, v: np.cos(v)

    u = coordinates[:, 0] # первый столбец
    v = coordinates[:, 1] # второй столбец

    dots_x = x(u, v)
    dots_y = y(u, v)
    dots_z = z(u, v)

    return dots_x, dots_y, dots_z

def surface_velocities(coordinates):
    x = lambda u, v: np.cos(u) * np.sin(v)
    y = lambda u, v: np.sin(u) * np.sin(v)
    z = lambda u, v: np.cos(v)
    dxdu = lambda u, v: -np.sin(u) * np.sin(v)
    dydu = lambda u, v: np.cos(u) * np.sin(v)
    dzdu = lambda u, v: np.zeros(u.shape)
    dxdv = lambda u, v: np.cos(u) * np.cos(v)
    dydv = lambda u, v: np.sin(u) * np.cos(v)
    dzdv = lambda u, v: -np.sin(v)

    u = coordinates[:, 0] # первый столбец
    v = coordinates[:, 1] # второй столбец

    xs = x(u, v)
    ys = y(u, v)
    zs = z(u, v)

    xsvu, xsvv = dxdu(u, v), dxdv(u, v)
    ysvu, ysvv = dydu(u, v), dydv(u, v)
    zsvu, zsvv = dzdu(u, v), dzdv(u, v)

    return (
        xs + xsvu, ys + ysvu, zs + zsvu
    ), (
        xs + xsvv, ys + ysvv, zs + zsvv
    )

def main():
    #xs, ys, zs = surface_dots_coordinates(coordinates)
    #vel_u, vel_v = surface_velocities(coordinates)
    #ax.plot(vel_u[0], vel_u[1], vel_u[2], 'o', color = 'orange', linewidth = 0.1)
    #ax.plot(vel_v[0], vel_v[1], vel_v[2], 'o', color = 'yellow', linewidth = 0.1)

    # return
    # Отрисовка
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.2)
    ax.quiver(X, Y, Z, Xu, Yu, Zu, color='red', length=0.3, normalize=True)
    ax.quiver(X, Y, Z, Xv, Yv, Zv, color='blue', length=0.3, normalize=True)

    plt.show()

if __name__ == "__main__":
    main()
