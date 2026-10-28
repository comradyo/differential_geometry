// TODO: нормально переписать

// Функция правых частей
export function geodesicDerivativesInPlace(dot_u, dot_v, Gamma, k) {
    k[0] = dot_u;
    k[1] = dot_v;
    k[2] = -(
        Gamma[0][0][0] * dot_u ** 2 +
        2 * Gamma[0][1][0] * dot_u * dot_v +
        Gamma[1][1][0] * dot_v ** 2
    );
    k[3] = -(
        Gamma[0][0][1] * dot_u ** 2 +
        2 * Gamma[0][1][1] * dot_u * dot_v +
        Gamma[1][1][1] * dot_v ** 2
    );
}

// Один шаг метода Рунге-Кутты 4-го порядка (RK4)
// state = [u, v, dot_u, dot_v]
export function rk4StepInPlace(state, dt, surface) {
    let u = state[0], v = state[1], dot_u = state[2], dot_v = state[3];

    const k1 = new Float64Array(4);
    const k2 = new Float64Array(4);
    const k3 = new Float64Array(4);
    const k4 = new Float64Array(4);

    // --- k1 (Шаг в исходной точке) ---
    geodesicDerivativesInPlace(dot_u, dot_v, surface.Christoffel_Symbols(u, v), k1);

    // --- k2 (Прогноз на половину шага вперед, используя k1) ---
    let u2 = u + 0.5 * dt * k1[0];
    let v2 = v + 0.5 * dt * k1[1];
    geodesicDerivativesInPlace(dot_u + 0.5 * dt * k1[2], dot_v + 0.5 * dt * k1[3], surface.Christoffel_Symbols(u2, v2), k2);

    // --- k3 (Второй прогноз на половину шага вперед, используя k2) ---
    let u3 = u + 0.5 * dt * k2[0];
    let v3 = v + 0.5 * dt * k2[1];
    geodesicDerivativesInPlace(dot_u + 0.5 * dt * k2[2], dot_v + 0.5 * dt * k2[3], surface.Christoffel_Symbols(u3, v3), k3);

    // --- k4 (Прогноз на полный шаг вперед, используя k3) ---
    let u4 = u + dt * k3[0];
    let v4 = v + dt * k3[1];
    geodesicDerivativesInPlace(dot_u + dt * k3[2], dot_v + dt * k3[3], surface.Christoffel_Symbols(u4, v4), k4);

    state[0] = u + (dt / 6) * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]);
    state[1] = v + (dt / 6) * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]);
    state[2] = dot_u + (dt / 6) * (k1[2] + 2 * k2[2] + 2 * k3[2] + k4[2]);
    state[3] = dot_v + (dt / 6) * (k1[3] + 2 * k2[3] + 2 * k3[3] + k4[3]);
}

