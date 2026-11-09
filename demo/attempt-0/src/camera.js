import * as vectors from './vector.js'
import * as calculations from './calculations.js'

const dAngle = 0.05; // на какой угол поворачивается камера при нажатии на кнопку
const dStep = 0.1; // Расстояние, на которое сдвигаемся при движении вперед
let maxTime = 0.05;
let dTime = 0.05;

// Плоскость Экрана - это плоскость e2, e3, где e3 - вектор, направленный к камере

// Мб излишняя и не сильно влияющая оптимизация
const k1Cam = new Float64Array(4);
const k2Cam = new Float64Array(4);
const k3Cam = new Float64Array(4);
const k4Cam = new Float64Array(4);

export class Screen {
    // TODO: мб считать не через пиксели, а через какие-то пропорции? А то как-то костыльно выглядит
    constructor(width, height, numOfPixelsX, numOfPixelsY) {
        this.setSizes(width, height, numOfPixelsX, numOfPixelsY)
    }

    setSizes(width, height, numOfPixelsX, numOfPixelsY) {
        this.numOfPixelsX = numOfPixelsX;
        this.numOfPixelsY = numOfPixelsY;
        this.pixelWidth = width / numOfPixelsX; // Ширина одного пикселя
        this.pixelHeight = height / numOfPixelsY; // Высота одного пикселя

        //this.centerPos = vectors.Vec(0, 0, 0); // позиция центра экрана (относительно начала координат касательной плоскости)
        //this.vecX = e2.mul(1/this.numOfPixelsX);
        //this.vecY = e3.mul(1/this.numOfPixelsX);
        //this.vecX = vectors.Vec([1/this.numOfPixelsX, 0]); // вектор одного пикселя по X плоскости экрана от центра экрана
        //this.vecY = vectors.Vec([0, 1/this.numOfPixelsY]); // вектор одного пикселя по Y плоскости экрана от центра экрана
    }

    // получить координаты пикселя в плоскости экрана (в пространстве относительно касательной плоскости).
    getPixelCoords(i, j) {
        // Смещение относительно центра экрана
        let iCoord = i - this.numOfPixelsX / 2;
        let jCoord = j - this.numOfPixelsY / 2;
        let x = this.pixelWidth * iCoord;
        let z = this.pixelHeight * jCoord;

        return {x, z};
    }
}

// Camera -- камера игрока
export class Camera {
    // TODO: нужно ли сюда пихать surface?
    constructor(fov_angle, distToScreen, screen, surface, z) {
        this.z = z; // Высота камеры относительно касательной плоскости
        this.distToScreen = distToScreen;
        this.screen = screen;

        this.fov_angle = fov_angle;
        this.surface = surface;
        this.u = 0;
        this.v = 0;
        this.pos = surface.transform(this.u, this.v); // координаты в объемлющем пространстве
        this.angle = 0; // Угол относительно rv
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
        this.pos = this.surface.transform(this.u, this.v);
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

    normalizeAngle() {
        if (this.angle < -Math.PI) {
            this.angle += 2 * Math.PI;
        } else if (this.angle > Math.PI) {
            this.angle -= 2 * Math.PI;
        }
    }

    turnLeft() {
        this.angle += dAngle; // Поворачиваемся в касательной плоскости, угол считается от оси X
        this.normalizeAngle();
        this.updateViewBasis();
    }

    turnRight() {
        this.angle -= dAngle;
        this.normalizeAngle();
        this.updateViewBasis();
    }

    setCoords(u, v) {
        this.u = u;
        this.v = v;
        this.updateBasis();
        this.updateViewBasis();
    }

    // Сдвигаемся на вектор длины dStep по направлению взгляда в течение 1 времени (экспоненциальное отображение)
    // e1 и e2 должны переноситься касательно вдоль этого вектора (мб достаточно будет параллельно переносить вектор взгляда)
    // А, правда, параллельный перенос можно выполнить, если у нас известна кривая, а тут, походу, 
    // просто будет расчёт геодезической вдоль вектора взгляда, но длины dStep, до момента времени 1.
    // Либо просто используем вектор взгляда и двигаемся ограниченное время (dTime)?
    moveForward() {
        let vec_view_decomp = vectors.decomposition(this.e2, this.r_u, this.r_v);
        let rayState = [this.u, this.v, vec_view_decomp[0], vec_view_decomp[1]];

        // TODO: нужен ли здесь цикл? Или просто один раз смещаемся?
        // Наверное, в игре нужен будет цикл - для инертности бега
        for (let t = 0; t < maxTime; t += dTime) {
            calculations.rk4StepInPlace(rayState, dTime, this.surface, k1Cam, k2Cam, k3Cam, k4Cam);
        }

        this.u = rayState[0];
        this.v = rayState[1];

        this.updateBasis();
        this.e2 = this.r_u.mul(rayState[2]).add(this.r_v.mul(rayState[3]));

        let angleBefore = this.angle;
        let newAngle = vectors.angle(this.e2, this.rv_norm);
        if (angleBefore * newAngle < 0) { // арккосинус может давать угол с другим знаком
            newAngle *= -1;
        }
        this.angle = newAngle;
    }

    moveBackward() {
        let vec_view_decomp = vectors.decomposition(this.e2.mul(-1), this.r_u, this.r_v);
        let rayState = [this.u, this.v, vec_view_decomp[0], vec_view_decomp[1]];

        for (let t = 0; t < maxTime; t += dTime) {
            calculations.rk4StepInPlace(rayState, dTime, this.surface, k1Cam, k2Cam, k3Cam, k4Cam);
        }

        this.u = rayState[0];
        this.v = rayState[1];

        this.updateBasis();
        this.e2 = this.r_u.mul(-rayState[2]).add(this.r_v.mul(-rayState[3]));

        let angleBefore = this.angle;
        let newAngle = vectors.angle(this.e2, this.rv_norm);
        if (angleBefore * newAngle < 0) { // арккосинус может давать угол с другим знаком
            newAngle *= -1;
        }
        this.angle = newAngle;
    }

    // Получить координаты точки пересечения луча, исходящего из камеры и проходящего через пиксель экрана i, j
    // с касательной плоскостью (в координатах камеры)
    // TODO: понять, откуда начинается j, а то мб изображение перевёрнуто
    getIntersectionPoint(i, j) {
        let pixelCoords = this.screen.getPixelCoords(i, j);
        let proportion = this.z / pixelCoords.z;
        let pX = proportion * pixelCoords.x;
        let pY = proportion * this.distToScreen;

        return this.e1.mul(pX).add(this.e2.mul(pY));
    }

    getDistToIntersectionPoint(i, j) {
        let pixelCoords = this.screen.getPixelCoords(i, j);
        let proportion = Math.abs(this.z / pixelCoords.z);

        return proportion * Math.sqrt(
            pixelCoords.x * pixelCoords.x + this.distToScreen * this.distToScreen
        );
    }

    // TODO: moveLeft, moveRight
}
