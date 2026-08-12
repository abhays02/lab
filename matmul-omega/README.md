# Matrix multiplication: omega

<p align="center">
  <img src="frame.png" alt="Matrix multiplication experiment" width="100%" />
</p>

> **Strassen saves a multiplication. Then the recursion does the rest.**

### What I measured

| n | Naive leaf calls | Strassen leaf calls | Wall-clock speedup |
|---:|---:|---:|---:|
| 64 | 8 | 7 | 0.89x |
| 256 | 512 | 343 | 0.53x |
| 1,024 | 32,768 | 16,807 | 0.79x |
| 2,048 | 262,144 | 117,649 | **1.06x** |

### The exponent

```text
naive       8^k → n^3.0000
Strassen    7^k → n^2.8074
```

Both implementations use the same recursion structure and the same NumPy leaf multiplication.

Only the number of recursive multiplications changes.

### What I verified

- Correct against NumPy at `n = 64, 128, 256`.
- Empirical naive exponent: `3.0000`.
- Empirical Strassen exponent: `2.8074`.
- The measured 2,048 × 2,048 speedup is only about `1.06x` in this Python implementation.

That last number matters.

Asymptotic improvement does not automatically mean a dramatic wall-clock win in a small implementation.

### The open question

The matrix multiplication exponent is still above the trivial lower bound of 2.

Can it ever reach 2?

This experiment does not answer that.

### Reproduce

```bash
python strassen.py
```

Then inspect:

- `matmul_log.json` — raw measurements
- `compute.md` — provenance and literature

[Back to the lab](../)
