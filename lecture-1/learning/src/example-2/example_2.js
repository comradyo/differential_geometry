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

function setup() {
  createCanvas(canvasWidth, canvasHeight);
  angleMode(DEGREES);
  describe(
    'Пытаюсь что-то сделать'
  );
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

let dx = 2;
let dy = 1;

function draw() {
  background(0);

  posX += directionX*dx;
  posY += directionY*dy;

  if (posX >= canvasWidth-1 || posX <= 0) {
    directionX *= -1
  }
  if (posY >= canvasHeight-1 || posY <= 0) {
    directionY *= -1
  }

  posX %= canvasWidth
  posY %= canvasWidth

  stroke('white');
  fill('white');
  circle(xToCanvasX(0), xToCanvasX(0), 10);
  
  tracesFrameCounter = (tracesFrameCounter + 1) % tracesFrameCounterStep;
  if (tracesFrameCounter == 0) {
    if (tracesPos.length < numOfTraces) {
      tracesPos.push([posX, posY]);
    } else {
      tracesPos[currentTrace] = { x: posX, y: posY };
    }
    currentTrace = (currentTrace + 1) % numOfTraces
  }

  for (let i = 0; i < numOfTraces; i++) {
    j = (currentTrace + i) % numOfTraces
    positions = tracesPos[j]
    if (positions !== undefined) {
      stroke(200, 100, 255 - i*numOfTraces);
      fill(200, 100, 255 - i*numOfTraces)
      circle(positions.x, positions.y, 10);
    }
  }

  stroke('white');
  fill(200, 100, 255)
  circle(posX, posY, 10);

}
