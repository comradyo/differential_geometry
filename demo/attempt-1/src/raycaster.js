let canvasWidth = 400;
let canvasHeight = 400;

function setup() {
  createCanvas(canvasWidth, canvasHeight);
  angleMode(DEGREES);
  describe(
    'Пытаюсь что-то сделать'
  );
}

function draw() {
  background(0);

  stroke('white');
  fill('white');
  circle(canvasWidth/2, canvasHeight/2, 10);

  stroke('white');
  fill(200, 100, 255)
  circle(posX, posY, 10);
}

export function initRaycaster() {
  const canvas = document.getElementById("raycast");
  const ctx = canvas.getContext("2d");

  function render() {
    const gradient = ctx.createLinearGradient(
      0, 0,
      0, canvas.height
    );

    gradient.addColorStop(0, "blue");
    gradient.addColorStop(1, "orange");

    ctx.fillStyle = gradient;
    ctx.fillRect(
      0, 0,
      canvas.width,
      canvas.height
    );
  }

  // Сразу рисуем первое изображение
  render();

  // Даём остальному коду возможность перерисовать холст
  return { render };
}

