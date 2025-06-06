function sketch2(p) {
  p.setup = function () {
    p.createCanvas(300, canvasHeight);
    p.background(backgroundColor);
  };

  p.draw = function () {
    p.background(backgroundColor);
    p.stroke(captionsColor)
    let values = gamma(t0)
    p.text(`t0 = ${t0}`, 10, 10)
    p.text(`x = ${values.x}`, 10, 30)
    p.text(`y = ${values.y}`, 10, 50)
  };
}

/*
p.millis() - Returns the number of milliseconds (thousandths of a second) since starting the sketch (when setup() is called).!

    let t = p.millis() / 1000;
    p.rect(150 + 50 * p.sin(t), 150 + 50 * p.cos(t), 20, 20);
*/