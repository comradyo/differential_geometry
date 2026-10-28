import { Vec } from './vector.js';
import * as vectors from './vector.js';

class GammaMatrix {

}

// Базовый класс для поверхностей
export class Surface2D {
    // Вспомогательный метод для эмуляции векторизации NumPy
    // Принимает переменные и функцию-формулу, которую нужно применить
    vectorize(u, v, formula) {
        if (Array.isArray(u) && Array.isArray(v)) {
            // Если пришли два массива одинаковой длины (как координаты сетки)
            return u.map((uVal, index) => formula(uVal, v[index]));
        } else if (Array.isArray(u)) {
            // Если u — массив, а v — одиночное число
            return u.map(uVal => formula(uVal, v));
        } else if (Array.isArray(v)) {
            // Если v — массив, а u — одиночное число
            return v.map(vVal => formula(u, vVal));
        } else {
            // Если оба аргумента — обычные числа (скаляры)
            return formula(u, v);
        }
    }

    transform(u, v) {
        return [this.X(u, v), this.Y(u, v), this.Z(u, v)];
    }

    r_u(u, v) {
        return new Vec([this.Xu(u, v), this.Yu(u, v), this.Zu(u, v)]);
    }

    r_v(u, v) {
        return new Vec([this.Xv(u, v), this.Yv(u, v), this.Zv(u, v)]);
    }

    G(u, v) {
        return [
            [
                vectors.dot(this.r_u(u, v), this.r_u(u, v)),
                vectors.dot(this.r_u(u, v), this.r_v(u, v)),
            ],
            [
                vectors.dot(this.r_v(u, v), this.r_u(u, v)),
                vectors.dot(this.r_v(u, v), this.r_v(u, v)),
            ],
        ];
    }

    G_inverse(u, v) {
        let g = this.G(u, v);
        let det = g[0][0] * g[1][1] - g[0][1] ** 2;
        return [
            [
                [g[1][1] / det, -g[0][1] / det],
                [-g[1][0] / det, g[0][0] / det],
            ]
        ];
    }

    // Вектора частной производной по двум переменным
    r_uu(u, v) {
        return new Vec([this.Xuu(u, v), this.Yuu(u, v), this.Zuu(u, v)]);
    }

    r_uv(u, v) {
        return new Vec([this.Xuv(u, v), this.Yuv(u, v), this.Zuv(u, v)]);
    }

    r_vu(u, v) {
        return new Vec([this.Xvu(u, v), this.Yvu(u, v), this.Zvu(u, v)]);
    }

    r_vv(u, v) {
        return new Vec([this.Xvv(u, v), this.Yvv(u, v), this.Zvv(u, v)]);
    }

    // Матрица частных производных по i и j векторам
    second_derivative_matrix(u, v) {
        return [
            [this.r_uu(u, v), this.r_uv(u, v)],
            [this.r_vu(u, v), this.r_vv(u, v)],
        ];
    }

    // Символ Кристоффеля 2-го рода
    christoffel_symbol(i, j, k, g_inv, scnd_der_mtrx, r_u, r_v) {
        // По формуле, которую вывел в конспекте
        return g_inv[k][0] * vectors.dot(scnd_der_mtrx[i][j], r_u)
            + g_inv[k][1] * vectors.dot(scnd_der_mtrx[i][j], r_v);
    }

    // Символы кристоффеля (матрица 2x2x2, элемент - ijk)
    // TODO: Возможно, имеет смысл возвращать [k][i][j], но это потом
    Christoffel_Symbols_Old(u, v) {
        const g_inv = this.G_inverse(u, v);
        const scnd = this.second_derivative_matrix(u, v);
        const r_u = this.r_u(u, v);
        const r_v = this.r_v(u, v);

        const res = Array.from({ length: 2 }, () =>
            Array.from({ length: 2 }, () => [0, 0])
        );

        for (let i = 0; i < 2; i++) {
            for (let j = 0; j < 2; j++) {
                const a = vectors.dot(scnd[i][j], r_u);
                const b = vectors.dot(scnd[i][j], r_v);

                for (let k = 0; k < 2; k++) {
                    res[i][j][k] =
                        g_inv[k][0] * a +
                        g_inv[k][1] * b;
                }
            }
        }

        return res;
    }

    // Символы кристоффеля, оптимизированная версия
    Christoffel_Symbols(u, v) {
        const g_inv = this.G_inverse(u, v);

        let x_u = this.Xu(u, v), y_u = this.Yu(u, v), z_u = this.Zu(u, v);
        let x_v = this.Xv(u, v), y_v = this.Yv(u, v), z_v = this.Zv(u, v);
        let x_uu = this.Xuu(u, v);
        let x_uv = this.Xuv(u, v);
        let x_vu = this.Xvu(u, v);
        let x_vv = this.Xvv(u, v);
        let y_uu = this.Yuu(u, v);
        let y_uv = this.Yuv(u, v);
        let y_vu = this.Yvu(u, v);
        let y_vv = this.Yvv(u, v);
        let z_uu = this.Zuu(u, v);
        let z_uv = this.Zuv(u, v);
        let z_vu = this.Zvu(u, v);
        let z_vv = this.Zvv(u, v);

        let u00 = x_uu * x_u + y_uu * y_u + z_uu * z_u;
        let v00 = x_uu * x_v + y_uu * y_v + z_uu * z_v;
        let u01 = x_uv * x_u + y_uv * y_u + z_uv * z_u;
        let v01 = x_uv * x_v + y_uv * y_v + z_uv * z_v;
        let u10 = x_vu * x_u + y_vu * y_u + z_vu * z_u;
        let v10 = x_vu * x_v + y_vu * y_v + z_vu * z_v;
        let u11 = x_vv * x_u + y_vv * y_u + z_vv * z_u;
        let v11 = x_vv * x_v + y_vv * y_v + z_vv * z_v;

        return [
            [
                [g_inv[0][0] * u00 + g_inv[0][1] * v00, g_inv[1][0] * u00 + g_inv[1][1] * v00],
                [g_inv[0][0] * u01 + g_inv[0][1] * v01, g_inv[1][0] * u01 + g_inv[1][1] * v01],
            ],
            [
                [g_inv[0][0] * u10 + g_inv[0][1] * v10, g_inv[1][0] * u10 + g_inv[1][1] * v10],
                [g_inv[0][0] * u11 + g_inv[0][1] * v11, g_inv[1][0] * u11 + g_inv[1][1] * v11],
            ],
        ];
    }

}

// Класс Сферы, наследующий Surface2D
export class Sphere extends Surface2D {
    X(u, v) {
        return Math.cos(u) * Math.sin(v);
    }

    Y(u, v) {
        return Math.sin(u) * Math.sin(v)
    }

    Z(u, v) {
        return Math.cos(v)
    }

    // Частные производные по u
    Xu(u, v) {
        return -Math.sin(u) * Math.sin(v)
    }

    Yu(u, v) {
        return Math.cos(u) * Math.sin(v)
    }

    Zu(u, v) {
        return 0
    }

    // Частные производные по v
    Xv(u, v) {
        return Math.cos(u) * Math.cos(v)
    }

    Yv(u, v) {
        return Math.sin(u) * Math.cos(v)
    }

    Zv(u, v) {
        return -Math.sin(v)
    }

    // Вторые частные производные по u
    Xuu(u, v) {
        return -Math.cos(u) * Math.sin(v)
    }

    Yuu(u, v) {
        return -Math.sin(u) * Math.sin(v)
    }

    Zuu(u, v) {
        return 0
    }

    Xvu(u, v) {
        return -Math.sin(u) * Math.cos(v)
    }

    Yvu(u, v) {
        return  Math.cos(u) * Math.cos(v)
    }

    Zvu(u, v) {
        return 0
    }

    // Вторые частные производные по v
    Xuv(u, v) {
        return -Math.sin(u) * Math.cos(v);
    }

    Yuv(u, v) {
        return  Math.cos(u) * Math.cos(v);
    }

    Zuv(u, v) {
        return 0;
    }

    Xvv(u, v) {
        return -Math.cos(u) * Math.sin(v);
    }

    Yvv(u, v) {
        return -Math.sin(u) * Math.sin(v);
    }

    Zvv(u, v) {
        return -Math.cos(v);
    }

    // TODO: здесь мб тоже нужна векторизация?
    G(u, v) {
        return [
            [Math.sin(v) ** 2, 0],
            [0, 1],
        ];
    }

    G_inverse(u, v) {
        // 0.000001 - костыль для избежания деления на 0
        return [
            [1 / (Math.sin(v + 0.000001) ** 2), 0],
            [0, 1],
        ];
    }

}


// Плоскость
export class Plane extends Surface2D {
    X(u, v) {
        return u;
    }

    Y(u, v) {
        return v;
    }

    Z(u, v) {
        return  0;
    }

    // Частные производные по u
    Xu(u, v) {
        return  1;
    }

    Yu(u, v) {
        return 0;
    }

    Zu(u, v) {
        return  0;
    }

    // Частные производные по v
    Xv(u, v) {
        return 0;
    }

    Yv(u, v) {
        return 1;
    }

    Zv(u, v) {
        return 0;
    }

    // Вторые частные производные по u
    Xuu(u, v) {
        return 0;
    }

    Yuu(u, v) {
        return 0;
    }

    Zuu(u, v) {
        return 0;
    }

    Xvu(u, v) {
        return 0;
    }

    Yvu(u, v) {
        return 0;
    }

    Zvu(u, v) {
        return 0;
    }

    // Вторые частные производные по v
    Xuv(u, v) {
        return 0;
    }

    Yuv(u, v) {
        return  0;
    }

    Zuv(u, v) {
        return 0;
    }

    Xvv(u, v) {
        return  0;
    }

    Yvv(u, v) {
        return 0;
    }

    Zvv(u, v) {
        return  0;
    }

    G(u, v) {
        return [
            [1, 0],
            [0, 1],
        ];
    }

    G_inverse(u, v) {
        return [
            [1, 0],
            [0, 1],
        ];
    }
}
