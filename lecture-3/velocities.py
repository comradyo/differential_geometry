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

dX_dU = -np.sin(U) * np.sin(V)
dX_dV = np.cos(U) * np.cos(V)
dY_dU = np.cos(U) * np.sin(V)
dY_dV = np.sin(U) * np.cos(V)
dZ_dU = np.zeros(U.shape) * np.zeros(V.shape)
dZ_dV = np.ones(U.shape) * -np.sin(V)

def build_dots_1(X, Y, Z):
    print(type(X))
    dots_x = X[0]
    dots_y = Y[0]
    dots_z = Z[0]

    print(len(dots_x), len(dots_y), len(dots_z))

def get_x(u, v):
    return np.cos(u) * np.sin(v)

def get_y(u, v):
    return np.sin(u) * np.sin(v)

def get_z(u, v):
    return np.cos(v)

def dx_d(u, v): # В ответе - производная по u, по v
    return -np.sin(u) * np.sin(v), np.cos(u) * np.cos(v)

def dy_d(u, v):
    return np.cos(u) * np.sin(v), np.sin(u) * np.cos(v)

def dz_d(u, v):
    return np.zeros(u.shape), -np.sin(v)

# Stack flattened arrays to get an array of coordinate pairs
# The shape will be (N*M, 2)
coordinates = np.stack((U.flatten(), V.flatten()), axis=1)

def surface_dots_coordinates(coordinates):
    u = coordinates[:, 0] # первый столбец
    v = coordinates[:, 1] # второй столбец

    dots_x = get_x(u, v)
    dots_y = get_y(u, v)
    dots_z = get_z(u, v)

    return dots_x, dots_y, dots_z

def surface_velocities(coordinates):
    u = coordinates[:, 0] # первый столбец
    v = coordinates[:, 1] # второй столбец

    dots_x = get_x(u, v)
    dots_y = get_y(u, v)
    dots_z = get_z(u, v)

    dots_x_vel_u, dots_x_vel_v = dx_d(u, v)
    dots_y_vel_u, dots_y_vel_v = dy_d(u, v)
    dots_z_vel_u, dots_z_vel_v = dz_d(u, v)

    return (
        dots_x + dots_x_vel_u, dots_y + dots_y_vel_u, dots_z + dots_z_vel_u
    ), (
        dots_x + dots_x_vel_v, dots_y + dots_y_vel_v, dots_z + dots_z_vel_v
    )

def main():
    xs, ys, zs = surface_dots_coordinates(coordinates)
    vel_u, vel_v = surface_velocities(coordinates)
    #return

    #dots_x, dots_y, dots_z = build_dots(coordinates)

    # return
    # Отрисовка
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #ax.plot_surface(X, Y, Z, cmap='viridis')
    #ax.plot_surface(dX_dU, dY_dU, dZ_dU, cmap='viridis')
    #ax.plot_surface(dX_dV, dY_dV, dZ_dV, cmap='viridis')
    #ax.plot(dots_x, dots_y, dots_z, 'o', color = 'red', linewidth = 1)
    ax.plot(xs, ys, zs, 'o', color = 'red', linewidth = 1)
    ax.plot(vel_u[0], vel_u[1], vel_u[2], 'o', color = 'orange', linewidth = 0.1)
    ax.plot(vel_v[0], vel_v[1], vel_v[2], 'o', color = 'yellow', linewidth = 0.1)
    plt.show()

if __name__ == "__main__":
    main()
