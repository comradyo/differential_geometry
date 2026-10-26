import {Vec} from './vector.js'; 
import * as vectors from './vector.js';

const dotProduct = (a, b) => a.reduce((sum, val, i) => sum + val * b[i], 0);

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

    Xu(u, v) { return `Parent Xu`; }
    Yu(u, v) { return `Parent Yu`; }
    Zu(u, v) { return `Parent Zu`; }

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

    // Символ кристоффеля (матрица 2x2x2, элемент - ijk)
    // TODO: Возможно, имеет смысл возвращать [k][i][j], но это потом
    Christoffel_Symbols(u, v) {
        // TODO: как-то оптимизировать расчёты,
        let g_inv = this.G_inverse(u, v);
        let scnd_der_mtrx = this.second_derivative_matrix(u, v);
        let r_u = this.r_u(u, v);
        let r_v = this.r_v(u, v);

        // Создание массива 2 x 2 x 2
        const res = Array.from({ length: 2 }, () =>
            Array.from({ length: 2 }, () =>
                Array.from({ length: 2 }, () => 0)
            )
        );

        for (let i = 0; i < 2; i++) {
            for (let j = 0; j < 2; j++) {
                for (let k = 0; k < 2; k++) {
                    res[i][j][k] = this.christoffel_symbol(
                        i, j, k, g_inv, scnd_der_mtrx, r_u, r_v
                    )
                }
            }
        }

        return res;
    }

}

// Класс Сферы, наследующий Surface2D
export class Sphere extends Surface2D {
    X(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => Math.cos(uVal) * Math.sin(vVal));
    }

    Y(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => Math.sin(uVal) * Math.sin(vVal));
    }

    Z(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => Math.cos(vVal));
    }

    // Частные производные по u
    Xu(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => -Math.sin(uVal) * Math.sin(vVal));
    }

    Yu(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => Math.cos(uVal) * Math.sin(vVal));
    }

    Zu(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => 0);
    }

    // Частные производные по v
    Xv(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => Math.cos(uVal) * Math.cos(vVal));
    }

    Yv(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => Math.sin(uVal) * Math.cos(vVal));
    }

    Zv(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => -Math.sin(vVal));
    }

    // Вторые частные производные по u
    Xuu(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => -Math.cos(uVal) * Math.sin(vVal));
    }

    Yuu(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => -Math.sin(uVal) * Math.sin(vVal));
    }

    Zuu(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => 0);
    }

    Xvu(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => -Math.sin(uVal) * Math.cos(vVal));
    }

    Yvu(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => Math.cos(uVal) * Math.cos(vVal));
    }

    Zvu(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => 0);
    }

    // Вторые частные производные по v
    Xuv(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => -Math.sin(uVal) * Math.cos(vVal));
    }

    Yuv(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => Math.cos(uVal) * Math.cos(vVal));
    }

    Zuv(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => 0);
    }

    Xvv(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => -Math.cos(uVal) * Math.sin(vVal));
    }

    Yvv(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => -Math.sin(uVal) * Math.sin(vVal));
    }

    Zvv(u, v) {
        return this.vectorize(u, v, (uVal, vVal) => -Math.cos(vVal));
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
