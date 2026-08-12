# Barren plateaus

<p align="center">
  <img src="frame.html" alt="Gradient variance collapses for the global cost" width="100%" />
</p>

> **When does a learning signal go silent?**

| Measure | 2 qubits | 12 qubits |
|---|---:|---:|
| Local gradient variance | 0.1127 | 0.0325 |
| Global gradient variance | 0.0977 | 0.000101 |

### What happened

```text
LOCAL   0.1127 ───────────────→ 0.0325
GLOBAL  0.0977 ───────────────→ 0.000101
                                  ↓
                              ~965× drop
```

### What I ran

- Pure NumPy statevector simulator
- Fixed depth: 20
- 150 random circuits per qubit count
- 2 → 12 qubits
- Exact parameter-shift gradients
- Local `<Z₀>` vs global parity `<Z₀…Zₙ₋₁>`

### What this means

- The global readout loses usable signal much faster.
- The local readout shrinks, but does not collapse in this run.
- This is a reproduction of an established barren-plateau effect.
- The numbers above are independently computed here.

### Open question

Can we characterize useful circuit families that avoid the collapse at practical scale?

### Reproduce

```bash
python barren.py
```

Then inspect:

- `barren_log.json` — raw measurements
- `visual.html` — interactive visual
- `compute.md` — provenance and claim classification

[Back to the lab](../)
