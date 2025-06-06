let canvasWidth = 400;
let canvasHeight = 400;

// Координаты левого нижнего и правого верхнего углов относительно начала координат
let canvasLeft = -50;
let canvasRight = +50;
let canvasBottom = -50;
let canvasTop = +50;
// Длина в векторном пространтсве
let canvasLenX = canvasRight - canvasLeft;
let canvasLenY = canvasTop - canvasBottom;
// Величины, на которые изменяется положение графика
let dCanvasHorizontal = 1.01; // По горизонтали
let dCanvasVertical = 1.01; // По вертикали
// Величины, на которые происходит растяжение графика
let dCanvasZoomHorizontal = 1;

// Преобразуем математические координаты в координаты холста (X)
function toCanvasX(x) {
  return ((x - canvasLeft) / (canvasRight - canvasLeft)) * canvasWidth
}

// Преобразуем математические координаты в координаты холста (Y)
function toCanvasY(y) {
  return canvasHeight - ((y - canvasBottom) / (canvasTop - canvasBottom)) * canvasHeight
}

function setup() {
  createCanvas(canvasWidth, canvasHeight);
  angleMode(DEGREES);
  describe(
    'Графики'
  );
  background(0);

  stroke('white');
  fill('white');
  circle(toCanvasX(0), toCanvasY(0), 5);

  line(toCanvasX(canvasLeft), toCanvasY(0), toCanvasX(canvasRight), toCanvasY(0));
  line(toCanvasX(0), toCanvasY(canvasBottom), toCanvasX(0), toCanvasY(canvasTop));

  //strokeWeight(0);
}

function draw() {
  background(0);

  drawCoordinateAxes();
  drawCoordinateDots();
  drawFigures();
  drawCoordinateCaptions();

  processKeys();
}

function drawCoordinateAxes() {
  stroke('white');
  fill('white');
  strokeWeight(2);

  circle(toCanvasX(0), toCanvasY(0), 5);

  line(toCanvasX(canvasLeft), toCanvasY(0), toCanvasX(canvasRight), toCanvasY(0));
  line(toCanvasX(0), toCanvasY(canvasBottom), toCanvasX(0), toCanvasY(canvasTop));
}

function divme(a, b){
    return (a - a%b)/b
}

function drawCoordinateDots() {
  stroke('white');
  fill('white');

  strokeWeight(1);
  for (let x = Math.ceil(canvasLeft/10)*10; x <= Math.floor(canvasRight/10)*10; x += 10) {
    stroke('grey');
    if (x === 0) {
      continue;
    }
    line(toCanvasX(x), toCanvasY(canvasBottom), toCanvasX(x), toCanvasY(canvasTop));
    stroke('white');
    circle(toCanvasX(x), toCanvasY(0), 3);
  }

  for (let y = Math.ceil(canvasBottom/10)*10; y <= Math.floor(canvasTop/10)*10; y += 10) {
    stroke('grey');
    if (y === 0) {
      continue;
    }
    line(toCanvasX(canvasLeft), toCanvasY(y), toCanvasX(canvasRight), toCanvasY(y));
    stroke('white');
    circle(toCanvasX(0), toCanvasY(y), 3);
  }
}

function drawCoordinateCaptions() {
  stroke('white');
  fill('white');

  strokeWeight(1);
  for (let x = Math.ceil(canvasLeft/10)*10 - 10; x <= Math.floor(canvasRight/10)*10 + 10; x += 10) {
    text(x, toCanvasX(x), toCanvasY(0));
  }

  for (let y = Math.ceil(canvasBottom/10)*10 - 10; y <= Math.floor(canvasTop/10)*10 + 10; y += 10) {
    text(y, toCanvasX(0), toCanvasY(y));
  }
}

function drawFigures() {
  drawLine();
  drawParametrizedCurve();
  drawPointOnCurve();
}

function drawLine() {
  stroke('red');
  strokeWeight(2);
  line(toCanvasX(-10), toCanvasY(-10), toCanvasX(30), toCanvasY(-5));
}

/*
Кривая
*/

let tCount = 100; // число точек
let curveFromT = -3; // начало отрезка
let curveToT = 3; // конец отрезка

// Выражение для компонента X кривой
function curveX(t) {
  return Math.pow(t, 3);
}

// Выражение для компонента Y кривой
function curveY(t) {
  return Math.pow(t, 2);
}

function drawParametrizedCurve() {
  noFill();
  strokeWeight(2);
  stroke('green');
  beginShape();
  let dt = (curveToT - curveFromT) / tCount

  for (let t = curveFromT; t <= curveToT; t += dt) {
    vertex(toCanvasX(curveX(t)), toCanvasY(curveY(t)));
  }
  vertex(toCanvasX(curveX(curveToT)), toCanvasY(curveY(curveToT))); // Иногда не дорисовывает

  endShape();
}

let t0 = curveToT;
let dt0 = 0.1;

function drawPointOnCurve() {
  noFill();
  stroke('green');
  fill('violet');
  circle(toCanvasX(curveX(t0)), toCanvasY(curveY(t0)), 4);
}

function processKeys() {
  // Смещение относительно центра
  if (keyIsDown(UP_ARROW)) {
    console.log('UP_ARROW нажата!');
    canvasBottom += dCanvasVertical;
    canvasTop += dCanvasVertical;
  }
  if (keyIsDown(DOWN_ARROW)) { // Проверка на стрелку вверх
    console.log('DOWN_ARROW нажата!');
    canvasBottom -= dCanvasVertical;
    canvasTop -= dCanvasVertical;
  }
  if (keyIsDown(LEFT_ARROW)) {
    console.log('LEFT_ARROW нажата!');
    canvasLeft -= dCanvasHorizontal;
    canvasRight -= dCanvasHorizontal;
  }
  if (keyIsDown(RIGHT_ARROW)) {
    console.log('RIGHT_ARROW нажата!');
    canvasLeft += dCanvasHorizontal;
    canvasRight += dCanvasHorizontal;
  }
  // ZOOM (неправильно, нужно, чтобы оно было относительно центра окна)
  if (keyIsDown(65)) {
    console.log('A нажата!');
    canvasLeft *= dCanvasHorizontal;
    canvasRight *= dCanvasHorizontal;
  }
  if (keyIsDown(68)) {
    console.log('D нажата!');
    canvasLeft /= dCanvasHorizontal;
    canvasRight /= dCanvasHorizontal;
  }
  if (keyIsDown(87)) {
    console.log('W нажата!');
    canvasBottom *= dCanvasVertical;
    canvasTop *= dCanvasVertical;
  }
  if (keyIsDown(83)) {
    console.log('S нажата!');
    canvasBottom /= dCanvasVertical;
    canvasTop /= dCanvasVertical;
  }

  // Точка на кривой
  if (keyIsDown(81)) {
    console.log('Q нажата!');
    t0 -= dt0;
    if (t0 < curveFromT) {
      t0 = curveFromT;
    }
  }
  if (keyIsDown(69)) {
    console.log('E нажата!');
    t0 += dt0;
    if (t0 > curveToT) {
      t0 = curveToT;
    }
  }

  // reset
  if (keyIsDown(82)) {

  }
}

