"""
Reproduces two barren-plateau results with a from-scratch statevector
simulator (no quantum SDK):
- McClean, Boixo, Smelyanskiy, Babbush, Neven, "Barren plateaus in quantum
  neural network training landscapes" (Nature Communications 9, 4812, 2018 /
  arXiv:1803.11173): gradient variance of a random parameterized circuit
  vanishes exponentially with qubit count.
- Cerezo, Sone, Volkoff, Cincio, Coles, "Cost function dependent barren
  plateaus in shallow parametrized quantum circuits" (Nature Communications
  12, 1791, 2021): the severity depends on whether the cost function is
  local (one qubit) or global (all qubits).

Circuit family: single-qubit rotations from {RX,RY,RZ} with random angles,
entangled by a brickwork layer of CZ gates, fixed depth for every qubit
count. For each qubit count, many random circuit instances are drawn; for
each, the exact gradient of one mid-circuit rotation parameter is computed
via the parameter-shift rule against two observables on the same circuit —
local <Z_0> and global <Z_0 Z_1 ... Z_{n-1}> parity — and the gradient's
variance across instances is measured for both.

Output: barren_log.json with variance per qubit count (both observables)
and the raw gradient samples behind every number.
"""
import json
import numpy as np

PAULIS = {
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex),
}


def rotation_gate(pauli, theta):
    P = PAULIS[pauli]
    return np.cos(theta / 2) * np.eye(2, dtype=complex) - 1j * np.sin(theta / 2) * P


def apply_single_qubit_gate(state, gate, qubit, n):
    state = np.moveaxis(state, qubit, 0)
    state = np.tensordot(gate, state, axes=([1], [0]))
    state = np.moveaxis(state, 0, qubit)
    return state


def apply_cz(state, q1, q2, n):
    idx = [slice(None)] * n
    idx[q1] = 1
    idx[q2] = 1
    state[tuple(idx)] *= -1
    return state


def build_circuit_gate_types(n, depth, rng_local):
    return [[rng_local.choice(["X", "Y", "Z"]) for _ in range(n)] for _ in range(depth)]


def cz_pairs(n, layer_idx):
    start = layer_idx % 2
    return [(q, q + 1) for q in range(start, n - 1, 2)]


def run_circuit(n, depth, gate_types, thetas):
    state = np.zeros((2,) * n, dtype=complex)
    state[(0,) * n] = 1.0
    for layer in range(depth):
        for q in range(n):
            g = rotation_gate(gate_types[layer][q], thetas[layer, q])
            state = apply_single_qubit_gate(state, g, q, n)
        for (q1, q2) in cz_pairs(n, layer):
            state = apply_cz(state, q1, q2, n)
    return state


def expectation_local_z0(state, n):
    probs = np.abs(state) ** 2
    idx0 = [slice(None)] * n
    idx0[0] = 0
    idx1 = [slice(None)] * n
    idx1[0] = 1
    return probs[tuple(idx0)].sum() - probs[tuple(idx1)].sum()


_PARITY_CACHE = {}


def parity_sign_tensor(n):
    if n not in _PARITY_CACHE:
        t = np.array([1.0, -1.0])
        for _ in range(n - 1):
            t = np.multiply.outer(t, np.array([1.0, -1.0]))
        _PARITY_CACHE[n] = t
    return _PARITY_CACHE[n]


def expectation_global_parity(state, n):
    probs = np.abs(state) ** 2
    return float(np.sum(probs * parity_sign_tensor(n)))


def gradient_sample(n, depth, target_layer, target_qubit, rng_local):
    gate_types = build_circuit_gate_types(n, depth, rng_local)
    thetas = rng_local.uniform(0, 2 * np.pi, size=(depth, n))

    thetas_plus = thetas.copy()
    thetas_plus[target_layer, target_qubit] += np.pi / 2
    thetas_minus = thetas.copy()
    thetas_minus[target_layer, target_qubit] -= np.pi / 2

    state_plus = run_circuit(n, depth, gate_types, thetas_plus)
    state_minus = run_circuit(n, depth, gate_types, thetas_minus)

    g_local = (expectation_local_z0(state_plus, n) - expectation_local_z0(state_minus, n)) / 2.0
    g_global = (expectation_global_parity(state_plus, n) - expectation_global_parity(state_minus, n)) / 2.0
    return g_local, g_global


def main():
    qubit_counts = [2, 4, 6, 8, 10, 12]
    fixed_depth = 20
    n_samples = 150
    results = {}

    for n in qubit_counts:
        target_layer = fixed_depth // 2
        target_qubit = 0
        grads_local, grads_global = [], []
        for s in range(n_samples):
            local_rng = np.random.default_rng(20260802 * 1000 + n * 100 + s)
            gl, gg = gradient_sample(n, fixed_depth, target_layer, target_qubit, local_rng)
            grads_local.append(float(gl))
            grads_global.append(float(gg))
        grads_local = np.array(grads_local)
        grads_global = np.array(grads_global)
        results[n] = {
            "depth": fixed_depth,
            "n_samples": n_samples,
            "mean_gradient_local": float(np.mean(grads_local)),
            "variance_gradient_local": float(np.var(grads_local)),
            "mean_gradient_global": float(np.mean(grads_global)),
            "variance_gradient_global": float(np.var(grads_global)),
            "grad_samples_local": grads_local.tolist(),
            "grad_samples_global": grads_global.tolist(),
        }
        print(f"n_qubits={n:2d} depth={fixed_depth:2d}  "
              f"var(local Z0)={results[n]['variance_gradient_local']:.3e}  "
              f"var(global parity)={results[n]['variance_gradient_global']:.3e}")

    ns = np.array(qubit_counts, dtype=float)
    logvars_local = np.log(np.array([max(results[n]["variance_gradient_local"], 1e-300) for n in qubit_counts]))
    logvars_global = np.log(np.array([max(results[n]["variance_gradient_global"], 1e-300) for n in qubit_counts]))
    slope_local, intercept_local = np.polyfit(ns, logvars_local, 1)
    slope_global, intercept_global = np.polyfit(ns, logvars_global, 1)
    print(f"\nlocal  Z0     fit: log(var) = {slope_local:.4f}*n + {intercept_local:.4f}  "
          f"(decay base {np.exp(slope_local):.4f} per qubit)")
    print(f"global parity fit: log(var) = {slope_global:.4f}*n + {intercept_global:.4f}  "
          f"(decay base {np.exp(slope_global):.4f} per qubit)")

    out = {
        "description": "gradient variance of two cost functions (local <Z0> vs global "
        "parity <Z0 Z1 ... Zn-1>) w.r.t. one fixed-depth mid-circuit rotation "
        "parameter, over random hardware-efficient circuits, vs qubit count",
        "seed": 20260802,
        "fixed_depth": fixed_depth,
        "qubit_counts": qubit_counts,
        "results": {str(k): v for k, v in results.items()},
        "log_variance_fit": {
            "local": {"slope": float(slope_local), "intercept": float(intercept_local),
                      "decay_base_per_qubit": float(np.exp(slope_local))},
            "global": {"slope": float(slope_global), "intercept": float(intercept_global),
                       "decay_base_per_qubit": float(np.exp(slope_global))},
        },
    }
    with open("barren_log.json", "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
