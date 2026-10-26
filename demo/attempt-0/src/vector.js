import { Vector3, ArrowHelper } from 'three';

// Vec -- класс векторов
export class Vec {
    constructor(data) {
        this.data = data instanceof Float64Array ? data : new Float64Array(data);
    }

    // Длина вектора
    norm() {
        const sumOfSquares = this.data.reduce((acc, val) => acc + val * val, 0);
        return Math.sqrt(sumOfSquares);
    }

    // Сложение векторов: v1.add(v2)
    add(v) {
        return new Vec(this.data.map((x, i) => x + v.data[i]));
    }

    // Вычитание векторов: v1.sub(v2)
    sub(v) {
        return new Vec(this.data.map((x, i) => x - v.data[i]));
    }

    // Умножение на скаляр
    mul(s) {
        return new Vec(this.data.map(x => x * s));
    }

    // Деление на скаляр
    div(s) {
        return new Vec(this.data.map(x => x / s));
    }

    // Нормализация вектора
    normalize() {
        return this.div(this.norm());
    }

    // Скалярное произведение
    dot(v) {
        return this.data.reduce((sum, x, i) => sum + x * v.data[i], 0);
    }

    // Пришлось идти на костыли из-за того, что normalize в моём модуле делает длину 0.999, 
    // а для стрелочек нужна 1
    toThreeVector3() {
        return new Vector3(this.data[0], this.data[1], this.data[2]);
    }

    toArray() {
        return Array.from(this.data); 
    }

    // Удобный вывод в консоль
    toString() {
        return `[${this.data.join(', ')}]`;
    }
}

// Скалярное произведение
export function dot(vec_a, vec_b) {
    return vec_a.data.reduce((sum, val, i) => sum + val * vec_b.data[i], 0);
}

// Векторная проекция вектора vec_arg на вектор vec_to
export function projection(vec_arg, vec_to) {
    return vec_to.mul(vec_to.dot(vec_arg) / vec_to.dot(vec_to));
}

// Угол между векторами в радианах
export function angle(vec_1, vec_2) {
    let cosRes = dot(vec_1, vec_2) / (vec_1.norm() * vec_2.norm())
    return Math.acos(cosRes);
}

// Разложение вектора vec по базису vec_e1, vec_e2
// TODO: мб возвращать вектор?
export function decomposition(vec, vec_e1, vec_e2) {
    /*
    Если вектор раскладывается по базису, то он записывается в виде v = a*e1 + b*e2. 
    Это можно расписать покоординатно и получить систему - 3 уравнение, 2 неизвестных. 
    Если взять первые 2 уравнения, их можно решить методом Крамера.
    */
    let det = vec_e1.data[0] * vec_e2.data[1] - vec_e2.data[0] * vec_e1.data[1]
    let det_e1_u = vec.data[0] * vec_e2.data[1] - vec_e2.data[0] * vec.data[1]
    let det_e1_v = vec_e1.data[0] * vec.data[1] - vec_e1.data[1] * vec.data[0]
    //Координаты e1 в базисе ru_norm, rv_norm
    let coord_e1 = det_e1_u / det
    let coord_e2 = det_e1_v / det

    return [coord_e1, coord_e2]
}

export class Arrow extends ArrowHelper {
    constructor(start, end, color, headLength, headWidth) {
        // Вызываем базовый конструктор с дефолтными значениями
        super(new Vector3(0, 1, 0), new Vector3(0, 0, 0), 1, color, headLength, headWidth);

        // Сразу инициализируем по двум точкам
        this.setPoints(start, end);
    }

    setPoints(start_dot, end_dot) {
        const start = new Vector3(start_dot[0], start_dot[1], start_dot[2]);
        const end = new Vector3(end_dot[0], end_dot[1], end_dot[2]);

        const dir = new Vector3().subVectors(end, start);
        const length = dir.length();
        dir.normalize();

        this.position.copy(start);
        this.setDirection(dir);
        this.setLength(length);
    }

    quiver(start_dot, dir_vec) {
        const start = new Vector3(start_dot[0], start_dot[1], start_dot[2]);
        const dir = new Vector3(dir_vec.data[0], dir_vec.data[1], dir_vec.data[2]);
        const length = dir.length();
        dir.normalize();

        this.position.copy(start);
        this.setDirection(dir);
        this.setLength(length);
    }
}
