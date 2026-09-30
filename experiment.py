import numpy as np
import matplotlib.pyplot as plt

# Создаем двумерный массив
data = np.array([
    [10, 20, 30, 45],
    [55,  1, 99, 12],
    [ 7, 88, 14, 23]
])

# Превращаем массив в красивую строку текста
# (каждая строчка массива начнется с новой строки '\n')
matrix_string = '\n'.join('   '.join(f'{num:3d}' for num in row) for row in data)

fig, ax = plt.subplots(figsize=(6, 4))

# Выводим текст по центру холста
# Важно: family='monospace' гарантирует, что числа встанут ровно друг под другом
ax.text(0.5, 0.5, matrix_string, 
        horizontalalignment='center', 
        verticalalignment='center', 
        fontsize=16, 
        family='monospace', 
        fontweight='bold')

# Полностью скрываем оси и рамку графика, оставляя только чистый холст
ax.axis('off')

plt.show()
