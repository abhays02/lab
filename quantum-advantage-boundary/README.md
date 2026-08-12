# Quantum advantage boundary

<p align="center">
  <img src="animation.svg" alt="Exact statevector memory grows to 144.12 PB at 53 qubits" width="100%" />
</p>

> **At 53 qubits, one exact statevector needs 144.12 PB.**

| Check | Result |
|---|---:|
| Circuit size | 14 qubits |
| Samples in deep run | 98,304 |
| Variance at 40 layers | 1.0167 |
| KS statistic at 40 layers | 0.00264 |
| Linear XEB | 1.012 ± 0.015 |
| Full statevector at 53 qubits | 144.12 PB |

## What you are seeing

```text
10q   KB
20q   MB
30q   GB
40q   TB
50q   PB
53q   144.12 PB
60q   18.45 EB
```

## The run

- From-scratch NumPy statevector simulator
- 14 qubits
- Haar-random single-qubit SU(2) gates
- Brick-pattern CZ entanglers
- Depth sweep: `9 → 60`
- Six independent circuits per depth
- Exact memory arithmetic

## Takeaway

This is a validation experiment, not a new quantum-advantage claim.

It shows the storage wall clearly and checks the basic RCS statistics behind the visual story.

## Go deeper

[Open the original visual](visual.svg) · [Run the verifier](rcs_verify.py) · [Read the evidence](compute.md) · [Inspect output](rcs_results.json)

[Back to the lab](../)
