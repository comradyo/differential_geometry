// Выражение для компонента X кривой
function curveX(t) {
  //return Math.pow(t, 3);
  //return t
  return 10*Math.sin(t)
}

// Выражение для компонента Y кривой
function curveY(t) {
  return Math.pow(t, 2);
  //return t*t
}

// Функция кривой
function gamma(t) {
    return {
        x: curveX(t),
        y: curveY(t)
    };
}

// Первая производная (скорость)
function velocity(gammaFunc, t, eps = 1e-3) {
  let p1 = gammaFunc(t + eps);
  let p0 = gammaFunc(t - eps);
  return {
    x: (p1.x - p0.x) / (2 * eps),
    y: (p1.y - p0.y) / (2 * eps)
  };
}
