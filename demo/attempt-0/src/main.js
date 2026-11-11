import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import Stats from 'stats.js';
import * as surfaces from './surface.js';
import { Vec, Arrow } from './vector.js';
import * as vectors from './vector.js';
import * as calculations from './calculations.js'
import * as cameras from './camera.js'
import * as texture_loader from './texture.js'

// Задаем фиксированное низкое разрешение для расчётов
const RENDER_W = 500;
const RENDER_H = 500;

let dT = 0.01;
let maxNumOfSteps = 10000;
const dAngleWidening = Math.PI / 100; // Для расширения/сужения угла обзора

// Угол обзора камеры на поверхности
let fov_angle_degrees = 60.0;
let fov_angle = Math.PI * fov_angle_degrees / 180.0;
let distToScreen = 0.5;
let dDistToScreen = 0.1;
// Число геодезических, которые будут отрисовываны на 3D изображении
const numOfGeodesicLines = 1;
// Угол в проекции на касательную плоскость между соседними пикселями с вершиной в камере
let dAngle = fov_angle / RENDER_W;
// Угол в проекции на касательную плоскость между геодезическими
let dAngleGeodesics = fov_angle / numOfGeodesicLines;

// Кажется, это должна быть внутренняя структура, связанная только с камерой, 
// и ширина/высота должны рассчитывать только исходя из расстояния до экрана + угла обзора 
// (видимо, должен быть угол обзора и по вертикали)
const screenWidth = 2 * Math.tan(fov_angle / 2) * distToScreen;
const screenHeight = 0.2;
const screen = new cameras.Screen(screenWidth, screenHeight, 200, 100);

const dZ = 0.01;
const cameraZ = 0.1;
const planeLength = 10;
const planeWidth = 10;
const surface = new surfaces.Sphere();
//const surface = new surfaces.Plane(planeLength, planeWidth);
const camera = new cameras.Camera(fov_angle, distToScreen, screen, surface, cameraZ);
camera.setCoords(0, 0.1);

// --- 1. НАСТРОЙКА ЛЕВОГО ОКНА (Three.js) ---
const leftContainer = document.getElementById('left-window');

// Контейнер для отображения статистики и других данных
let statsDiv = document.createElement("div");
// Расположение в правом верхнем углу
statsDiv.style.position = 'absolute';
statsDiv.style.top = '0px';
statsDiv.style.left = 'auto';
statsDiv.style.right = '0px';
statsDiv.style.color = 'purple';
leftContainer.appendChild(statsDiv);

// Счётчик для статистики
const stats = new Stats();
stats.showPanel(1); // 0: fps, 1: ms, 2: mb, 3+: custom
stats.dom.style.position = 'relative'; // или 'absolute' / 'inherit'
stats.dom.style.top = 'auto';
stats.dom.style.left = 'auto';
statsDiv.appendChild(stats.dom);

let posDiv = document.createElement("div");
posDiv.style.color = 'red';
statsDiv.appendChild(posDiv);

let posDiv1 = document.createElement("div");
posDiv1.style.color = 'green';
statsDiv.appendChild(posDiv1);

let posDiv2 = document.createElement("div");
posDiv2.style.color = 'blue';
statsDiv.appendChild(posDiv2);

// Создаем сцену, камеру и рендерер
const scene = new THREE.Scene();
const threeCamera = new THREE.PerspectiveCamera(75, (window.innerWidth / 2) / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

threeCamera.position.set(2, 2, 2);
threeCamera.up.set(0, 0, 1); // Z — это верх

// Задаем размер рендерера ровно под левое окно
renderer.setSize(window.innerWidth / 2, window.innerHeight);
leftContainer.appendChild(renderer.domElement);

// Создаем контроллер орбиты, передаем камеру и элемент, который будет слушать мышь
const controls = new OrbitControls(threeCamera, renderer.domElement);
// По желанию настраиваем плавность (инерцию) вращения
controls.enableDamping = true;
controls.dampingFactor = 0.05;

//const surfaceTextureURL = 'src/123.png';
const surfaceTextureURL = 'src/earth.jpg';
texture_loader.loadTextureToCPU(surfaceTextureURL);

// 1. Создаем каркас сферы (радиус, сегменты по u, сегменты по v)
const sphereGeometry = new THREE.SphereGeometry(1, 64, 64);
sphereGeometry.rotateX(Math.PI / 2); // Нужно для того, чтобы полюса были на оси z.
sphereGeometry.rotateZ(Math.PI); // Образ нулевого столбца текстуры будет лежать в плоскости xOz
// 2. Создаем материал
const textureLoader = new THREE.TextureLoader();
const earthTexture = textureLoader.load(surfaceTextureURL); // пример текстуры из доков Three.js
const surfaceMaterial = new THREE.MeshBasicMaterial({ map: earthTexture });
// 3. Объединяем геометрию и материал в один объект и добавляем на сцену
const sphereMesh = new THREE.Mesh(sphereGeometry, surfaceMaterial);

const planeGeometry = new THREE.PlaneGeometry(planeLength, planeWidth);
const planeMesh = new THREE.Mesh(planeGeometry, surfaceMaterial);
planeMesh.position.set(planeLength / 2, planeWidth / 2, 0);

scene.add(sphereMesh);
//scene.add(planeMesh);

// Камера на поверхности
const playerGeometry = new THREE.SphereGeometry(0.03, 16, 16);
const playerMaterial = new THREE.MeshBasicMaterial({ color: "red" });
const playerMesh = new THREE.Mesh(playerGeometry, playerMaterial);
scene.add(playerMesh);

/////////////////
// Стрелочки
/////////////////
const arrow_r_u = new Arrow([0, 0, 0], [0, 0, 1], "red", 0.05, 0.05);
const arrow_r_v = new Arrow([0, 0, 0], [0, 0, 1], "blue", 0.05, 0.05);
scene.add(arrow_r_u);
scene.add(arrow_r_v);
const arrow_e1 = new Arrow([0, 0, 0], [0, 0, 1], "red", 0.05, 0.05);
const arrow_e2 = new Arrow([0, 0, 0], [0, 0, 1], "blue", 0.05, 0.05);
arrow_e1.line.material = new THREE.LineDashedMaterial({
  color: "red",
  dashSize: 0.1,  // Длина самого штриха
  gapSize: 0.1,   // Длина пропуска между штрихами
  scale: 1        // Масштаб пунктира
});
arrow_e1.line.computeLineDistances();
arrow_e2.line.material = new THREE.LineDashedMaterial({
  color: "blue",
  dashSize: 0.1,  // Длина самого штриха
  gapSize: 0.1,   // Длина пропуска между штрихами
  scale: 1        // Масштаб пунктира
});
arrow_e2.line.computeLineDistances();
scene.add(arrow_e1);
scene.add(arrow_e2);

const arrow_Ox = new Arrow([0, 0, 0], [10, 0, 0], "red", 0.05, 0.05);
const arrow_Oy = new Arrow([0, 0, 0], [0, 10, 0], "green", 0.05, 0.05);
const arrow_Oz = new Arrow([0, 0, 0], [0, 0, 10], "blue", 0.05, 0.05);
scene.add(arrow_Ox, arrow_Oy, arrow_Oz);
////////////////

// Создаем материал линии
// TODO: толщина линии, пунктир
const lineMaterial = new THREE.LineBasicMaterial({ color: 0xff0000 });
const lineDotsMaterial = new THREE.PointsMaterial({
  color: 0xff0000,
  size: 0.03,           // Размер точек в единицах мира
  sizeAttenuation: true // Уменьшать ли точки по мере удаления от камеры
});


// Создаем геометрию линии из массива точек
const geodesicLines = new Array(numOfGeodesicLines);
const lineGeometries = new Array(numOfGeodesicLines);
for (let i = 0; i < numOfGeodesicLines; i++) {
  lineGeometries[i] = new THREE.BufferGeometry();
  //geodesicLines[i] = new THREE.Line(lineGeometries[i], lineMaterial);
  geodesicLines[i] = new THREE.Points(lineGeometries[i], lineDotsMaterial);
  scene.add(geodesicLines[i]);
}

// Точки для геодезической
const geodesicPoints = [];
let geodesicPointsCount = 100;
let geodesicPositionBuffers = [];

function initGeodesicArrays() {
  geodesicPoints.length = geodesicPointsCount;

  // Для каждой геодезической линии заранее создаем типизированный массив под числа X,Y,Z
  geodesicPositionBuffers = [];
  for (let i = 0; i < numOfGeodesicLines; i++) {
    // Выделяем память: по 3 числа (X,Y,Z) на каждую точку
    const floatArray = new Float32Array(geodesicPointsCount * 3);
    geodesicPositionBuffers.push(floatArray);

    // Привязываем этот массив к геометрии один раз
    lineGeometries[i].setAttribute('position', new THREE.BufferAttribute(floatArray, 3));
  }
}

const k1Geo = new Float64Array(4);
const k2Geo = new Float64Array(4);
const k3Geo = new Float64Array(4);
const k4Geo = new Float64Array(4);

// Функция для расчёта геодезических на поверхности
function calculateGeodesics(w, h) {
  let vec_view = camera.e2;
  let vec_e1 = camera.e1;
  let vec_ru = camera.r_u;
  let vec_rv = camera.r_v;
  let u = camera.u;
  let v = camera.v;
  let view_norm = vec_view.norm();
  let i = 0;

  let angle = -(numOfGeodesicLines - 1) / 2 * dAngleGeodesics;
  for (let k = 0; k < numOfGeodesicLines; k++) { // Столбец
    // Растягиваем пропорционально углу отставания от вектора взгляда (в касательной плоскости)
    // UPD: НЕ растягиваем
    let diff_vec = vec_e1.mul(view_norm * Math.tan(angle));
    let tmp_vec_view = vec_view.add(diff_vec).normalize();

    let tmp_vec_view_decomp = vectors.decomposition(tmp_vec_view, vec_ru, vec_rv);
    let currentRayState = [u, v, tmp_vec_view_decomp[0], tmp_vec_view_decomp[1]];

    // Берем заранее выделенный плоский массив для этой линии
    const positions = geodesicPositionBuffers[k];

    let j = 0;
    let nextDist = camera.getDistToIntersectionPoint(i, j);
    let curDist = 0;
    let numOfSteps = 0;

    let tempDT = dT;
    while (numOfSteps < maxNumOfSteps) {
      calculations.rk4StepInPlace(currentRayState, tempDT, surface, k1Geo, k2Geo, k3Geo, k4Geo);
      curDist += tempDT;

      if (curDist >= nextDist) {
        let coords = surface.transform(currentRayState[0], currentRayState[1]);
        let stride = j * 3;
        positions[stride] = coords[0]; // X
        positions[stride + 1] = coords[1]; // Y
        positions[stride + 2] = coords[2]; // Z
        j++;
        if (j == h) {
          //tempDT *= 1.2; // Эвристика, мб можно более эффективно
          break;
        }

        nextDist = camera.getDistToIntersectionPoint(i, j);
      }

      // Тут же можно проверять пересечение луча со стенами/объектами
      numOfSteps++;
    }

    // Сообщаем Three.js, что данные в буфере изменились, и их надо отправить на GPU.
    lineGeometries[k].attributes.position.needsUpdate = true;
    i += w / numOfGeodesicLines;
    angle += dAngleGeodesics;
  }
}

// Рендеринг вида из камеры
function renderCameraViewOld(w, h) {
  let angle = -(canvas.width - 1) / 2 * dAngle;
  let vec_view = camera.e2;
  let vec_e1 = camera.e1;
  let vec_ru = camera.r_u;
  let vec_rv = camera.r_v;
  let u = camera.u;
  let v = camera.v;
  let view_norm = vec_view.norm();

  let diff_vec = vec_e1.mul(view_norm * Math.tan(angle));
  let tmp_vec_view = vec_view.add(diff_vec);
  let tmp_vec_view_decomp = vectors.decomposition(tmp_vec_view, vec_ru, vec_rv);
  let currentRayState = [u, v, tmp_vec_view_decomp[0], tmp_vec_view_decomp[1]];
  let i = 0;
  let x = 0;
  let y = 0;

  for (x = 0; x < w; x++) {
    // Растягиваем пропорционально углу отставания от вектора взгляда (в касательной плоскости)
    diff_vec = vec_e1.mul(view_norm * Math.tan(angle));
    tmp_vec_view = vec_view.add(diff_vec);

    tmp_vec_view_decomp = vectors.decomposition(tmp_vec_view, vec_ru, vec_rv);
    currentRayState = [u, v, tmp_vec_view_decomp[0], tmp_vec_view_decomp[1]];

    for (y = 0; y < h; y++) {
      calculations.rk4StepInPlace(currentRayState, dT, surface); // dT, кажется, нужно как-то пропорционально увеличивать с y

      // Индекс первого цветового канала пикселя
      i = ((canvas.height - y) * w + x) * 4;

      let normalizeCoordinates = surface.normalizeCoordinates(currentRayState[0], currentRayState[1]);
      let color = texture_loader.getPixelColor(normalizeCoordinates.uNorm, normalizeCoordinates.vNorm);

      image.data[i] = color.r;
      image.data[i + 1] = color.g;
      image.data[i + 2] = color.b;
      image.data[i + 3] = 255; // прозрачность

      // TODO: проверять пересечение луча со стенами/объектами
    }

    angle += dAngle;
  }
}

const k1Old = new Float64Array(4);
const k2Old = new Float64Array(4);
const k3Old = new Float64Array(4);
const k4Old = new Float64Array(4);

function renderCameraViewOld1(w, h) {
  let angle = -(canvas.width - 1) / 2 * dAngle;
  let vec_view = camera.e2;
  let vec_e1 = camera.e1;
  let vec_ru = camera.r_u;
  let vec_rv = camera.r_v;
  let u = camera.u;
  let v = camera.v;
  let view_norm = vec_view.norm();

  let diff_vec = vec_e1.mul(view_norm * Math.tan(angle));
  let tmp_vec_view = vec_view.add(diff_vec);
  let tmp_vec_view_decomp = vectors.decomposition(tmp_vec_view, vec_ru, vec_rv);
  let currentRayState = [u, v, tmp_vec_view_decomp[0], tmp_vec_view_decomp[1]];
  let i = 0;
  let x = 0;
  let y = 0;

  for (x = 0; x < w; x++) {
    for (y = 0; y < h; y++) {
      // Вектор в касательной плоскости до точки пересечения луча из камеры, проходящего через пиксель (x, y)
      let vecToCrossingPoint = camera.getIntersectionPoint(x, y);
      tmp_vec_view_decomp = vectors.decomposition(vecToCrossingPoint, vec_ru, vec_rv);
      currentRayState = [u, v, tmp_vec_view_decomp[0], tmp_vec_view_decomp[1]];
      calculations.rk4StepInPlace(currentRayState, 1, surface, k1Old, k2Old, k3Old, k4Old);

      // Индекс первого цветового канала пикселя
      i = ((canvas.height - y) * w + x) * 4;

      let normalizeCoordinates = surface.normalizeCoordinates(currentRayState[0], currentRayState[1]);
      let color = texture_loader.getPixelColor(normalizeCoordinates.uNorm, normalizeCoordinates.vNorm);

      image.data[i] = color.r;
      image.data[i + 1] = color.g;
      image.data[i + 2] = color.b;
      image.data[i + 3] = 255; // прозрачность

      // TODO: проверять пересечение луча со стенами/объектами
    }
  }
}

const k1 = new Float64Array(4);
const k2 = new Float64Array(4);
const k3 = new Float64Array(4);
const k4 = new Float64Array(4);
const cameraRayState = new Float64Array(4);

let renderMode = 1;

// Для плоскости тут рендериг некорректный - искажается перспектива (в отличии от Old1), нужно понять, как корректно делать отрисовку.
function renderCameraView(w, h) {
  let angle = -(canvas.width - 1) / 2 * dAngle;
  let vec_view = camera.e2;
  let vec_e1 = camera.e1;
  let vec_ru = camera.r_u;
  let vec_rv = camera.r_v;

  let tmp_vec_view = vec_view
  let tmp_vec_view_decomp = vectors.decomposition(tmp_vec_view, vec_ru, vec_rv);
  let stride = 0;
  let j = 0;

  for (let x = 0; x < w; x++) {
    tmp_vec_view = vec_view.mul(Math.cos(angle)).add(vec_e1.mul(Math.sin(angle)));
    tmp_vec_view_decomp = vectors.decomposition(tmp_vec_view, vec_ru, vec_rv);

    cameraRayState[0] = camera.u;
    cameraRayState[1] = camera.v;
    cameraRayState[2] = tmp_vec_view_decomp[0];
    cameraRayState[3] = tmp_vec_view_decomp[1];

    j = 0;
    let nextDist = camera.getDistToIntersectionPoint(x, j);
    let curDist = 0;
    let numOfSteps = 0;

    let tempDT = dT;
    while (j < h && numOfSteps < maxNumOfSteps) {
      numOfSteps++;
      if (renderMode == 1 && nextDist - curDist < tempDT) {
        tempDT = nextDist - curDist;
      }
      //tempDT = min(tempDT, nextDist - curDist);
      calculations.rk4StepInPlace(cameraRayState, tempDT, surface, k1, k2, k3, k4);

      curDist += tempDT;

      if (curDist >= nextDist) {
        // Индекс первого цветового канала пикселя
        // TODO: мб неправильно и всё перевёрнуто/отражено
        stride = ((canvas.height - j) * w + x) * 4;

        let normalizeCoordinates = surface.normalizeCoordinates(cameraRayState[0], cameraRayState[1]);
        let color = texture_loader.getPixelColor(normalizeCoordinates.uNorm, normalizeCoordinates.vNorm);

        image.data[stride] = color.r;
        image.data[stride + 1] = color.g;
        image.data[stride + 2] = color.b;
        image.data[stride + 3] = 255; // прозрачность

        j++;
        nextDist = camera.getDistToIntersectionPoint(x, j);
        if (renderMode == 1) {
          tempDT = Math.sqrt(nextDist - curDist); // Подсмотрел
        }
      }
    }

    angle += dAngle;
    // TODO: проверять пересечение луча со стенами/объектами
  }
}

// DEBUG
function renderSurfaceTexture(w, h) {
  let u = 0;
  let v = 0;
  for (let x = 0; x < w; x++) {
    v = 0;
    for (let y = 0; y < h; y++) {
      // Индекс первого цветового канала пикселя
      let i = (y * w + x) * 4;

      let normalizeCoordinates = surface.normalizeCoordinates(u, v);
      let color = texture_loader.getPixelColor(normalizeCoordinates.uNorm, normalizeCoordinates.vNorm);

      image.data[i] = color.r;
      image.data[i + 1] = color.g;
      image.data[i + 2] = color.b;
      image.data[i + 3] = 255; // прозрачность

      v += Math.PI / h;
    }
    u += 2 * Math.PI / w;
  }
}

// --- 2. НАСТРОЙКА ПРАВОГО ОКНА (2D Canvas) ---
/** @type {HTMLCanvasElement} */
const canvas = document.getElementById('raycastCanvas');
const ctx = canvas.getContext('2d');
// Создаём пустое изображение
let image = ctx.createImageData(canvas.width, canvas.height);

// Подгоняем размер 2D-холста под размер его окна
canvas.width = RENDER_W;
canvas.height = RENDER_H;
image = ctx.createImageData(canvas.width, canvas.height);
screen.setSizes(screenWidth, screenHeight, canvas.width, canvas.height);

// --- 3. ИНТЕРАКТИВНОСТЬ ---
// При движении мыши над левым окном мы обновляем глобальные координаты
leftContainer.addEventListener('mousemove', (event) => {
  // Нормализуем координаты мыши от 0 до 1
  //mouseX = event.clientX / (window.innerWidth / 2);
  //mouseY = event.clientY / window.innerHeight;
});

// Пересчитываем размеры окон, если пользователь изменил размер браузера
window.addEventListener('resize', () => {
  threeCamera.aspect = (window.innerWidth / 2) / window.innerHeight;
  threeCamera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth / 2, window.innerHeight);
  //resizeCanvas();
  renderY = canvas.height / 2;
  //geodesicPointsCount = Math.floor(canvas.height / 2);
  //initGeodesicArrays();
  //calculateGeodesics();
});

let renderY = canvas.height / 2;

// Обработка нажатия на клавишу
window.addEventListener('keydown', (event) => {
  switch (event.key) {
    case 'ArrowLeft':
      camera.turnLeft();
      calculateGeodesics(canvas.width, renderY);
      //renderCameraView(canvas.width, renderY);
      //moveLeft();
      break;

    case 'ArrowRight':
      camera.turnRight();
      calculateGeodesics(canvas.width, renderY);
      //renderCameraView(canvas.width, renderY);
      //moveRight();
      break;

    case 'ArrowUp':
      camera.moveForward();
      calculateGeodesics(canvas.width, renderY);
      //renderCameraView(canvas.width, renderY);
      //moveRight();
      break;

    case 'ArrowDown':
      camera.moveBackward();
      calculateGeodesics(canvas.width, renderY);
      //renderCameraView(canvas.width, renderY);
      //moveRight();
      break;

    case 'e':
      fov_angle += dAngleWidening;
      dAngleGeodesics = fov_angle / numOfGeodesicLines;
      dAngle = fov_angle / canvas.width;
      calculateGeodesics(canvas.width, renderY);
      //renderCameraView(canvas.width, renderY);
      break;

    case 'q':
      fov_angle -= dAngleWidening;
      dAngleGeodesics = fov_angle / numOfGeodesicLines;
      dAngle = fov_angle / canvas.width;
      calculateGeodesics(canvas.width, renderY);
      //renderCameraView(canvas.width, renderY);
      break;

    case 'w':
      camera.z += dZ;
      //dT = Math.abs(camera.z / 10); // Эвристика мб некорерктно
      calculateGeodesics(canvas.width, renderY);
      //renderCameraView(canvas.width, renderY);
      break;

    case 's':
      camera.z -= dZ;
      //dT = Math.abs(camera.z / 10);
      calculateGeodesics(canvas.width, renderY);
      //renderCameraView(canvas.width, renderY);
      break;

    case 'z':
      camera.distToScreen -= dDistToScreen;
      calculateGeodesics(canvas.width, renderY);
      break;

    case 'x':
      camera.distToScreen += dDistToScreen;
      calculateGeodesics(canvas.width, renderY);
      break;

    case 't':
      renderCameraView(canvas.width, renderY);
      break;

    case 'y':
      renderCameraViewOld1(canvas.width, renderY);
      break;

    case '1':
      renderMode = 1;
      break;

    case '2':
      renderMode = 2;
      break;

    default:
      // Игнорируем все остальные клавиши
      return;
  }

  posDiv.textContent = "cam.z = " + Number(camera.z).toFixed(3) + " distToScr = " + Number(camera.distToScreen).toFixed(3);
  posDiv1.textContent = "(u, v) = " + Number(camera.u).toFixed(3) + ", " + Number(camera.v).toFixed(3);
  posDiv2.textContent = "(x, y, z) = " + Number(camera.pos[0]).toFixed(3) + ", " + Number(camera.pos[1]).toFixed(3) + ", " + Number(camera.pos[2]).toFixed(3);

  // Отменяем стандартное поведение браузера (например, прокрутку страницы стрелками)
  event.preventDefault();
});

geodesicPointsCount = canvas.height / 2;
initGeodesicArrays(); // Начальная инициализация геодезических линий на 3д картинке
calculateGeodesics(canvas.width, canvas.height / 2); // начальный расчёт геодезических

// --- 4. ЕДИНЫЙ ИГРОВОЙ ЦИКЛ (Отрисовка) ---
function animate() {
  // Запрашиваем следующий кадр анимации (60 FPS)
  // TODO: разобраться, что это и зачем
  requestAnimationFrame(animate);

  stats.begin(); // <--- Начало замера

  // Обновляем контроллер каждый кадр, чтобы работала инерция (damping)
  controls.update();

  // --- Обновляем левое окно (Three.js) ---
  renderer.render(scene, threeCamera);

  arrow_r_u.quiver(camera.pos, camera.r_u);
  arrow_r_v.quiver(camera.pos, camera.r_v);
  arrow_e1.quiver(camera.pos, camera.e1);
  arrow_e2.quiver(camera.pos, camera.e2);
  // Свдигание камеры на поверхности
  playerMesh.position.set(camera.pos[0], camera.pos[1], camera.pos[2]);

  /////////////////////////////
  /////////////////////////////
  /////////////////////////////

  // --- Обновляем правое окно (2D Canvas Градиент) ---
  // Очищаем холст
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  renderCameraView(canvas.width, canvas.height / 2); // Оказывается, быстрее рисуется, если рисовать здесь, а не при движении

  // TODO: выводить текстуру, чтобы было видно, где находимся в плоскости (u, v)
  //renderSurfaceTexture(canvas.width, canvas.height);

  // Вывод вида из камеры
  ctx.putImageData(image, 0, 0);

  stats.end(); // <--- Конец замера
}

// Запуск цикла отрисовки
animate();

/*
  ctx.beginPath();
  let normal = surface.normalizeCoordinates(camera.u, camera.v);
  let x = Math.floor(normal.uNorm * canvas.width);
  let y = Math.floor(normal.vNorm * canvas.height);
  //let pixelCoords = texture_loader.getPixelCoordinates(normal.uNorm, normal.vNorm);
  //console.log(pixelCoords);

  ctx.arc(x, y, 50, 0, 2 * Math.PI); // Center at (100,100), radius 50
  ctx.fillStyle = '#3498db';              // Blue fill
  ctx.fill();                            // Draw the solid circle

*/