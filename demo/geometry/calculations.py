

# Система параллельного переноса (для момента времени t)
def parallel_translation_system(t, xi, curve_func, curve_dt_func, christoffel_func):
    # xi = [xi_u, xi_v]
    # curve_func(t) возвращает (u, v, dot_u, dot_v) для текущего момента времени
    xi_u, xi_v = xi
    u, v = curve_func(t)
    u_t, v_t = curve_dt_func(t)

    Gamma = christoffel_func(u, v)

    # Производные d(xi_u)/dt и d(xi_v)/dt
    dot_xi_u = -(
        Gamma[0][0][0] * u_t * xi_u
        + Gamma[0][1][0] * u_t * xi_v
        + Gamma[1][0][0] * v_t * xi_u
        + Gamma[1][1][0] * v_t * xi_v
    )

    dot_xi_v = -(
        Gamma[0][0][1] * u_t * xi_u
        + Gamma[0][1][1] * u_t * xi_v
        + Gamma[1][0][1] * v_t * xi_u
        + Gamma[1][1][1] * v_t * xi_v
    )

    return [dot_xi_u, dot_xi_v]


# Система параллельного переноса (для момента времени t)
# Y - вектор состояния решения, состоит из четырёх элементов:
#   u, v - текущие координаты
#   dot_u, dot_v - производные координатных функций кривой (по t) в точке
def geodesic_system(t, Y, christoffel_func):
    u, v, dot_u, dot_v = Y
    Gamma = christoffel_func(u, v)  # получаем символы Кристоффеля в текущей точке (u, v)

    # Считаем вторые производные (ускорения) из системы уравнений
    # Обратите внимание на знаки "минус", так как мы перенесли Г в правую часть
    # И на законные двойки перед смешанными слагаемыми!
    ddot_u = -(
        Gamma[0][0][0] * dot_u**2 + 
        2 * Gamma[0][1][0] * dot_u * dot_v + 
        Gamma[1][1][0] * dot_v**2
    )

    ddot_v = -(
        Gamma[0][0][1] * dot_u**2 + 
        2 * Gamma[0][1][1] * dot_u * dot_v + 
        Gamma[1][1][1] * dot_v**2
    )

    return [dot_u, dot_v, ddot_u, ddot_v]
