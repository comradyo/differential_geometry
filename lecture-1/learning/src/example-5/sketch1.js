let backgroundColor = 'white';
let captionsColor = 'black'
let gridColor = 'gray'

function sketch1(p) {
  p.setup = function () {
    p.createCanvas(canvasWidth, canvasHeight);
    p.angleMode(p.DEGREES);
    p.describe(
        'Графики'
    );
    p.background(backgroundColor);

    p.stroke(captionsColor);
    p.fill(captionsColor);
    p.circle(toCanvasX(0), toCanvasY(0), 5);

    p.line(toCanvasX(canvasLeft), toCanvasY(0), toCanvasX(canvasRight), toCanvasY(0));
    p.line(toCanvasX(0), toCanvasY(canvasBottom), toCanvasX(0), toCanvasY(canvasTop));
  };

  p.draw = function () {
    p.background(backgroundColor);

    drawCoordinateAxes(p);
    drawCoordinateDots(p);
    drawFigures(p);
    drawCoordinateCaptions(p);

    processKeys(p);
  };
}

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

function drawCoordinateAxes(p) {
  p.stroke(captionsColor);
  p.fill(captionsColor);
  p.strokeWeight(2);

  p.circle(toCanvasX(0), toCanvasY(0), 5);

  p.line(toCanvasX(canvasLeft), toCanvasY(0), toCanvasX(canvasRight), toCanvasY(0));
  p.line(toCanvasX(0), toCanvasY(canvasBottom), toCanvasX(0), toCanvasY(canvasTop));
}

function drawCoordinateDots(p) {
  p.stroke(captionsColor);
  p.fill(captionsColor);

  p.strokeWeight(1);
  for (let x = Math.ceil(canvasLeft/10)*10; x <= Math.floor(canvasRight/10)*10; x += 10) {
    p.stroke(gridColor);
    if (x === 0) {
      continue;
    }
    p.line(toCanvasX(x), toCanvasY(canvasBottom), toCanvasX(x), toCanvasY(canvasTop));
    p.stroke(captionsColor);
    p.circle(toCanvasX(x), toCanvasY(0), 3);
  }

  for (let y = Math.ceil(canvasBottom/10)*10; y <= Math.floor(canvasTop/10)*10; y += 10) {
    p.stroke(gridColor);
    if (y === 0) {
      continue;
    }
    p.line(toCanvasX(canvasLeft), toCanvasY(y), toCanvasX(canvasRight), toCanvasY(y));
    p.stroke(captionsColor);
    p.circle(toCanvasX(0), toCanvasY(y), 3);
  }
}

function drawCoordinateCaptions(p) {
  p.stroke(captionsColor);
  p.fill(captionsColor);

  p.strokeWeight(1);
  for (let x = Math.ceil(canvasLeft/10)*10 - 10; x <= Math.floor(canvasRight/10)*10 + 10; x += 10) {
    p.text(x, toCanvasX(x), toCanvasY(0));
  }

  for (let y = Math.ceil(canvasBottom/10)*10 - 10; y <= Math.floor(canvasTop/10)*10 + 10; y += 10) {
    p.text(y, toCanvasX(0), toCanvasY(y));
  }
}

function drawFigures(p) {
  drawCurve(p);
  drawVelocity(p);
  drawPointOnCurve(p);
}

/*
Кривая
*/

let tCount = 100; // число точек
let curveFromT = -10; // начало отрезка
let curveToT = 10; // конец отрезка
let dt = (curveToT - curveFromT) / tCount

function drawCurve(p) {
  p.noFill();
  p.strokeWeight(2);
  p.stroke('green');
  p.beginShape();

  let values = gamma(curveFromT);
  for (let t = curveFromT; t <= curveToT; t += dt) {
    values = gamma(t);
    p.vertex(toCanvasX(values.x), toCanvasY(values.y));
  }
  values = gamma(curveToT);
  p.vertex(toCanvasX(values.x), toCanvasY(values.y)); // Иногда не дорисовывает

  p.endShape();
}

function drawTangent(p, t) {
  let pt = gamma(t);
  let vel = velocity(gamma, t);

  // Нормализуем, чтобы вектор не был слишком длинным (это, по идее, вектор dg/ds)
  let len = Math.sqrt(vel.x ** 2 + vel.y ** 2);
  vel.x /= len;
  vel.y /= len;

  //let scale = 40; // длина стрелки
  let scale = 10; // TODO: scale тоже сделать изменяемым

  p.stroke(255, 30, 30);
  p.line(toCanvasX(pt.x), toCanvasY(pt.y), toCanvasX(pt.x + vel.x * scale), toCanvasY(pt.y + vel.y * scale));
}

function drawVelocity(p) {
  p.noFill();
  p.strokeWeight(2);
  p.stroke('red');
  p.beginShape();

  for (let t = curveFromT; t <= curveToT; t += dt) {
    drawTangent(p, t);
  }
  drawTangent(p, curveToT);

  p.endShape();
}

let t0 = curveToT;
let dt0 = 0.1;

function drawPointOnCurve(p) {
  p.noFill();
  p.stroke('green');
  p.fill('violet');
  let values = gamma(t0)
  p.circle(toCanvasX(values.x), toCanvasY(values.y), 10);
}

function processKeys(p) {
  // Смещение относительно центра
  if (p.keyIsDown(p.UP_ARROW)) {
    console.log('UP_ARROW нажата!');
    canvasBottom += dCanvasVertical;
    canvasTop += dCanvasVertical;
  }
  if (p.keyIsDown(p.DOWN_ARROW)) { // Проверка на стрелку вверх
    console.log('DOWN_ARROW нажата!');
    canvasBottom -= dCanvasVertical;
    canvasTop -= dCanvasVertical;
  }
  if (p.keyIsDown(p.LEFT_ARROW)) {
    console.log('LEFT_ARROW нажата!');
    canvasLeft -= dCanvasHorizontal;
    canvasRight -= dCanvasHorizontal;
  }
  if (p.keyIsDown(p.RIGHT_ARROW)) {
    console.log('RIGHT_ARROW нажата!');
    canvasLeft += dCanvasHorizontal;
    canvasRight += dCanvasHorizontal;
  }
  // ZOOM (неправильно, нужно, чтобы оно было относительно центра окна)
  if (p.keyIsDown(65)) {
    console.log('A нажата!');
    canvasLeft *= dCanvasHorizontal;
    canvasRight *= dCanvasHorizontal;
  }
  if (p.keyIsDown(68)) {
    console.log('D нажата!');
    canvasLeft /= dCanvasHorizontal;
    canvasRight /= dCanvasHorizontal;
  }
  if (p.keyIsDown(87)) {
    console.log('W нажата!');
    canvasBottom *= dCanvasVertical;
    canvasTop *= dCanvasVertical;
  }
  if (p.keyIsDown(83)) {
    console.log('S нажата!');
    canvasBottom /= dCanvasVertical;
    canvasTop /= dCanvasVertical;
  }

  // Точка на кривой
  if (p.keyIsDown(81)) {
    console.log('Q нажата!');
    t0 -= dt0;
    if (t0 < curveFromT) {
      t0 = curveFromT;
    }
  }
  if (p.keyIsDown(69)) {
    console.log('E нажата!');
    t0 += dt0;
    if (t0 > curveToT) {
      t0 = curveToT;
    }
  }

  // reset
  if (p.keyIsDown(82)) {
    let values = velocity(gamma, t0);
    console.log(values.x, ' ', values.y)
  }
}

