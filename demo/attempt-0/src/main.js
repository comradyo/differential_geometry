import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import * as surfaces from './surface.js';
import { Vec, Arrow } from './vector.js';
import * as vectors from './vector.js';
import * as calculations from './calculations.js'
import * as cameras from './camera.js'

// --- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ДЛЯ СВЯЗИ ОКОН ---
let mouseX = 0;
let mouseY = 0;

// Угол обзора камеры на поверхности
let fov_angle_degrees = 60.0;
let fov_angle = Math.PI * fov_angle_degrees / 180.0;
// Число геодезических, которые будут отрисовываны на 3D изображении
const numOfGeodesicLines = 9;
let delta_fov_angle = fov_angle / numOfGeodesicLines;

const surface = new surfaces.Sphere();
//const surface = new surfaces.Plane();
const camera = new cameras.Camera(fov_angle, surface);
camera.setCoords(0, 0.1);

// --- 1. НАСТРОЙКА ЛЕВОГО ОКНА (Three.js) ---
const leftContainer = document.getElementById('left-window');

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

// 1. Создаем каркас сферы (радиус, сегменты по u, сегменты по v)
const sphereGeometry = new THREE.SphereGeometry(1, 64, 64);
sphereGeometry.rotateX(Math.PI / 2); // Нужно для того, чтобы полюса были на оси z.

// 2. Создаем материал
// Вариант А: Обычная сетка (как plot_wireframe)
// const wireMaterial = new THREE.MeshBasicMaterial({ color: 0x4444ff, wireframe: true });
// Вариант Б: Сплошная поверхность с текстурой (как plot_surface)
// TODO: почему-то в 3д Ox расположена справа, Oy - слева, Oz - смотрит на камеру.
// При этом, полюса накладывается на ось Z. А, ну в движках часто z - это глубина, но тут нужно будет поправить. 
const textureLoader = new THREE.TextureLoader();
const earthTexture = textureLoader.load('src/earth.jpg'); // пример текстуры из доков Three.js
const surfaceMaterial = new THREE.MeshBasicMaterial({ map: earthTexture });

// 3. Объединяем геометрию и материал в один объект и добавляем на сцену
const sphereMesh = new THREE.Mesh(sphereGeometry, surfaceMaterial);
scene.add(sphereMesh);

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

// Создаем геометрию линии из массива точек
const lineGeometry = new THREE.BufferGeometry();
// Создаем материал линии (толщина линии в WebGL на большинстве карт всегда 1 пиксель)
// TODO: толщина линии, пунктир
const lineMaterial = new THREE.LineBasicMaterial({ color: 0xff0000 });

const geodesicLines = new Array(numOfGeodesicLines);
const lineGeometries = new Array(numOfGeodesicLines);
for (let i = 0; i < numOfGeodesicLines; i++) {
  lineGeometries[i] = new THREE.BufferGeometry();
  geodesicLines[i] = new THREE.Line(lineGeometries[i], lineMaterial);
  scene.add(geodesicLines[i]);
}

// Точки для геодезической
const geodesicPoints = [];
const geodesicPointsCount = 100;
geodesicPoints.length = geodesicPointsCount;

// Для каждой геодезической линии заранее создаем типизированный массив под числа X,Y,Z
const geodesicPositionBuffers = [];
for (let i = 0; i < numOfGeodesicLines; i++) {
  // Выделяем память: по 3 числа (X,Y,Z) на каждую точку
  const floatArray = new Float32Array(geodesicPointsCount * 3);
  geodesicPositionBuffers.push(floatArray);

  // Привязываем этот массив к геометрии один раз
  lineGeometries[i].setAttribute('position', new THREE.BufferAttribute(floatArray, 3));
}

// Функция для расчёта геодезических на поверхности
function calculateGeodesics(camera, surface) {
  let vec_view = camera.e2;
  let vec_e1 = camera.e1;
  let vec_ru = camera.r_u;
  let vec_rv = camera.r_v;
  let u = camera.u;
  let v = camera.v;
  let view_norm = vec_view.norm();

  let angle = -(numOfGeodesicLines - 1) / 2 * delta_fov_angle;
  //let angle = -fov_angle / 2;
  for (let i = 0; i < numOfGeodesicLines; i++) {
    // Растягиваем пропорционально углу отставания от вектора взгляда (в касательной плоскости)
    let diff_vec = vec_e1.mul(view_norm * Math.tan(angle));
    let tmp_vec_view = vec_view.add(diff_vec);

    let tmp_vec_view_decomp = vectors.decomposition(tmp_vec_view, vec_ru, vec_rv);
    let currentRayState = [u, v, tmp_vec_view_decomp[0], tmp_vec_view_decomp[1]];

    // Берем заранее выделенный плоский массив для этой линии
    const positions = geodesicPositionBuffers[i];

    // TODO: мб делать не число шагов, а длину/время t?
    for (let j = 0; j < geodesicPointsCount; j++) {
      calculations.rk4StepInPlace(currentRayState, 0.05, surface);
      let coords = surface.transform(currentRayState[0], currentRayState[1]);

      // Записываем голые числа прямо в массив без создания THREE.Vector3
      let stride = j * 3;
      positions[stride] = coords[0]; // X
      positions[stride + 1] = coords[1]; // Y
      positions[stride + 2] = coords[2]; // Z

      // Тут же можно проверять пересечение луча со стенами/объектами
    }

    // Сообщаем Three.js, что данные в буфере изменились, и их надо отправить на GPU.
    lineGeometries[i].attributes.position.needsUpdate = true;

    angle += delta_fov_angle;
  }

}

const dT = 0.01;

function renderSurface(w, h) {
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
      calculations.rk4StepInPlace(currentRayState, dT, surface);

      // Индекс первого цветового канала пикселя
      i = (y * w + x) * 4;

      image.data[i] = x * 255 / w + camera.pos[0] * 100; // красный
      image.data[i + 1] = 200 * currentRayState[0]; // зелёный
      image.data[i + 2] = 150 * currentRayState[1];         // синий
      image.data[i + 3] = 255;         // прозрачность
      // Тут же можно проверять пересечение луча со стенами/объектами
    }

    angle += delta_fov_angle;
  }
}

// --- 2. НАСТРОЙКА ПРАВОГО ОКНА (2D Canvas) ---
/** @type {HTMLCanvasElement} */
const canvas = document.getElementById('raycastCanvas');
const ctx = canvas.getContext('2d');
// Создаём пустое изображение
let image = ctx.createImageData(canvas.width, canvas.height);

let dAngle = fov_angle / canvas.width;
// Подгоняем размер 2D-холста под размер его окна
function resizeCanvas() {
  canvas.width = window.innerWidth / 2;
  canvas.height = window.innerHeight;
  image = ctx.createImageData(canvas.width, canvas.height);
  dAngle = fov_angle / canvas.width;
}
resizeCanvas();

// --- 3. ИНТЕРАКТИВНОСТЬ ---
// При движении мыши над левым окном мы обновляем глобальные координаты
leftContainer.addEventListener('mousemove', (event) => {
  // Нормализуем координаты мыши от 0 до 1
  mouseX = event.clientX / (window.innerWidth / 2);
  mouseY = event.clientY / window.innerHeight;

  //camera.setCoords(mouseX, mouseY);
  //calculateGeodesics(camera, surface);
});

// Пересчитываем размеры окон, если пользователь изменил размер браузера
window.addEventListener('resize', () => {
  threeCamera.aspect = (window.innerWidth / 2) / window.innerHeight;
  threeCamera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth / 2, window.innerHeight);
  resizeCanvas();
});

// Обработка нажатия на клавишу
window.addEventListener('keydown', (event) => {
  switch (event.key) {
    case 'ArrowLeft':
      camera.turnLeft();
      calculateGeodesics(camera, surface);
      //moveLeft();
      break;

    case 'ArrowRight':
      camera.turnRight();
      calculateGeodesics(camera, surface);
      //moveRight();
      break;

    case 'ArrowUp':
      camera.moveForward();
      calculateGeodesics(camera, surface);
      //moveRight();
      break;

    case 'ArrowDown':
      camera.moveBackward();
      calculateGeodesics(camera, surface);
      //moveRight();
      break;

    default:
      // Игнорируем все остальные клавиши
      return;
  }

  // Отменяем стандартное поведение браузера (например, прокрутку страницы стрелками)
  event.preventDefault();
});

calculateGeodesics(camera, surface); // начальный расчёт геодезических
// --- 4. ЕДИНЫЙ ИГРОВОЙ ЦИКЛ (Отрисовка) ---
function animate() {
  // Запрашиваем следующий кадр анимации (60 FPS)
  // TODO: разобраться, что это и зачем
  requestAnimationFrame(animate);

  // Обновляем контроллер каждый кадр, чтобы работала инерция (damping)
  controls.update();

  // --- Обновляем левое окно (Three.js) ---
  renderer.render(scene, threeCamera);

  arrow_r_u.quiver(camera.pos, camera.r_u);
  arrow_r_v.quiver(camera.pos, camera.r_v);
  arrow_e1.quiver(camera.pos, camera.e1);
  arrow_e2.quiver(camera.pos, camera.e2);
  // Свдигание камеры
  playerMesh.position.set(camera.pos[0], camera.pos[1], camera.pos[2]);

  /////////////////////////////
  /////////////////////////////
  /////////////////////////////

  // --- Обновляем правое окно (2D Canvas Градиент) ---
  // Очищаем холст
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  renderSurface(canvas.width, canvas.height);
  //renderSurface(canvas.width, 100);
  //renderSurfaceOptimized(canvas.width, canvas.height);

  // Выводим вычисленные пиксели на холст
  ctx.putImageData(image, 0, 0);

  /*
  // Переводим нормализованные координаты мыши в пиксели правого холста
  let dotX = mouseX * canvas.width;
  let dotY = mouseY * canvas.height;

  // Цвет динамически меняется от движения
  let r = Math.floor(mouseX * 255);
  let g = Math.floor(mouseY * 255);
  let b = 150;

  // Заливаем холст получившимся градиентом
  ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
  ctx.fillRect(dotX, dotY, 50, 50);
*/
}

// Запускаем наш цикл
animate();
