# Sorting network depth

<p align="center">
  <img src="../assets/lab-intro.svg" alt="Sorting network experiment" width="100%" />
</p>

> **The textbook network is correct. It is just not optimal.**

### What I checked

| n | Batcher depth | Known optimum |
|---:|---:|---:|
| 16 | 10 | 9 |
| 17 | 10 | 10 |
| 28 | 13 best known | not proven optimal |

### From scratch

```text
Batcher
  ↓
comparators
  ↓
parallel layers
  ↓
0 / 1 exhaustive verification
```

For every `n ≤ 16`, every binary input was checked.

**Zero counterexamples.**

### The interesting gap

At `n = 16`:

```text
Batcher       10 rounds
optimal        9 rounds
               ↑
          one round
```

The construction is established.

The verification here is ours.

The larger optimal-depth problem remains open beyond the proven range.

### Reproduce

```bash
python batcher_verify.py
```

Then inspect:

- `batcher_results.json` — measured network structure
- `compute.md` — provenance and literature

[Back to the lab](../)
