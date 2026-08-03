"""
Strassen's algorithm vs naive divide-and-conquer matrix multiplication.

Both are implemented as recursive block algorithms with an identical
structure (split into quadrants, recurse, recombine) and an identical
leaf case (numpy's dense multiply below a size threshold). The only
difference is the textbook one: naive recursion makes 8 recursive
multiplications per level, Strassen's makes 7. Instrumenting both lets
us verify, by actually running the code, that this single difference
in call count produces the exponent gap the literature claims
(log2(8) = 3 vs log2(7) ~= 2.807), and to measure real wall-clock
speedup on top of numpy's own leaf-level BLAS calls.

Run: python3 strassen.py
Writes matmul_log.json with every measurement.
"""

import json
import time
import numpy as np

LEAF = 32  # below this size, just call numpy's dense matmul directly


def naive_dc(A, B, counter):
    n = A.shape[0]
    if n <= LEAF:
        counter[0] += 1
        return A @ B
    h = n // 2
    A11, A12, A21, A22 = A[:h, :h], A[:h, h:], A[h:, :h], A[h:, h:]
    B11, B12, B21, B22 = B[:h, :h], B[:h, h:], B[h:, :h], B[h:, h:]
    C11 = naive_dc(A11, B11, counter) + naive_dc(A12, B21, counter)
    C12 = naive_dc(A11, B12, counter) + naive_dc(A12, B22, counter)
    C21 = naive_dc(A21, B11, counter) + naive_dc(A22, B21, counter)
    C22 = naive_dc(A21, B12, counter) + naive_dc(A22, B22, counter)
    top = np.hstack((C11, C12))
    bot = np.hstack((C21, C22))
    return np.vstack((top, bot))


def strassen(A, B, counter):
    n = A.shape[0]
    if n <= LEAF:
        counter[0] += 1
        return A @ B
    h = n // 2
    A11, A12, A21, A22 = A[:h, :h], A[:h, h:], A[h:, :h], A[h:, h:]
    B11, B12, B21, B22 = B[:h, :h], B[:h, h:], B[h:, :h], B[h:, h:]

    M1 = strassen(A11 + A22, B11 + B22, counter)
    M2 = strassen(A21 + A22, B11, counter)
    M3 = strassen(A11, B12 - B22, counter)
    M4 = strassen(A22, B21 - B11, counter)
    M5 = strassen(A11 + A12, B22, counter)
    M6 = strassen(A21 - A11, B11 + B12, counter)
    M7 = strassen(A12 - A22, B21 + B22, counter)

    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    top = np.hstack((C11, C12))
    bot = np.hstack((C21, C22))
    return np.vstack((top, bot))


def log_slope(xs, ys):
    """Least-squares slope of log(ys) vs log(xs) -- the empirical exponent."""
    lx = np.log(xs)
    ly = np.log(ys)
    A = np.vstack([lx, np.ones_like(lx)]).T
    slope, intercept = np.linalg.lstsq(A, ly, rcond=None)[0]
    return float(slope)


def main():
    rng = np.random.default_rng(47)
    sizes = [64, 128, 256, 512, 1024, 2048]
    results = []

    for n in [64, 128, 256]:
        A = rng.standard_normal((n, n))
        B = rng.standard_normal((n, n))
        ref = A @ B
        c = [0]
        got_naive = naive_dc(A, B, c)
        c2 = [0]
        got_strassen = strassen(A, B, c2)
        assert np.allclose(ref, got_naive, atol=1e-8), f"naive_dc wrong at n={n}"
        assert np.allclose(ref, got_strassen, atol=1e-8), f"strassen wrong at n={n}"

    correctness = "PASS: naive_dc and strassen both match numpy A@B (atol=1e-8) at n=64,128,256"

    for n in sizes:
        A = rng.standard_normal((n, n))
        B = rng.standard_normal((n, n))

        c_naive = [0]
        t0 = time.perf_counter()
        naive_dc(A, B, c_naive)
        t_naive = time.perf_counter() - t0

        c_strassen = [0]
        t0 = time.perf_counter()
        strassen(A, B, c_strassen)
        t_strassen = time.perf_counter() - t0

        results.append({
            "n": n,
            "naive_leaf_multiplications": c_naive[0],
            "strassen_leaf_multiplications": c_strassen[0],
            "naive_seconds": t_naive,
            "strassen_seconds": t_strassen,
        })
        print(f"n={n:5d}  naive_calls={c_naive[0]:7d}  strassen_calls={c_strassen[0]:7d}"
              f"  naive_t={t_naive:.4f}s  strassen_t={t_strassen:.4f}s")

    ns = np.array([r["n"] for r in results], dtype=float)
    naive_calls = np.array([r["naive_leaf_multiplications"] for r in results], dtype=float)
    strassen_calls = np.array([r["strassen_leaf_multiplications"] for r in results], dtype=float)
    naive_t = np.array([r["naive_seconds"] for r in results], dtype=float)
    strassen_t = np.array([r["strassen_seconds"] for r in results], dtype=float)

    exponent_naive_calls = log_slope(ns, naive_calls)
    exponent_strassen_calls = log_slope(ns, strassen_calls)
    exponent_naive_time = log_slope(ns, naive_t)
    exponent_strassen_time = log_slope(ns, strassen_t)

    summary = {
        "leaf_threshold": LEAF,
        "sizes": sizes,
        "correctness": correctness,
        "results": results,
        "empirical_exponent_from_leaf_multiplication_counts": {
            "naive": exponent_naive_calls,
            "strassen": exponent_strassen_calls,
            "theoretical_naive": float(np.log2(8)),
            "theoretical_strassen": float(np.log2(7)),
        },
        "empirical_exponent_from_wallclock": {
            "naive": exponent_naive_time,
            "strassen": exponent_strassen_time,
            "note": "wall-clock includes numpy leaf-call and python recursion overhead, "
                    "so this is noisier than the call-count exponent; included for the "
                    "real speedup number, not as a precise exponent measurement.",
        },
        "speedup_at_largest_n": {
            "n": sizes[-1],
            "naive_seconds": results[-1]["naive_seconds"],
            "strassen_seconds": results[-1]["strassen_seconds"],
            "speedup_x": results[-1]["naive_seconds"] / results[-1]["strassen_seconds"],
        },
    }

    print(json.dumps(summary["empirical_exponent_from_leaf_multiplication_counts"], indent=2))
    print(json.dumps(summary["speedup_at_largest_n"], indent=2))

    with open("matmul_log.json", "w") as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    main()
