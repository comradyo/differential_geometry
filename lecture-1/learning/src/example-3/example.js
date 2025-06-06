let canvasWidth = 400;
let canvasHeight = 400;

let canvasLeft = -50;
let canvasRight = +50;
let canvasBottom = -50;
let canvasTop = +50;
let canvasLenX = canvasRight - canvasLeft;
let canvasLenY = canvasTop - canvasBottom;

// Преобразуем математические координаты в координаты холста (X)
/*
  ○-------------○-----○
  cl            x     cr
*/
function xToCanvasX(x) {
  return ((x - canvasLeft) / (canvasRight - canvasLeft)) * canvasWidth
}

// Преобразуем математические координаты в координаты холста (Y)
function yToCanvasY(y) {
  return ((y - canvasBottom) / (canvasTop - canvasBottom)) * canvasHeight
}

var tracesPos = [];
let numOfTraces = 10;
let currentTrace = 0;
let tracesFrameCounter = 0;
let tracesFrameCounterStep = 5;

let directionX = 1;
let directionY = 1;

let posX = 1;
let posY = 3;

let speedCoefficient = 5;
let dx = 1 * speedCoefficient;
let dy = 1 * speedCoefficient;

function setup() {
  createCanvas(canvasWidth, canvasHeight);
  angleMode(DEGREES);
  describe(
    'Пытаюсь что-то сделать'
  );
  background(0);

  stroke('white');
  fill('white');
  circle(xToCanvasX(0), xToCanvasX(0), 10);

  strokeWeight(0);
}

let colorR = 200;
let colorG = 100;
let colorB = 255;
let dColorR = 1;
let dColorG = 2;
let dColorB = 3;
let dColorRMultiplier = 1;
let dColorGMultiplier = 1;
let dColorBMultiplier = 1;
let maxColorValue = 255;

function draw() {
  //background(0);

  posX += directionX*dx;
  posY += directionY*dy;

  if (posX >= canvasWidth-1 || posX <= 0) {
    directionX *= -1
  }
  if (posY >= canvasHeight-1 || posY <= 0) {
    directionY *= -1
  }

  //posX %= canvasWidth
  //posY %= canvasWidth

  //stroke('white');
  fill(colorR, colorG, colorB)
  circle(posX, posY, 10);

  colorR += dColorR * dColorRMultiplier;
  if ((colorR >= maxColorValue) || (colorR < 0)) {
    dColorRMultiplier *= -1;
  }
  colorG += dColorG * dColorGMultiplier;
  if ((colorG >= maxColorValue) || (colorG < 0)) {
    dColorGMultiplier *= -1;
  }
  colorB += dColorB * dColorBMultiplier;
  if ((colorB >= maxColorValue) || (colorB < 0)) {
    dColorBMultiplier *= -1;
  }

  processKeys();
}

function processKeys() {
  if (keyIsDown(UP_ARROW)) {
    dx += 0.05
    console.log('UP_ARROW нажата!');
  }
  if (keyIsDown(DOWN_ARROW)) { // Проверка на стрелку вверх
    dx -= 0.05
    console.log('DOWN_ARROW нажата!');
  }
}

