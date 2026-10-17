//import { createWorld } from "./world.js";
//import { initScene3D } from "./scene3d.js";
import { initRaycaster } from "./raycaster.js";

//const world = createWorld();
//const scene3D = initScene3D(world);
//const raycaster = initRaycaster(world);

const raycaster = initRaycaster();

// Позже здесь добавить управление камерой и синхронизацию двух панелей.

// Когда понадобится обновить изображение:
raycaster.render();
