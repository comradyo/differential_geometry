import matplotlib.pyplot as plt
import numpy as np

def sphere():
    # Создание параметров
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 40)
    U, V = np.meshgrid(u, v)

    # Уравнения поверхности (сфера)
    X = np.cos(U) * np.sin(V)
    Y = np.sin(U) * np.sin(V)
    Z = np.cos(V)

    # частные производные по u
    Xu = -np.sin(U) * np.sin(V)
    Yu = np.cos(U) * np.sin(V)
    Zu = np.zeros_like(U)

    # частные производные по v
    Xv = np.cos(U) * np.cos(V)
    Yv = np.sin(U) * np.cos(V)
    Zv = np.ones_like(U) * -np.sin(V)

    return X, Y, Z, Xu, Yu, Zu, Xv, Yv, Zv

def example_2():
    u = np.linspace(-5, 5, 20)
    v = np.linspace(-5, 5, 20)
    U, V = np.meshgrid(u, v)

    X = U**2/2 + U*V - V**2/2   # dx/du = u + v,      dx/dv = u - v
    Y = U**2/2 + U*V + V**3/3   # dy/du = u + v,      dy/dv = u + v^2
    Z = U + np.sin(V)           # dz/du = 1,          dz/dv = cos(v)

    Xu = U + V
    Yu = U + V
    Zu = np.ones_like(U)

    Xv = U + V
    Yv = U + V**2
    Zv = np.cos(V)

    return X, Y, Z, Xu, Yu, Zu, Xv, Yv, Zv

def main():
    X, Y, Z, Xu, Yu, Zu, Xv, Yv, Zv = sphere()
    #X, Y, Z, Xu, Yu, Zu, Xv, Yv, Zv = example_2()

    # Отрисовка
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(X, Y, Z, cmap='viridis')

    # Шаг, с которым отсчитываем точки для отрисовки скоростей
    step = 3

    length = 0.3
    should_normalize = True

    ax.quiver(
        X[::step, ::step], Y[::step, ::step], Z[::step, ::step], 
        Xu[::step, ::step], Yu[::step, ::step], Zu[::step, ::step], 
        color='red', length=length, normalize=should_normalize,
    )
    ax.quiver(
        X[::step, ::step], Y[::step, ::step], Z[::step, ::step], 
        Xv[::step, ::step], Yv[::step, ::step], Zv[::step, ::step], 
        color='blue', length=length, normalize=should_normalize,
    )

    plt.show()

if __name__ == "__main__":
    main()
