// TODO: нормально переписать

// Функция правых частей (аналог вашего parallel_transport_ode)
export function geodesicDerivatives(u, v, dot_u, dot_v, surface) {
    let Gamma = surface.Christoffel_Symbols(u, v);

    let ddot_u = -(
        Gamma[0][0][0] * dot_u ** 2 +
        2 * Gamma[0][1][0] * dot_u * dot_v +
        Gamma[1][1][0] * dot_v ** 2
    );

    let ddot_v = -(
        Gamma[0][0][1] * dot_u ** 2 +
        2 * Gamma[0][1][1] * dot_u * dot_v +
        Gamma[1][1][1] * dot_v ** 2
    )

    return [dot_u, dot_v, ddot_u, ddot_v];
}

// Один шаг метода Рунге-Кутты 4-го порядка (RK4)
// state = [u, v, dot_u, dot_v]
export function rk4Step(state, dt, surface) {
    let [u, v, dot_u, dot_v] = state; // Достаём данные из state

    // --- k1 (Шаг в исходной точке) ---
    let k1 = geodesicDerivatives(u, v, dot_u, dot_v, surface);

    // --- k2 (Прогноз на половину шага вперед, используя k1) ---
    let u2 = u + 0.5 * dt * k1[0];
    let v2 = v + 0.5 * dt * k1[1];
    let k2 = geodesicDerivatives(u2, v2, dot_u + 0.5 * dt * k1[2], dot_v + 0.5 * dt * k1[3], surface);

    // --- k3 (Второй прогноз на половину шага вперед, используя k2) ---
    let u3 = u + 0.5 * dt * k2[0];
    let v3 = v + 0.5 * dt * k2[1];
    let k3 = geodesicDerivatives(u3, v3, dot_u + 0.5 * dt * k2[2], dot_v + 0.5 * dt * k2[3], surface);

    // --- k4 (Прогноз на полный шаг вперед, используя k3) ---
    let u4 = u + dt * k3[0];
    let v4 = v + dt * k3[1];
    let k4 = geodesicDerivatives(u4, v4, dot_u + dt * k3[2], dot_v + dt * k3[3], surface);

    // --- ИТОГОВОЕ СУММИРОВАНИЕ (Взвешенное среднее по формуле RK4) ---
    let next_u = u + (dt / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]);
    let next_v = v + (dt / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]);
    let next_dot_u = dot_u + (dt / 6) * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]);
    let next_dot_v = dot_v + (dt / 6) * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]);

    // Возвращаем новый массив состояния
    return [next_u, next_v, next_dot_u, next_dot_v];
}
