let canvas3Height = canvasHeight;
let canvas3Width = 300;
let canvas3Stroke = 1;

// Преобразуем математические координаты в координаты холста (X)
function toCanvas3X(x) {
  return ((x - canvasLeft) / (canvasRight - canvasLeft)) * canvasWidth
}

// Преобразуем математические координаты в координаты холста (Y)
function toCanvas3Y(y) {
  return canvasHeight - ((y - canvasBottom) / (canvasTop - canvasBottom)) * canvasHeight
}

function sketch3(p) {
  p.setup = function () {
    p.createCanvas(canvas3Width, canvasHeight);
    p.background(backgroundColor);
  };

  p.draw = function () {
    p.translate(0, canvasHeight);
    p.scale(1, -1);
    p.background(100, 100, 100);
    drawView(p);
  };
}

let cameraHeight = 1;
let angleView = Math.PI / 2.1;
let numOfLines = 200;
let dPhi = angleView / numOfLines;

function drawView(p) {
  p.noFill();
  //p.stroke(canvas3Stroke);

  let phi = 0;
  let t1 = t0;
  phi += dPhi;

  let wantLen = 0;
  let curLen = 0;
  let t2 = 0;

  for (let i = 0; i < numOfLines && t1 < curveToT; i++) {
    wantLen = cameraHeight * Math.tan(phi);
    curLen = 0;
    t2 = t1;
    while (curLen < wantLen) {
      curLen = curveLength(gamma, t1, t2);
      t2 += 0.01;
    }
    t1 = t2;
    phi += dPhi;

    col = getCurvePointColor(p, t2);
    p.fill(col);
    p.stroke(col);
    //p.line(0, i * canvas3Stroke, canvas3Width, i * canvas3Stroke);
    p.rect(0, i * canvas3Stroke, canvas3Width, canvas3Stroke)
  }
}

/*
p.millis() - Returns the number of milliseconds (thousandths of a second) since starting the sketch (when setup() is called).!

    let t = p.millis() / 1000;
    p.rect(150 + 50 * p.sin(t), 150 + 50 * p.cos(t), 20, 20);
*/