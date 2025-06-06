// Создаем экземпляр p5 для первого холста
const sketch1 = (p) => {
  p.setup = () => {
    p.createCanvas(200, 200);
  };

  p.draw = () => {
    p.background(255, 0, 0);
    p.ellipse(p.width/2, p.height/2, 50, 50);
  };
};
