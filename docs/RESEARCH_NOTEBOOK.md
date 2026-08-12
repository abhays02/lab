# Lab notebook

## Six experiments, one visual language

Every experiment is organized around the same questions:

```text
WHAT IS THE QUESTION?
        ↓
WHAT DID WE RUN?
        ↓
WHAT CAME OUT?
        ↓
WHAT DOES IT MEAN?
        ↓
WHAT IS ACTUALLY VERIFIED?
        ↓
WHERE IS THE EVIDENCE?
```

| # | Experiment | Core question | Main measured result |
|---|---|---|---|
| 01 | [Barren plateaus](../barren-plateaus/) | Does the training signal survive as qubits increase? | Global gradient variance: `0.0977 → 0.000101` |
| 02 | [Double descent](../double-descent/) | What happens at the interpolation threshold? | Test MSE: `238,807 → 32.9` from `p=100 → 101` |
| 03 | [Colibri / GLM](../colibri-glm/) | How much of a huge model is active per token? | `5.38%` active; about `11 GB` cold-token reads |
| 04 | [Sorting networks](../sorting-network-depth/) | Can a correct network still be too deep? | `10` rounds vs proven optimum `9` at `n=16` |
| 05 | [Quantum advantage boundary](../quantum-advantage-boundary/) | Why does exact simulation hit a memory wall? | `144.12 PB` for a 53-qubit complex128 statevector |
| 06 | [Emergence mirage](../emergence-mirage/) | Can a metric make a smooth curve look discontinuous? | Exact-match crossing shifts and sharpens as `k` grows |

## How to read the evidence

```text
VISUAL
  ↓
MEASUREMENT
  ↓
CODE
  ↓
RAW OUTPUT
  ↓
PROVENANCE
```

| Label | Meaning |
|---|---|
| **Established** | Known before this run. |
| **Verified here** | Independently computed in this repo. |
| **Not claimed** | Not presented as a new discovery. |

The purpose of the notebook is not to make every experiment sound novel.

It is to make the **actual evidence easy to inspect**.
