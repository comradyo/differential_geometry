import scipy.integrate as integrate
import numpy as np

# Поверхность, описываемая двумерными координатами
class Surface2D:
    def __init__(
        self, u_start, u_end, num_of_u_points, v_start, v_end, num_of_v_points
    ):
        self.u = np.linspace(u_start, u_end, num_of_u_points)
        self.v = np.linspace(v_start, v_end, num_of_v_points)
        self.U, self.V = np.meshgrid(self.u, self.v)

    def transform(self, u, v):
        return self.X(u, v), self.Y(u, v), self.Z(u, v)

    def jacobian(self, u, v):
        return np.array(
            [
                [self.Xu(u, v), self.Xv(u, v)],
                [self.Yu(u, v), self.Yv(u, v)],
                [self.Zu(u, v), self.Zv(u, v)],
            ]
        )

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

        return self.U, self.V, X, Y, Z, Xu, Yu, Zu, Xv, Yv, Zv

    def r_u(self, u, v):
        return np.array([self.Xu(u, v), self.Yu(u, v), self.Zu(u, v)])

    def r_v(self, u, v):
        return np.array([self.Xv(u, v), self.Yv(u, v), self.Zv(u, v)])

    def G(self, u, v):
        return np.array(
            [
                [
                    np.dot(self.r_u(u, v), self.r_u(u, v)),
                    np.dot(self.r_u(u, v), self.r_v(u, v)),
                ],
                [
                    np.dot(self.r_v(u, v), self.r_u(u, v)),
                    np.dot(self.r_v(u, v), self.r_v(u, v)),
                ],
            ]
        )

    def G_inverse(self, u, v):
        g = self.G(u, v)
        det = g[0][0] * g[1][1] - g[0][1] ** 2
        return (
            np.array(
                [
                    [g[1][1], -g[0][1]],
                    [-g[1][0], g[0][0]],
                ]
            )
            / det
        )

    def r_uu(self, u, v):
        return np.array([self.Xuu(u, v), self.Yuu(u, v), self.Zuu(u, v)])

    def r_uv(self, u, v):
        return np.array([self.Xuv(u, v), self.Yuv(u, v), self.Zuv(u, v)])

    def r_vu(self, u, v):
        return np.array([self.Xvu(u, v), self.Yvu(u, v), self.Zvu(u, v)])

    def r_vv(self, u, v):
        return np.array([self.Xvv(u, v), self.Yvv(u, v), self.Zvv(u, v)])

    # Матрица частных производных по i и j векторам
    def second_derivative_matrix(self, u, v):
        return np.array(
            [
                [self.r_uu(u, v), self.r_uv(u, v)],
                [self.r_vu(u, v), self.r_vv(u, v)],
            ]
        )

    # Символ Кристоффеля 2-го рода (хз, нужен ли будет 1-й)
    def _christoffel_symbol(self, i, j, k, g_inv, scnd_der_mtrx, r_u, r_v):
        # По формуле, которую вывел в конспекте
        return g_inv[k][0] * np.dot(scnd_der_mtrx[i][j], r_u) + g_inv[k][1] * np.dot(
            scnd_der_mtrx[i][j], r_v
        )

    # Символ кристоффеля (матрица 2x2x2, элемент - ijk)
    # TODO: Возможно, имеет смысл возвращать [k][i][j], но это потом
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
                    res[i][j][k] = self._christoffel_symbol(
                        i, j, k, g_inv, scnd_der_mtrx, r_u, r_v
                    )

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
        return np.array(
            [
                [np.sin(v) ** 2, 0],
                [0, 1],
            ]
        )

    def G_inverse(self, u, v):
        # 0.000001 - костыль для избежания деления на 0
        return np.array(
            [
                [1 / (np.sin(v + 0.000001) ** 2), 0],
                [0, 1],
            ]
        )


class SurfaceWithCollinearVectors(Surface2D):
    def X(self, u, v):
        return u**2 / 2 + u * v - v**2 / 2

    def Y(self, u, v):
        return u**2 / 2 + u * v + v**3 / 3

    def Z(self, u, v):
        return u + np.sin(v)

    # частные производные по u
    def Xu(self, u, v):
        return u + v

    def Yu(self, u, v):
        return u + v

    def Zu(self, u, v):
        return np.ones_like(u)

    # частные производные по v
    def Xv(self, u, v):
        return u - v

    def Yv(self, u, v):
        return u + v**2

    def Zv(self, u, v):
        return np.ones_like(u) * np.cos(v)

    # Вторые частные производные по u
    def Xuu(self, u, v):
        return np.ones_like(u)

    def Yuu(self, u, v):
        return np.ones_like(u)

    def Zuu(self, u, v):
        return np.zeros_like(u)

    def Xvu(self, u, v):
        return np.ones_like(u)

    def Yvu(self, u, v):
        return np.ones_like(u)

    def Zvu(self, u, v):
        return np.zeros_like(u)

    # Вторые частные производные по v
    def Xuv(self, u, v):
        return np.ones_like(v)

    def Yuv(self, u, v):
        return np.ones_like(v)

    def Zuv(self, u, v):
        return np.zeros_like(u)

    def Xvv(self, u, v):
        return -np.ones_like(v)

    def Yvv(self, u, v):
        return 2 * v

    def Zvv(self, u, v):
        return -np.sin(v)

# TODO: тор, конус, гипербола

# Плоскость
class Plane(Surface2D):
    def X(self, u, v):
        return u

    def Y(self, u, v):
        return v

    def Z(self, u, v):
        return np.zeros_like(u)

    # Частные производные по u
    def Xu(self, u, v):
        return np.ones_like(u)

    def Yu(self, u, v):
        return np.zeros_like(u)

    def Zu(self, u, v):
        return np.zeros_like(u)

    # Частные производные по v
    def Xv(self, u, v):
        return np.zeros_like(v)

    def Yv(self, u, v):
        return np.ones_like(v)

    def Zv(self, u, v):
        return np.zeros_like(v)

    # Вторые частные производные по u
    def Xuu(self, u, v):
        return np.zeros_like(u)

    def Yuu(self, u, v):
        return np.zeros_like(u)

    def Zuu(self, u, v):
        return np.zeros_like(u)

    def Xvu(self, u, v):
        return np.zeros_like(u)

    def Yvu(self, u, v):
        return np.zeros_like(u)

    def Zvu(self, u, v):
        return np.zeros_like(u)

    # Вторые частные производные по v
    def Xuv(self, u, v):
        return np.zeros_like(u)

    def Yuv(self, u, v):
        return np.zeros_like(u)

    def Zuv(self, u, v):
        return np.zeros_like(u)

    def Xvv(self, u, v):
        return np.zeros_like(u)

    def Yvv(self, u, v):
        return np.zeros_like(u)

    def Zvv(self, u, v):
        return np.zeros_like(u)

    def G(self, u, v):
        return np.array(
            [
                [1, 0],
                [0, 1],
            ]
        )

    def G_inverse(self, u, v):
        return np.array(
            [
                [1, 0],
                [0, 1],
            ]
        )
