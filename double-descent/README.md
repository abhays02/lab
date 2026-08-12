# Double descent

<p align="center">
  <img src="visual.html" alt="Test error spikes at the interpolation threshold and then falls" width="100%" />
</p>

> **One parameter can turn the cliff off.**

| Feature count | Test MSE |
|---:|---:|
| 5 | 1.209 |
| 100 | 238,807 |
| 101 | 32.9 |
| 2,000 | 0.464 |

### The shape

```text
error
  │                 /
  │                /  
  │_______________/\____________
                  100  101       features
```

### What I ran

- 100 fixed training points
- Random Fourier features
- Minimum-norm least squares
- 30 random trials per feature count
- Feature sweep: 5 → 2,000
- Same fitting method on both sides of the threshold

### The striking part

At `p = n = 100`, the mean test MSE reaches **238,807**.

At `p = 101`, it falls to **32.9**.

By `p = 2,000`, it reaches **0.464**.

### What this is

- A from-scratch reproduction of established double-descent theory.
- Not presented as a new discovery.
- The value of the experiment is seeing the scale of the transition directly.

### Reproduce

```bash
python double_descent.py
```

Then inspect:

- `double_descent_log.json` — raw sweep
- `visual.html` — animated poster
- `compute.md` — evidence and literature

[Back to the lab](../)
