let circleX = 200;
let circleY = 150;
let circleRadius = 75;

let graphX = 50;
let graphY = 300;
let graphAmplitude = 50;
let graphPeriod = 300;

function setup() {
  createCanvas(400, 400);
  angleMode(DEGREES);
  describe(
    'Animated demonstration of a point moving around the unit circle, together with the corresponding sine and cosine values moving along their graphs.'
  );
}

function draw() {
  background(0);

  // Set angle based on frameCount, and display current value

  let angle = frameCount % 360;

  fill(200, 100, 70); // выбираем цвет, которым будем заполнять формы
  textSize(20);       // размер текста
  textAlign(LEFT, CENTER);          // положение текста, который планируем сейчас отрисовать
  text(`angle: ${angle}`, 25, 25);  // строка, x, y

  // Draw circle and diameters

  noFill();
  stroke(128);  // цвет линии (контура)
  strokeWeight(3); // ширина линии
  circle(circleX, circleY, 2 * circleRadius); // рисует круг
  line(circleX, circleY - circleRadius, circleX, circleY + circleRadius); // рисует линию, x1, y1, x2, y2
  line(circleX - circleRadius, circleY, circleX + circleRadius, circleY);

  // Draw moving points

  let pointX = circleX + circleRadius * cos(angle);
  let pointY = circleY - circleRadius * sin(angle);

  line(circleX, circleY, pointX, pointY);

  noStroke();

  fill('white');
  circle(pointX, pointY, 10);

  fill('orange');
  circle(pointX, circleY, 10);

  fill('red');
  circle(circleX, pointY, 10);

  // Draw graph

  stroke('grey');
  strokeWeight(3);
  line(graphX, graphY, graphX + 300, graphY);
  line(graphX, graphY - graphAmplitude, graphX, graphY + graphAmplitude);
  line(
    graphX + graphPeriod,
    graphY - graphAmplitude,
    graphX + graphPeriod,
    graphY + graphAmplitude
  );

  fill('grey');
  strokeWeight(1);
  textAlign(CENTER, CENTER);
  text('0', graphX, graphY + graphAmplitude + 20);
  text('360', graphX + graphPeriod, graphY + graphAmplitude + 20);
  text('1', graphX / 2, graphY - graphAmplitude);
  text('0', graphX / 2, graphY);
  text('-1', graphX / 2, graphY + graphAmplitude);

  fill('orange');
  text('cos', graphX + graphPeriod + graphX / 2, graphY - graphAmplitude);
  fill('red');
  text('sin', graphX + graphPeriod + graphX / 2, graphY);

  // Draw cosine curve

  noFill();
  stroke('orange');
  beginShape();
  for (let t = 0; t <= 360; t++) {
    let x = map(t, 0, 360, graphX, graphX + graphPeriod); // массив типа? А, или масштабирование числа
    let y = graphY - graphAmplitude * cos(t);
    vertex(x, y);
  }
  endShape();

  // Draw sine curve

  noFill();
  stroke('red');
  beginShape();
  for (let t = 0; t <= 360; t++) {
    let x = map(t, 0, 360, graphX, graphX + graphPeriod);
    let y = graphY - graphAmplitude * sin(t);
    vertex(x, y);
  }
  endShape();

  // Draw moving line

  let lineX = map(angle, 0, 360, graphX, graphX + graphPeriod);
  stroke('grey');
  line(lineX, graphY - graphAmplitude, lineX, graphY + graphAmplitude);

  // Draw moving points on graph

  let orangeY = graphY - graphAmplitude * cos(angle);
  let redY = graphY - graphAmplitude * sin(angle);

  noStroke();

  fill('orange');
  circle(lineX, orangeY, 10);

  fill('red');
  circle(lineX, redY, 10);
}
