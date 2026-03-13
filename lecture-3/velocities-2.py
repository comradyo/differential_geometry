import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# Пытаюсь отрисовывать движущаюся точку и векторы скоростей к ней, 
# а также касательную плоскость и нормаль

class Surface2D: # Parent Class
    def __init__(self, u_start, u_end, num_of_u_points, v_start, v_end, num_of_v_points):
        self.u = np.linspace(u_start, u_end, num_of_u_points)
        self.v = np.linspace(v_start, v_end, num_of_v_points)
        self.U, self.V = np.meshgrid(self.u, self.v)

    def get_data_to_draw(self):
        return

class Sphere(Surface2D): # Child Class
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

        return X,Y,Z,Xu,Yu,Zu,Xv,Yv,Zv

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

        return X,Y,Z,Xu,Yu,Zu,Xv,Yv,Zv

#u_start = 0
#u_end = 2*np.pi
#v_start=0
#v_end=np.pi
#surface = Sphere(u_start, u_end, 40, v_start, v_end, 40)

u_start = -5
u_end = 5
v_start=-5
v_end=5
surface = SurfaceWithCollinearVectors(u_start, u_end, 40, v_start, v_end, 40)

X, Y, Z, Xu, Yu, Zu, Xv, Yv, Zv = surface.get_data_to_draw()

fig = plt.figure()
ax1 = fig.add_axes([0, 0, 1, 0.8], projection = '3d')
# Аргумент: 4-tuple of floats rect = [left, bottom, width, height]. 
# A new Axes is added with dimensions rect in normalized (0, 1) units using ~.Figure.add_axes on the current figure.
ax_u = fig.add_axes([0.2, 0.85, 0.7, 0.1])
ax_v = fig.add_axes([0.2, 0.75, 0.7, 0.1])

u_slider = Slider(ax = ax_u, label = 'Значение u', valmin = u_start, valmax = u_end, valinit = (u_start + u_end) / 2)
v_slider = Slider(ax = ax_v, label = 'Значение v', valmin = v_start, valmax = v_end, valinit = (v_start + v_end) / 2)

aplha_level = 0.4

# 3. Update function
def update(val):
    u = u_slider.val
    v = v_slider.val
    ax1.cla()
    x, y, z = surface.X(u, v), surface.Y(u, v), surface.Z(u, v)
    xu, yu, zu = surface.Xu(u, v), surface.Yu(u, v), surface.Zu(u, v)
    xv, yv, zv = surface.Xv(u, v), surface.Yv(u, v), surface.Zv(u, v)
    ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=aplha_level)
    ax1.plot_wireframe(X, Y, Z, color = 'gray', rstride=2, cstride=2, alpha=0.3)
    ax1.scatter(x, y, z, marker='o', color='g', linewidths=5)
    ax1.quiver(x, y, z, xu, yu, zu, color='red', length=1)
    ax1.quiver(x, y, z, xv, yv, zv, color='blue', length=1)
    fig.canvas.draw_idle()

u_slider.on_changed(update)
v_slider.on_changed(update)
update(0)

plt.show()
