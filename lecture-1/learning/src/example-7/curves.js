// Выражение для компонента X кривой
function curveX(t) {
  //return Math.pow(t, 3);
  //return t + Math.cos(t) - t*t;
  //return 10*Math.sin(t) + t;
  //return 10 * Math.sin(t) - t * t;
  //return t;
  return t*t;
}

// Выражение для компонента Y кривой
function curveY(t) {
  //return Math.pow(t, 2);
  //return 10*Math.cos(t) + t * t;
  //return 10 * Math.cos(t) + t;
  //return 20 * Math.cos(t);
  //return t * t
  return 5*Math.sin(t);
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

// Вторая производная (ускорение)
function acceleration(gammaFunc, t, eps = 1e-3) {
  let p1 = velocity(gammaFunc, t + eps);
  let p0 = velocity(gammaFunc, t - eps);
  return {
    x: (p1.x - p0.x) / (2 * eps),
    y: (p1.y - p0.y) / (2 * eps)
  };
}

// Длина вектора
function vectorLen(vec) {
  return Math.sqrt(vec.x * vec.x + vec.y * vec.y);
}

function scalarMultipy(v1, v2) {
  return v1.x*v2.x + v1.y*v2.y;
}

function multipty(scalar, v) {
  return {
    x: scalar * v.x,
    y: scalar * v.y
  };
}

function add(v1, v2) {
  return {
    x: v1.x + v2.x,
    y: v1.y + v2.y
  };
}

// projectionVector - проекция v1 на v2
function projectionVector(v1, v2) {
  let sm = scalarMultipy(v1, v2);
  let len = vectorLen(v2);
  let koef = sm / (len * len);
  return multipty(koef, v2);
}

// projectionVector - перпендикулярная составляющая v1 к v2
function perpendicularVector(v1, v2) {
  let proj = projectionVector(v1, v2);
  return add(v1, multipty(-1, proj));
}

// curvature - кривизна в точке
function curvature(gamma, t0) {
  let v2 = velocity(gamma, t0);
  let v1 = acceleration(gamma, t0);
  let x = vectorLen(
    add(
      acceleration(gamma, t0), 
      multipty(-1, projectionVector(v1, v2))
    )
  );
  let y = vectorLen(velocity(gamma, t0));
  return x/(y*y);
}

// curvatureRadius - радиус кривизны в точке
function curvatureRadius(gamma, t0) {
  let v2 = velocity(gamma, t0);
  let v1 = acceleration(gamma, t0);
    let x = vectorLen(
    add(
      acceleration(gamma, t0), 
      multipty(-1, projectionVector(v1, v2))
    )
  );
  let y = vectorLen(velocity(gamma, t0));
  return (y*y)/x
}

// normaliseVector - нормализация вектора
function normaliseVector(v) {
  len = vectorLen(v);
  return {
    x: v.x/len,
    y: v.y/len
  }
}

// curveLength - длина кривой от t1 до t2
function curveLength(gamma, t1, t2) {
  let dt_ = (curveToT-curveFromT) / 1000;
  let len = 0;
  for (let t = t1; t < t2; t += dt_) {
    len += vectorLen(velocity(gamma, t)) * dt_;
  }
  return len;
}