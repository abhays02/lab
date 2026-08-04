"""
rcs_verify.py -- validation-gate computation for the "quantum advantage
boundary" post (abhays02 / lab / quantum-advantage-boundary).

Three independent, from-scratch computations, no external quantum
libraries:

1. Porter-Thomas check: simulate random quantum circuits (statevector,
   brick-pattern single-qubit rotations + entangling CZ gates, the same
   structural ingredients real random-circuit-sampling experiments use)
   and check whether the output distribution matches the Porter-Thomas
   law that both (a) the classical-hardness argument and (b) the XEB
   verification statistic used in real experiments depend on.

2. Exact classical memory-cost table for full statevector simulation,
   n = 10..60 qubits. Pure arithmetic, not a simulation -- this is the
   concrete, undisputed reason EXACT classical simulation is impossible
   past a certain width (which is why the real classical competition
   uses approximate tensor-network methods instead, not full statevectors).

3. Linear XEB fidelity computed on this run's own noiseless simulated
   circuits, as a sanity check that the estimator behaves the way the
   literature says it should on a perfect (noiseless) simulation.

Everything here is run on n=14 qubits (2^14 = 16,384-dim statevector),
small enough to be exact and fast, structurally the same ingredients as
a real RCS circuit at far larger n.
"""

import numpy as np

rng = np.random.default_rng(20260804)

N_QUBITS = 14
DIM = 2 ** N_QUBITS
LAYERS = 40          # cycles of (random single-qubit layer + entangling layer)
N_CIRCUITS = 6       # independent random circuit instances, pooled for stats
DEPTH_SWEEP = [9, 15, 20, 30, 40, 60]  # shows convergence to Porter-Thomas


def random_su2():
    """Haar-random single-qubit unitary via random Euler angles."""
    theta = np.arccos(1 - 2 * rng.random())
    phi = rng.random() * 2 * np.pi
    lam = rng.random() * 2 * np.pi
    a = np.cos(theta / 2)
    b = -np.exp(1j * lam) * np.sin(theta / 2)
    c = np.exp(1j * phi) * np.sin(theta / 2)
    d = np.exp(1j * (phi + lam)) * np.cos(theta / 2)
    return np.array([[a, b], [c, d]], dtype=complex)


def apply_single_qubit(state, u, qubit, n):
    """Apply 2x2 unitary u to `qubit` of an n-qubit statevector."""
    state = state.reshape([2] * n)
    state = np.moveaxis(state, qubit, 0)
    state = np.tensordot(u, state, axes=([1], [0]))
    state = np.moveaxis(state, 0, qubit)
    return state.reshape(-1)


def apply_cz(state, q0, q1, n):
    """Apply a CZ gate (entangler used in real RCS circuits) to q0,q1."""
    state = state.reshape([2] * n)
    idx = [slice(None)] * n
    idx[q0] = 1
    idx[q1] = 1
    state[tuple(idx)] *= -1
    return state.reshape(-1)


def run_random_circuit(n, layers, seed_rng):
    state = np.zeros(2 ** n, dtype=complex)
    state[0] = 1.0
    for layer in range(layers):
        for q in range(n):
            state = apply_single_qubit(state, random_su2(), q, n)
        start = 0 if layer % 2 == 0 else 1
        for q0 in range(start, n - 1, 2):
            state = apply_cz(state, q0, q0 + 1, n)
    return state


def porter_thomas_check(probs_pool, dim):
    """
    Compare pooled output probabilities (scaled by dim) against the
    Porter-Thomas law P(q) = exp(-q), q = dim * p.
    Theoretical mean = 1, theoretical variance = 1 (exponential(1)).
    Also reports max deviation between empirical and theoretical CDF
    (a manual Kolmogorov-Smirnov statistic, no scipy dependency).
    """
    q = dim * probs_pool
    mean_q = float(np.mean(q))
    var_q = float(np.var(q))
    q_sorted = np.sort(q)
    m = len(q_sorted)
    empirical_cdf = np.arange(1, m + 1) / m
    theoretical_cdf = 1 - np.exp(-q_sorted)
    ks_stat = float(np.max(np.abs(empirical_cdf - theoretical_cdf)))
    return {
        "n_samples": int(m),
        "mean_q": mean_q,
        "theoretical_mean_q": 1.0,
        "var_q": var_q,
        "theoretical_var_q": 1.0,
        "ks_statistic": ks_stat,
    }


def linear_xeb(probs, dim, n_measurements, rng):
    """
    Linear XEB estimator on a noiseless simulated circuit: draw samples
    from the TRUE distribution (this is what a perfect, error-free
    quantum computer would do), then score them against the same true
    distribution. For a noiseless simulation this should land close to
    1.0 -- that is the known, established behavior of this estimator,
    reproduced here as a sanity check, not a new claim.
    """
    idx = rng.choice(dim, size=n_measurements, p=probs)
    return float(dim * np.mean(probs[idx]) - 1.0)


def memory_table(qubit_counts, bytes_per_amplitude=16):
    """Exact bytes required to hold a full statevector, n qubits."""
    units = [("KB", 1e3), ("MB", 1e6), ("GB", 1e9), ("TB", 1e12),
             ("PB", 1e15), ("EB", 1e18), ("ZB", 1e21)]
    rows = []
    for n in qubit_counts:
        total_bytes = (2 ** n) * bytes_per_amplitude
        best_unit, best_val = "B", float(total_bytes)
        for name, scale in units:
            if total_bytes >= scale:
                best_unit, best_val = name, total_bytes / scale
        rows.append({
            "qubits": n,
            "bytes_exact": int(total_bytes),
            "human": f"{best_val:,.2f} {best_unit}",
        })
    return rows


def main():
    all_probs = []
    xeb_values = []
    for i in range(N_CIRCUITS):
        state = run_random_circuit(N_QUBITS, LAYERS, rng)
        probs = np.abs(state) ** 2
        probs = probs / probs.sum()  # renormalize against float drift
        all_probs.append(probs)
        xeb_values.append(linear_xeb(probs, DIM, n_measurements=4000, rng=rng))

    pooled = np.concatenate(all_probs)
    pt = porter_thomas_check(pooled, DIM)

    # Depth sweep: does the circuit need to be deep to reach Porter-Thomas
    # statistics? (It does -- this matches the published anti-concentration
    # story: shallow random circuits do not scramble enough to look
    # Haar-random yet.) Separate RNG stream, fixed seed, for reproducibility.
    sweep_rng = np.random.default_rng(7)
    depth_sweep_results = []
    for depth in DEPTH_SWEEP:
        probs_d = []
        for i in range(N_CIRCUITS):
            state = run_random_circuit(N_QUBITS, depth, sweep_rng)
            p = np.abs(state) ** 2
            p = p / p.sum()
            probs_d.append(p)
        pooled_d = np.concatenate(probs_d)
        pt_d = porter_thomas_check(pooled_d, DIM)
        depth_sweep_results.append({"layers": depth, **pt_d})

    mem_rows = memory_table([10, 20, 30, 40, 50, 53, 60])

    results = {
        "circuit": {
            "n_qubits": N_QUBITS,
            "dim": DIM,
            "layers": LAYERS,
            "n_circuit_instances": N_CIRCUITS,
            "gate_set": "Haar-random single-qubit SU(2) + brick-pattern CZ entanglers",
        },
        "porter_thomas_check": pt,
        "depth_sweep_porter_thomas": depth_sweep_results,
        "linear_xeb_per_circuit": xeb_values,
        "linear_xeb_mean": float(np.mean(xeb_values)),
        "linear_xeb_std": float(np.std(xeb_values)),
        "classical_memory_table_full_statevector": mem_rows,
        "sycamore_2019_memory_bytes_exact": int(2 ** 53 * 16),
    }

    import json
    with open("rcs_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
