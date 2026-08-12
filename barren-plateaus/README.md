# Barren plateaus

<p align="center">
  <img src="animation.svg" alt="Global gradient variance collapses as qubits increase" width="100%" />
</p>

## 01. The question

> **What happens to the training signal when the circuit gets wider?**

```text
same circuit
same depth
same parameter
      │
      └──── add qubits ────→
                    ↓
             does the gradient survive?
```

## 02. The comparison

| | Local cost | Global cost |
|---|---|---|
| Readout | `<Z₀>` | `<Z₀ Z₁ ... Zₙ₋₁>` |
| Depth | 20 | 20 |
| Circuits / size | 150 | 150 |
| Width | 2 → 12 qubits | 2 → 12 qubits |

## 03. The result

| Gradient variance | 2 qubits | 12 qubits | Change |
|---|---:|---:|---:|
| Local | 0.1127 | 0.0325 | 3.5× lower |
| Global | 0.0977 | 0.000101 | **965× lower** |

```text
LOCAL
0.1127 ━━━━━━━━━━━━━━━━━━━━━ 0.0325

GLOBAL
0.0977 ━━━━━━━━━━━━━━━━━━━━━ 0.000101
                                  nearly silent
```

## 04. What this answers

**The global objective loses usable gradient signal much faster.**

The local objective shrinks too, but stays much stronger in this run.

## 05. What was actually run

- NumPy statevector simulator
- Random hardware-efficient circuits
- Fixed depth: `20`
- `2, 4, 6, 8, 10, 12` qubits
- `150` circuits per point
- Exact parameter-shift gradients

## 06. What is known vs checked here

| Layer | Answer |
|---|---|
| Established | Barren-plateau suppression is known. |
| Verified here | The local/global contrast above was independently computed. |
| Not claimed | No new theorem or optimizer is claimed. |

## 07. Evidence path

```text
QUESTION
   ↓
VISUAL
   ↓
CODE
   ↓
RAW LOG
   ↓
PROVENANCE
```

[Interactive visual](visual.html) · [Code](barren.py) · [Raw log](barren_log.json) · [Evidence](compute.md)

[Back to the lab](../)
