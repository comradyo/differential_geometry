import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// --- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ДЛЯ СВЯЗИ ОКОН ---
let mouseX = 0;
let mouseY = 0;

// --- 1. НАСТРОЙКА ЛЕВОГО ОКНА (Three.js) ---
const leftContainer = document.getElementById('left-window');

// Создаем сцену, камеру и рендерер
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, (window.innerWidth / 2) / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

// Задаем размер рендерера ровно под левое окно
renderer.setSize(window.innerWidth / 2, window.innerHeight);
leftContainer.appendChild(renderer.domElement);

// Создаем контроллер орбиты, передаем камеру и элемент, который будет слушать мышь
const controls = new OrbitControls(camera, renderer.domElement);
// По желанию настраиваем плавность (инерцию) вращения
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Добавляем тестовый 3D-куб
/*
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);
*/

// 1. Создаем каркас сферы (радиус, сегменты по u, сегменты по v)
const sphereGeometry = new THREE.SphereGeometry(1, 64, 64);

// 2. Создаем материал
// Вариант А: Обычная сетка (как plot_wireframe)
// const wireMaterial = new THREE.MeshBasicMaterial({ color: 0x4444ff, wireframe: true });
// Вариант Б: Сплошная поверхность с текстурой (как plot_surface)
const textureLoader = new THREE.TextureLoader();
const earthTexture = textureLoader.load('src/earth.jpg'); // пример текстуры из доков Three.js
const surfaceMaterial = new THREE.MeshBasicMaterial({ map: earthTexture });

// 3. Объединяем геометрию и материал в один объект и добавляем на сцену
const sphereMesh = new THREE.Mesh(sphereGeometry, surfaceMaterial);
scene.add(sphereMesh);

// Точки
const points = [];
const pointsCount = 100;
// В цикле рассчитываете ваши 3D координаты (X, Y, Z) геодезической линии:
for (let i = 0; i < pointsCount; i++) {
    let x = i;
    let y = Math.sin(i);
    let z = Math.cos(i);
    // Вычисляете x, y, z на основе ваших u и v из решения уравнения геодезической
    points.push(new THREE.Vector3(x, y, z));
}

// Создаем геометрию линии из массива точек
const lineGeometry = new THREE.BufferGeometry().setFromPoints(points);

// Создаем материал линии (толщина линии в WebGL на большинстве карт всегда 1 пиксель)
const lineMaterial = new THREE.LineBasicMaterial({ color: 0xff0000 });

// Объединяем и добавляем
const geodesicLine = new THREE.Line(lineGeometry, lineMaterial);
scene.add(geodesicLine);


camera.position.z = 3;

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

// --- 3. ИНТЕРАКТИВНОСТЬ (Слежка за мышью) ---
// При движении мыши над левым окном мы обновляем глобальные координаты
leftContainer.addEventListener('mousemove', (event) => {
    // Нормализуем координаты мыши от 0 до 1
    mouseX = event.clientX / (window.innerWidth / 2);
    mouseY = event.clientY / window.innerHeight;
});

// Пересчитываем размеры окон, если пользователь изменил размер браузера
window.addEventListener('resize', () => {
    camera.aspect = (window.innerWidth / 2) / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth / 2, window.innerHeight);
    resizeCanvas();
});


// --- 4. ЕДИНЫЙ ИГРОВОЙ ЦИКЛ (Отрисовка) ---
function animate() {
    // Запрашиваем следующий кадр анимации (60 FPS)
    requestAnimationFrame(animate);

    // Обновляем контроллер каждый кадр, чтобы работала инерция (damping)
    controls.update(); 

    // --- Обновляем левое окно (Three.js) ---
    renderer.render(scene, camera);

    // --- Обновляем правое окно (2D Canvas Градиент) ---
    // Очищаем холст
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Создаем радиальный градиент, который "следит" за курсором из левого окна
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
}

// Запускаем наш цикл
animate();
