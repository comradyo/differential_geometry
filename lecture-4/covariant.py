import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys

# Что хочу тут увидеть:
# 1. Расчёт матрицы 1-й ФФ 
# 2. Расчёт обратной матрицы к ней
# 3. Ковариантное дифференцирование вдоль координатных векторов (?)
# 4. Ковариантное дифференцирование вдоль кривой (?)
# 5. Параллельный перенос касательного вдоль кривой (возможно, в отдельном файле)
# 5.1. Касательное гладкое векторное поле - задать его, отрисовать, 
# в каждой точке раскладывать вектор из этого касательного векторного поля по каноническому базису

# 6. Расчёт символов Кристоффеля (хз, нужен ли 1-й род)
# 7. Из точки пускать пучок геодезических, отрисовывать их

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
        du = np.array([self.Xu(u, v), self.Yu(u, v), self.Zu(u, v)])
        dv = np.array([self.Xv(u, v), self.Yv(u, v), self.Zv(u, v)])
        return np.cross(du, dv)
    
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
    
    def r_u(self, u, v):
        return (self.Xu(u, v),self.Yu(u, v),self.Zu(u, v))

    def r_v(self, u, v):
        return (self.Xv(u, v),self.Yv(u, v),self.Zv(u, v))

    def G(self, u, v):
        return np.array([
            [np.dot(self.r_u(u, v), self.r_u(u, v)), np.dot(self.r_u(u, v), self.r_v(u, v))],
            [np.dot(self.r_v(u, v), self.r_u(u, v)), np.dot(self.r_v(u, v), self.r_v(u, v))],
        ])

    def G_inverse(self, u, v):
        g = self.G(u, v)
        det = g[0][0] * g[1][1] - g[0][1] ** 2
        return np.array([
            [g[1][1], -g[0][1]],
            [-g[1][0], g[0][0]],
        ]) / det

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
    
    # Матрица частных производных по i и j векторам
    def second_derivative_matrix(self, u, v):
        return np.array([
            [self.r_uu(u, v), self.r_uv(u, v)],
            [self.r_vu(u, v), self.r_vv(u, v)],
        ])

    # Символ Кристоффеля 2-го рода (хз, нужен ли будет 1-й)
    def _christoffel_symbol(self, i, j, k, g_inv, scnd_der_mtrx, r_u, r_v):
        # По формуле, которую вывел в конспекте
        return g_inv[k][0] * np.dot(scnd_der_mtrx[i][j], r_u) + g_inv[k][1] * np.dot(scnd_der_mtrx[i][j], r_v)

    def Christoffel_Symbols(self, u, v):
        # TODO: как-то оптимизировать расчёты, 
        # так как тут два вычисления одного и того же
        g_inv = self.G_inverse(u, v)
        scnd_der_mtrx = self.second_derivative_matrix(u, v)
        r_u = self.r_u(u, v)
        r_v = self.r_v(u, v)
        res = np.zeros((2, 2, 2))
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    res[i][j][k] = self._christoffel_symbol(i, j, k, g_inv, scnd_der_mtrx, r_u, r_v)

        return res    

class Sphere(Surface2D):
    def X(self, u, v):
        return np.cos(u) * np.sin(v)
    def Y(self, u, v):
        return np.sin(u) * np.sin(v)
    def Z(self, u, v):
        return np.cos(v)
    # Частные производные по u
    def Xu(self, u, v):
        return -np.sin(u) * np.sin(v)
    def Yu(self, u, v):
        return np.cos(u) * np.sin(v)
    def Zu(self, u, v):
        return np.zeros_like(u)
    # Частные производные по v
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
    
    def G(self, u, v):
        return np.array([
            [np.sin(v) ** 2, 0],
            [0, 1],
        ])
    def G_inverse(self, u, v):
        return np.array([
            [1/(np.sin(v) ** 2), 0],
            [0, 1],
        ])

class SurfaceWithCollinearVectors(Surface2D):
    def X(self, u, v):
        return u**2/2 + u*v - v**2/2
    def Y(self, u, v):
        return u**2/2 + u*v + v**3/3
    def Z(self, u, v):
        return u + np.sin(v)
    # частные производные по u
    def Xu(self, u, v):
        return u+v
    def Yu(self, u, v):
        return u+v
    def Zu(self, u, v):
        return np.ones_like(u)
    # частные производные по v
    def Xv(self, u, v):
        return u-v
    def Yv(self, u, v):
        return u + v**2
    def Zv(self, u, v):
        return np.ones_like(u) * np.cos(v)

def curve(t):
    return 2*t, np.cos(t)

u_min=0
u_max=2*np.pi
v_min=0
v_max=np.pi
num_of_u=20
num_of_v=20
surface = Sphere(u_min, u_max, num_of_u, v_min, v_max, num_of_v)

#u_min = -5
#u_max = 5
#v_min=-5
#v_max=5
#num_of_u=40
#num_of_v=40
#surface = SurfaceWithCollinearVectors(u_min, u_max, num_of_u, v_min, v_max, num_of_v)

U, V, X, Y, Z, Xu, Yu, Zu, Xv, Yv, Zv = surface.get_data_to_draw()

# Фигуры
fig = plt.figure(figsize=(14, 6))
plt.subplots_adjust(bottom=0.25)

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
ax2.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)
ax2.set_title("После отображения")
ax2.set_aspect('equal')
ax2.set_xlabel('Ось X', fontsize=12, color='red')
ax2.set_ylabel('Ось Y', fontsize=12, color='green')
ax2.set_zlabel('Ось Z', fontsize=12, color='blue', labelpad=10)

vec_u = ax2.quiver(0, 0, 0, 0, 0, 0, color='red')
vec_v = ax2.quiver(0, 0, 0, 0, 0, 0, color='blue')
vec_normal = ax2.quiver(0, 0, 0, 0, 0, 0, color='green')

eps = 0.4
u_square = np.linspace(-eps, eps, 5)
v_square = np.linspace(-eps, eps, 5)
# Квадрат 
Du, Dv = np.meshgrid(u_square, v_square)
Dx, Dy, Dz = surface.transform(Du, Dv)

grid_lines = []

for i in range(len(Du)):
    line, = ax1.plot([], [], color='red')
    grid_lines.append(line)

for i in range(len(Dv)):
    line, = ax1.plot([], [], color='red')
    grid_lines.append(line)

grid_lines_3d = []

for i in range(len(Dx)):
    line, = ax2.plot([], [], color='red')
    grid_lines_3d.append(line)

for i in range(len(Dy)):
    line, = ax2.plot([], [], color='red')
    grid_lines_3d.append(line)

for i in range(len(Dz)):
    line, = ax2.plot([], [], color='red')
    grid_lines_3d.append(line)

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

    global vec_u # чтобы использовалсь существующая переменная, объявленная вне этой функции
    global vec_v
    global vec_normal
    
    # 1. Стираем старый вектор, если он существует
    if vec_u is not None:
        vec_u.remove()
    if vec_v is not None:
        vec_v.remove()
    if vec_normal is not None:
        vec_normal.remove()

    vec_u=ax2.quiver(x, y, z, xu, yu, zu, color='red')
    vec_v=ax2.quiver(x, y, z, xv, yv, zv, color='blue')

    # Сетка вокруг точки
    U_square = p0[0] + Du
    V_square = p0[1] + Dv

    k = 0

    for i in range(len(U_square)):
        grid_lines[k].set_data(
            U_square[i, :],
            V_square[i, :]
        )
        k += 1

    for i in range(len(V_square)):
        grid_lines[k].set_data(
            U_square[:, i],
            V_square[:, i]
        )
        k += 1
    
    # Преобразованная сетка:
    X_square, Y_square, Z_square = surface.transform(U_square, V_square)

    k = 0

    for i in range(X_square.shape[0]):
        grid_lines_3d[k].set_data(
            X_square[i, :],
            Y_square[i, :]
        )
        grid_lines_3d[k].set_3d_properties(
            Z_square[i, :]
        )
        k += 1

    for i in range(X_square.shape[1]):
        grid_lines_3d[k].set_data(
            X_square[:, i],
            Y_square[:, i]
        )
        grid_lines_3d[k].set_3d_properties(
            Z_square[:, i]
        )
        k += 1

    # Отрисовка нормали плоскости
    norm = surface.normal(u, v)
    vec_normal=ax2.quiver(x, y, z, norm[0], norm[1], norm[2], color='green')

    # Матрица первой фундаментальной формы
    print("")
    G_matrix = surface.G(u, v)
    matrix_string = '\n'.join('   '.join(f'{num:.5f}' for num in row) for row in G_matrix)
    print("Fisrt fundamental form:")
    print(matrix_string)
    G_inv_matrix = surface.G_inverse(u, v)
    matrix_string = '\n'.join('   '.join(f'{num:.5f}' for num in row) for row in G_inv_matrix)
    print("Inverse:")
    print(matrix_string)

    print("Christoffel_Symbols:")
    chr_symb = surface.Christoffel_Symbols(u, v)
    print(chr_symb)

    fig.canvas.draw_idle()

u_slider.on_changed(update)
v_slider.on_changed(update)

update(0)

plt.show()
