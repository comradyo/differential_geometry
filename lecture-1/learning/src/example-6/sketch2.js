function sketch2(p) {
  p.setup = function () {
    p.createCanvas(300, canvasHeight);
    p.background(backgroundColor);
  };

  p.draw = function () {
    p.background(backgroundColor);
    p.stroke(captionsColor)
    let pt = gamma(t0)
    p.text(`t0 = ${t0}`, 10, 10)
    p.text(`x = ${pt.x}`, 10, 30)
    p.text(`y = ${pt.y}`, 10, 50)
    let ptVel = velocity(gamma, t0)
    p.text(`vel.x = ${ptVel.x}`, 10, 70)
    p.text(`vel.y = ${ptVel.y}`, 10, 90)
    p.text(`speed = ${vectorLen(ptVel)}`, 10, 110)
    let ptAcc = acceleration(gamma, t0);
    p.text(`acc.x = ${ptAcc.x}`, 10, 130)
    p.text(`acc.y = ${ptAcc.y}`, 10, 150)
    p.text(`acceleration = ${vectorLen(ptAcc)}`, 10, 170)
    let curv = curvature(gamma, t0)
    let rad = curvatureRadius(gamma, t0)
    p.text(`curvature = ${curv}`, 10, 190)
    p.text(`curvature radius = ${rad}`, 10, 210)
  };
}

/*
p.millis() - Returns the number of milliseconds (thousandths of a second) since starting the sketch (when setup() is called).!

    let t = p.millis() / 1000;
    p.rect(150 + 50 * p.sin(t), 150 + 50 * p.cos(t), 20, 20);
*/