// Создаем экземпляр p5 для второго холста
const sketch2 = (p) => {
  p.setup = () => {
    p.createCanvas(200, 200);
    // Можно расположить второй холст ниже или сбоку
    // например, с помощью CSS или позиционирования
  };

  p.draw = () => {
    p.background(0, 255, 0);
    p.rect(p.width/4, p.height/4, 100, 100);
  };
};
