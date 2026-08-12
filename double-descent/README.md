# Double descent

<p align="center">
  <img src="animation.svg" alt="Test error spikes at the interpolation threshold" width="100%" />
</p>

> **One extra feature can change the result dramatically.**

| Feature count | Test MSE |
|---:|---:|
| 5 | 1.209 |
| 100 | **238,807** |
| 101 | **32.9** |
| 2,000 | 0.464 |

## What you are seeing

```text
fit improves
    ↓
interpolation threshold
    ↓
238,807
    ↓
one more feature
    ↓
32.9
```

## The run

- 100 training points
- Random Fourier features
- Minimum-norm least squares
- 30 random trials per feature count
- Sweep: `5 → 2,000`
- Same fitting method on both sides

## Takeaway

This is a from-scratch reproduction of established double-descent behavior. The value here is seeing the scale of the spike directly.

## Go deeper

[Open the animated visual](visual.html) · [Run the code](double_descent.py) · [Read the evidence](compute.md) · [Inspect raw data](double_descent_log.json)

[Back to the lab](../)
