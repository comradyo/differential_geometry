import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import * as surfaces from './surface.js';
import { Vec, Arrow } from './vector.js';
import * as vectors from './vector.js';
import * as calculations from './calculations.js'

// --- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ДЛЯ СВЯЗИ ОКОН ---
let mouseX = 0;
let mouseY = 0;

const surface = new surfaces.Sphere();

// Угол поворота
let alpha = 0.0;
const dAlpha = 0.05;
let dot_coords = surface.transform(0, 0);

// --- 1. НАСТРОЙКА ЛЕВОГО ОКНА (Three.js) ---
const leftContainer = document.getElementById('left-window');

// Создаем сцену, камеру и рендерер
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, (window.innerWidth / 2) / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

camera.position.z = 3;

// Задаем размер рендерера ровно под левое окно
renderer.setSize(window.innerWidth / 2, window.innerHeight);
leftContainer.appendChild(renderer.domElement);

// Создаем контроллер орбиты, передаем камеру и элемент, который будет слушать мышь
const controls = new OrbitControls(camera, renderer.domElement);
// По желанию настраиваем плавность (инерцию) вращения
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// 1. Создаем каркас сферы (радиус, сегменты по u, сегменты по v)
const sphereGeometry = new THREE.SphereGeometry(1, 64, 64);

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
// Объединяем и добавляем
const geodesicLine = new THREE.Line(lineGeometry, lineMaterial);
scene.add(geodesicLine);

// Точки для геодезической
const geodesicPoints = [];
const geodesicPointsCount = 100;
geodesicPoints.length = geodesicPointsCount;

function calculateGeodesic(u, v, vec_ru, vec_rv, vec_view, surface) {
  let vec_view_decomp = vectors.decomposition(vec_view, vec_ru, vec_rv);
  let currentRayState = [u, v, vec_view_decomp[0], vec_view_decomp[1]];
  // TODO: мб делать не число шагов, а длину?
  for (let i = 0; i < geodesicPointsCount; i++) {
    currentRayState = calculations.rk4Step(currentRayState, 0.05, surface);
    let coords = surface.transform(currentRayState[0], currentRayState[1]);
    geodesicPoints[i] =  new THREE.Vector3(coords[0], coords[1], coords[2]);

    // Тут же можно проверять пересечение луча со стенами/объектами
  }

  lineGeometry.setFromPoints(geodesicPoints);
}

// --- 2. НАСТРОЙКА ПРАВОГО ОКНА (2D Canvas) ---
/** @type {HTMLCanvasElement} */
const canvas = document.getElementById('raycastCanvas');
const ctx = canvas.getContext('2d');

// Подгоняем размер 2D-холста под размер его окна
function resizeCanvas() {
  canvas.width = window.innerWidth / 2;
  canvas.height = window.innerHeight;
}
resizeCanvas();

// --- 3. ИНТЕРАКТИВНОСТЬ ---
// При движении мыши над левым окном мы обновляем глобальные координаты
leftContainer.addEventListener('mousemove', (event) => {
  // Нормализуем координаты мыши от 0 до 1
  mouseX = event.clientX / (window.innerWidth / 2);
  mouseY = event.clientY / window.innerHeight;
  
  let u = mouseX;
  let v = mouseY;
  let r_u = surface.r_u(u, v);
  let r_v = surface.r_v(u, v);

  // TODO: не дублировать код, считать в одном месте

  // Ортонормируем канонический базис
  let ru_norm = r_u.normalize();
  let rv_norm = r_v.sub(vectors.projection(r_v, ru_norm));
  rv_norm = rv_norm.div(rv_norm.norm());

  // Строем ортонормированный базис относительно направления взгляда
  // Направление взгляда совпадает с вектором e2
  let e1 = ru_norm.mul(+Math.cos(alpha)).add(rv_norm.mul(+Math.sin(alpha)));
  let e2 = ru_norm.mul(-Math.sin(alpha)).add(rv_norm.mul(+Math.cos(alpha)));

  calculateGeodesic(u, v, r_u, r_v, e2, surface);
});

// Пересчитываем размеры окон, если пользователь изменил размер браузера
window.addEventListener('resize', () => {
  camera.aspect = (window.innerWidth / 2) / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth / 2, window.innerHeight);
  resizeCanvas();
});

// Обработка нажатия на клавишу
window.addEventListener('keydown', (event) => {
  switch (event.key) {
    case 'ArrowLeft':
      alpha += dAlpha;
      //moveLeft();
      break;

    case 'ArrowRight':
      alpha -= dAlpha;
      //moveRight();
      break;

    default:
      // Игнорируем все остальные клавиши
      return;
  }

  // Отменяем стандартное поведение браузера (например, прокрутку страницы стрелками)
  event.preventDefault();
});

// --- 4. ЕДИНЫЙ ИГРОВОЙ ЦИКЛ (Отрисовка) ---
function animate() {
  // Запрашиваем следующий кадр анимации (60 FPS)
  // TODO: разобраться, что это и зачем
  requestAnimationFrame(animate);

  // Обновляем контроллер каждый кадр, чтобы работала инерция (damping)
  controls.update();

  // --- Обновляем левое окно (Three.js) ---
  renderer.render(scene, camera);

  // TODO: поменять потом на нормальные данные
  let u = mouseX;
  let v = mouseY;

  dot_coords = surface.transform(u, v);

  let r_u = surface.r_u(u, v);
  let r_v = surface.r_v(u, v);

  // Ортонормируем канонический базис
  let ru_norm = r_u.normalize();
  let rv_norm = r_v.sub(vectors.projection(r_v, ru_norm));
  rv_norm = rv_norm.div(rv_norm.norm());

  // Строем ортонормированный базис относительно направления взгляда
  // Направление взгляда совпадает с вектором e2
  let e1 = ru_norm.mul(+Math.cos(alpha)).add(rv_norm.mul(+Math.sin(alpha)));
  let e2 = ru_norm.mul(-Math.sin(alpha)).add(rv_norm.mul(+Math.cos(alpha)));

  arrow_r_u.quiver(dot_coords, r_u);
  arrow_r_v.quiver(dot_coords, r_v);
  arrow_e1.quiver(dot_coords, e1);
  arrow_e2.quiver(dot_coords, e2);
  // Свдигание камеры
  playerMesh.position.set(dot_coords[0], dot_coords[1], dot_coords[2]);

  // Отрисовка геодезической

  /////////////////////////////
  /////////////////////////////
  /////////////////////////////

  // --- Обновляем правое окно (2D Canvas Градиент) ---
  // Очищаем холст
  ctx.clearRect(0, 0, canvas.width, canvas.height);

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

  //print(surface.X(mouseX, mouseY));
}

// Запускаем наш цикл
animate();
