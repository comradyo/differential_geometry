import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys

# Касательное векторное поле
# 5.1. Касательное гладкое векторное поле - задать его, отрисовать, 
# в каждой точке раскладывать вектор из этого касательного векторного поля по каноническому базису
# можно отрисовать штрихпунктиром проекции на базис

# Отрисовать проекцию
# Отрисовывать вектор, вдоль которого будем двигаться
# Отрисовывать кривую, вдоль которой будет двигаться точка, и вектор её скорости

# Перенос вдоль кривых тут или отдельным файлом?

class Surface2D: # Parent Class
    def __init__(self, u_start, u_end, num_of_u_points, v_start, v_end, num_of_v_points):
        self.u = np.linspace(u_start, u_end, num_of_u_points)
        self.v = np.linspace(v_start, v_end, num_of_v_points)
        self.U, self.V = np.meshgrid(self.u, self.v)

    def get_data_to_draw(self):
        return
    
    def transform(self, u, v):
        return self.X(u, v), self.Y(u, v), self.Z(u, v)
    
    def jacobian(self, u, v):
        return np.array([
            [self.Xu(u, v), self.Xv(u, v)],
            [self.Yu(u, v), self.Yv(u, v)],
            [self.Zu(u, v), self.Zv(u, v)],
        ])

    def normal(self, u, v):
        return np.cross(self.r_u(u, v), self.r_v(u, v))

    def r_u(self, u, v):
        return (self.Xu(u, v), self.Yu(u, v), self.Zu(u, v))
    def r_v(self, u, v):
        return (self.Xv(u, v), self.Yv(u, v), self.Zv(u, v))
    def r_uu(self, u, v):
        return (self.Xuu(u, v), self.Yuu(u, v), self.Zuu(u, v))
    def r_uv(self, u, v):
        return (self.Xuv(u, v), self.Yuv(u, v), self.Zuv(u, v))
    def r_vu(self, u, v):
        return (self.Xvu(u, v), self.Yvu(u, v), self.Zvu(u, v))
    def r_vv(self, u, v):
        return (self.Xvv(u, v), self.Yvv(u, v), self.Zvv(u, v))

    def get_data_to_draw(self):
        X = self.X(self.U, self.V)
        Y = self.Y(self.U, self.V)
        Z = self.Z(self.U, self.V)
        Xu = self.Xu(self.U, self.V)
        Yu = self.Yu(self.U, self.V)
        Zu = self.Zu(self.U, self.V)
        Xv = self.Xv(self.U, self.V)
        Yv = self.Yv(self.U, self.V)
        Zv = self.Zv(self.U, self.V)

        return self.U,self.V,X,Y,Z,Xu,Yu,Zu,Xv,Yv,Zv

class Sphere(Surface2D):
    def X(self, u, v):
        return np.cos(u) * np.sin(v)
    def Y(self, u, v):
        return np.sin(u) * np.sin(v)
    def Z(self, u, v):
        return np.cos(v)
    # частные производные по u
    def Xu(self, u, v):
        return -np.sin(u) * np.sin(v)
    def Yu(self, u, v):
        return np.cos(u) * np.sin(v)
    def Zu(self, u, v):
        return np.zeros_like(u)
    # частные производные по v
    def Xv(self, u, v):
        return np.cos(u) * np.cos(v)
    def Yv(self, u, v):
        return np.sin(u) * np.cos(v)
    def Zv(self, u, v):
        return np.ones_like(u) * -np.sin(v)
    # Вторые частные производные по u
    def Xuu(self, u, v):
        return -np.cos(u) * np.sin(v)
    def Yuu(self, u, v):
        return -np.sin(u) * np.sin(v)
    def Zuu(self, u, v):
        return np.zeros_like(u)
    def Xvu(self, u, v):
        return -np.sin(u) * np.cos(v)
    def Yvu(self, u, v):
        return np.cos(u) * np.cos(v)
    def Zvu(self, u, v):
        return np.zeros_like(u)
    # Вторые частные производные по v
    def Xuv(self, u, v):
        return -np.sin(u) * np.cos(v)
    def Yuv(self, u, v):
        return np.cos(u) * np.cos(v)
    def Zuv(self, u, v):
        return np.zeros_like(u)
    def Xvv(self, u, v):
        return -np.cos(u) * np.sin(v)
    def Yvv(self, u, v):
        return -np.sin(u) * np.sin(v)
    def Zvv(self, u, v):
        return np.ones_like(u) * -np.cos(v)

u_min=0
u_max=2*np.pi
v_min=0
v_max=np.pi
num_of_u=20
num_of_v=20
surface = Sphere(u_min, u_max, num_of_u, v_min, v_max, num_of_v)

U, V, X, Y, Z, Xu, Yu, Zu, Xv, Yv, Zv = surface.get_data_to_draw()

# Касательное векторное поле
def xi_u(u, v):
    return np.sin(u) + np.cos(v)
def d_xi_u_d_u(u, v):
    return np.cos(u)
def d_xi_u_d_v(u, v):
    return -np.sin(v)
def xi_v(u, v):
    return np.sin(u) * np.cos(v)
def d_xi_v_d_u(u, v):
    return np.cos(u) * np.cos(v)
def d_xi_v_d_v(u, v):
    return -np.sin(u) * np.sin(v)
def xi(u, v, r_u, r_v):
    return (
        xi_u(u, v) * r_u[0] + xi_v(u, v) * r_v[0],
        xi_u(u, v) * r_u[1] + xi_v(u, v) * r_v[1],
        xi_u(u, v) * r_u[2] + xi_v(u, v) * r_v[2],
    )
def d_xi_d_u(u, v, ru, rv, r_uu, r_vu):    
    return (
        d_xi_u_d_u(u, v) * ru[0] + d_xi_u_d_u(u, v) * rv[0] + xi_u(u, v) * r_uu[0] + xi_v(u, v) * r_vu[0],
        d_xi_u_d_u(u, v) * ru[1] + d_xi_u_d_u(u, v) * rv[1] + xi_u(u, v) * r_uu[1] + xi_v(u, v) * r_vu[1],
        d_xi_u_d_u(u, v) * ru[2] + d_xi_u_d_u(u, v) * rv[2] + xi_u(u, v) * r_uu[2] + xi_v(u, v) * r_vu[2],
    )
def d_xi_d_v(u, v, ru, rv, r_uv, r_vv):    
    return (
        d_xi_u_d_v(u, v) * ru[0] + d_xi_u_d_v(u, v) * rv[0] + xi_u(u, v) * r_uv[0] + xi_v(u, v) * r_vv[0],
        d_xi_u_d_v(u, v) * ru[0] + d_xi_u_d_v(u, v) * rv[0] + xi_u(u, v) * r_uv[1] + xi_v(u, v) * r_vv[1],
        d_xi_u_d_v(u, v) * ru[0] + d_xi_u_d_v(u, v) * rv[0] + xi_u(u, v) * r_uv[2] + xi_v(u, v) * r_vv[2],
    )

# Фигуры
fig = plt.figure(figsize=(14, 6))
plt.subplots_adjust(bottom=0.25)  # Leave room at the bottom for sliders

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2, projection='3d')

dot2d, = ax1.plot([0], [0], 'ro', zorder=10) 
dot3d, = ax2.plot([0], [0], [0], 'ro', zorder=10)

ax_u = fig.add_axes([0.25, 0.1, 0.5, 0.03])
ax_v = fig.add_axes([0.25, 0.05, 0.5, 0.03])
u_slider = Slider(ax = ax_u, label = 'Координата u', valmin = u_min, valmax = u_max, valinit = 0)
v_slider = Slider(ax = ax_v, label = 'Координата v', valmin = v_min, valmax = v_max, valinit = 0)

# Отрисовка исходной сетки
for i in range(num_of_u):
    ax1.plot(U[i, :], V[i, :], 'gray', alpha=0.3)
for i in range(num_of_v):
    ax1.plot(U[:, i], V[:, i], 'gray', alpha=0.3)
ax1.set_title("Исходная сетка")
ax1.set_aspect('equal')
ax1.set_xlabel('Ось U', fontsize=12, color='red')
ax1.set_ylabel('Ось V', fontsize=12, color='green')

# Отрисовка преобразованной сетки
ax2.plot_surface(X, Y, Z, cmap='viridis', alpha=0.0)
#ax2.plot_wireframe(X, Y, Z, color = 'gray')
ax2.set_title("После отображения")
ax2.set_aspect('equal')
ax2.set_xlabel('Ось X', fontsize=12, color='red')
ax2.set_ylabel('Ось Y', fontsize=12, color='green')
ax2.set_zlabel('Ось Z', fontsize=12, color='blue', labelpad=10)

vec_u = ax2.quiver(0, 0, 0, 0, 0, 0, color='red')
vec_v = ax2.quiver(0, 0, 0, 0, 0, 0, color='blue')
vec_normal = ax2.quiver(0, 0, 0, 0, 0, 0, color='green')
# векторное поле в точке
vec_xi = ax2.quiver(0, 0, 0, 0, 0, 0, color='pink')
# Куда тянет вектор векторного поля (без проекции на касательную плоскость)
vec_xi_u = ax2.quiver(0, 0, 0, 0, 0, 0, color='red')
vec_xi_v = ax2.quiver(0, 0, 0, 0, 0, 0, color='blue')

# Отрисовка касательного поля
step = 1
length = 0.3
should_normalize = False
X_xi, Y_xi, Z_xi = xi(U, V, (Xu, Yu, Zu), (Xv, Yv, Zv))
ax2.quiver(
    X[::step, ::step], Y[::step, ::step], Z[::step, ::step], 
    X_xi[::step, ::step], Y_xi[::step, ::step], Z_xi[::step, ::step], 
    color='magenta', length=length, normalize=should_normalize, 
    alpha=0.3,
)

# Update function
def update(val):
    u = u_slider.val
    v = v_slider.val
    p0 = [u, v]
    p0t = surface.transform(p0[0], p0[1])

    dot2d.set_data([p0[0]], [p0[1]])

    dot3d.set_data([p0t[0]], [p0t[1]])
    dot3d.set_3d_properties([p0t[2]]) # Для 3D оси Z обновляется отдельно

    x, y, z = surface.X(u, v), surface.Y(u, v), surface.Z(u, v)
    xu, yu, zu = surface.Xu(u, v), surface.Yu(u, v), surface.Zu(u, v)
    xv, yv, zv = surface.Xv(u, v), surface.Yv(u, v), surface.Zv(u, v)
    x_xi, y_xi, z_xi = xi(u, v, (xu, yu, zu), (xv, yv, zv))
    x_xi_u, y_xi_u, z_xi_u = d_xi_d_u(u, v, surface.r_u(u, v), surface.r_v(u, v),  surface.r_uu(u, v), surface.r_vu(u, v))
    x_xi_v, y_xi_v, z_xi_v = d_xi_d_v(u, v, surface.r_u(u, v), surface.r_v(u, v), surface.r_uv(u, v), surface.r_vv(u, v))

    global vec_u # чтобы использовалсь существующая переменная, объявленная вне этой функции
    global vec_v
    global vec_xi
    global vec_xi_u
    global vec_xi_v
    
    # 1. Стираем старый вектор, если он существует
    if vec_u is not None:
        vec_u.remove()
    if vec_v is not None:
        vec_v.remove()
    if vec_xi is not None:
        vec_xi.remove()
    if vec_xi_u is not None:
        vec_xi_u.remove()
    if vec_xi_v is not None:
        vec_xi_v.remove()

    vec_u=ax2.quiver(x, y, z, xu, yu, zu, color='red')
    vec_v=ax2.quiver(x, y, z, xv, yv, zv, color='blue')
    vec_xi=ax2.quiver(x, y, z, x_xi, y_xi, z_xi, color='purple')
    vec_xi_u=ax2.quiver(x + x_xi, y + y_xi, z + z_xi, x_xi_u, y_xi_u, z_xi_u, color='red', linestyle='dashed')
    vec_xi_v=ax2.quiver(x + x_xi, y + y_xi, z + z_xi, x_xi_v, y_xi_v, z_xi_v, color='blue', linestyle='dashed')

    fig.canvas.draw_idle()

u_slider.on_changed(update)
v_slider.on_changed(update)

update(0)

plt.show()
