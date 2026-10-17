const canvas = document.getElementById("screen");
const ctx = canvas.getContext("2d");

const w = canvas.width;
const h = canvas.height;

// Создаём пустое изображение
const image = ctx.createImageData(w, h);

for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
        // Индекс первого цветового канала пикселя
        const i = (y * w + x) * 4;

        image.data[i] = x * 255 / w; // красный
        image.data[i + 1] = y * 255 / h; // зелёный
        image.data[i + 2] = 150;         // синий
        image.data[i + 3] = 255;         // прозрачность
    }
}

// Выводим вычисленные пиксели на холст
ctx.putImageData(image, 0, 0);
