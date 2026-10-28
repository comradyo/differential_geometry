import * as vectors from './vector.js'

const dAngle = 0.05; // на какой угол поворачивается камера при нажатии на кнопку

// Camera -- камера игрока
export class Camera {
    // TODO: нужно ли сюда пихать surface?
    constructor(fov_angle, surface) {
        this.fov_angle = fov_angle;
        this.surface = surface;
        this.u = 0;
        this.v = 0;
        this.coords = surface.transform(this.u, this.v);
        this.angle = 0;
        // Канонический базис в точке
        this.r_u = surface.r_u(this.u, this.v);
        this.r_v = surface.r_v(this.u, this.v);
        // Ортонормируем канонический базис
        this.ru_norm = this.r_u.normalize();
        this.rv_norm = this.r_v.sub(vectors.projection(this.r_v, this.ru_norm));
        this.rv_norm = this.rv_norm.div(this.rv_norm.norm());
        // Ортонормированный базис относительно направления взгляда
        // Направление взгляда совпадает с вектором e2
        this.e1 = this.ru_norm.mul(+Math.cos(this.angle)).add(this.rv_norm.mul(+Math.sin(this.angle)));
        this.e2 = this.ru_norm.mul(-Math.sin(this.angle)).add(this.rv_norm.mul(+Math.cos(this.angle)));

    }

    updateBasis() {
        this.coords = this.surface.transform(this.u, this.v);
        // Канонический базис в точке
        this.r_u = this.surface.r_u(this.u, this.v);
        this.r_v = this.surface.r_v(this.u, this.v);
        // Ортонормируем канонический базис
        this.ru_norm = this.r_u.normalize();
        this.rv_norm = this.r_v.sub(vectors.projection(this.r_v, this.ru_norm));
        this.rv_norm = this.rv_norm.div(this.rv_norm.norm());
    }

    updateViewBasis() {
        this.e1 = this.ru_norm.mul(+Math.cos(this.angle)).add(this.rv_norm.mul(+Math.sin(this.angle)));
        this.e2 = this.ru_norm.mul(-Math.sin(this.angle)).add(this.rv_norm.mul(+Math.cos(this.angle)));
    }

    turnLeft() {
        this.angle -= dAngle;
        this.updateViewBasis();
    }

    turnRight() {
        this.angle += dAngle;
        this.updateViewBasis();
    }

    setCoords(u, v) {
        this.u = u;
        this.v = v;
        this.updateBasis();
        this.updateViewBasis();
    }

    moveForward() {

    }

    moveBackward() {

    }

    // TODO: moveLeft, moveRight
}
