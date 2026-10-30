// Глобальные переменные для хранения данных текстуры
let texturePixels = null;
let textureWidth = 0;
let textureHeight = 0;

export function loadTextureToCPU(url) {
    const img = new Image();
    img.crossOrigin = "Anonymous"; // Важно, чтобы браузер разрешил читать пиксели
    img.src = url;

    img.onload = () => {
        textureWidth = img.width;
        textureHeight = img.height;

        // Создаем скрытый холст
        const hiddenCanvas = document.createElement('canvas');
        hiddenCanvas.width = textureWidth;
        hiddenCanvas.height = textureHeight;
        const ctx = hiddenCanvas.getContext('2d');

        // Рисуем картинку на холст
        ctx.drawImage(img, 0, 0);

        // Получаем одномерный массив ВСЕХ пикселей в формате [R, G, B, A, R, G, B, A, ...]
        const imgData = ctx.getImageData(0, 0, textureWidth, textureHeight);
        texturePixels = imgData.data;

        console.log("Texture is loaded");
    };
}

export function getPixelColor(u, v) {
    // Если текстура еще не загрузилась, возвращаем дефолтный серый цвет
    if (!texturePixels) return { r: 100, g: 100, b: 100 };

    // 2. Переводим в пиксельные индексы картинки (X, Y)
    let x = Math.floor(u * (textureWidth - 1));
    let y = Math.floor(v * (textureHeight - 1));

    // 3. Находим индекс начала пикселя в одномерном массиве RGBA
    // Каждая строка содержит textureWidth пикселей, каждый пиксель занимает 4 байта
    let pixelIndex = (y * textureWidth + x) * 4;

    // 4. Вытаскиваем каналы
    let r = texturePixels[pixelIndex];
    let g = texturePixels[pixelIndex + 1];
    let b = texturePixels[pixelIndex + 2];

    return { r, g, b };
}

