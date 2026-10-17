import * as THREE from './node_modules/three/build/three.module.js';

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

// Добавляем тестовый 3D-куб
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

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

    // --- Обновляем левое окно (Three.js) ---
    // Куб вращается со скоростью, зависящей от положения мыши
    cube.rotation.x += 0.01 + mouseY * 0.05;
    cube.rotation.y += 0.01 + mouseX * 0.05;
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
