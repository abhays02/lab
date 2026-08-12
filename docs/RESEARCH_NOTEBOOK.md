# Lab notebook

> A visual index of the experiments in this repository.
>
> **Epistemic rule:** a reproduced result is not presented as a new scientific finding. Each experiment separates published knowledge from what was independently computed here.

## How to read the lab

```text
       QUESTION
          │
          ▼
     ┌───────────┐
     │  RUN IT   │  ← from-scratch code / deterministic logs
     └─────┬─────┘
           │
     ┌─────▼─────┐
     │ VERIFY IT │  ← correctness checks / raw artifacts
     └─────┬─────┘
           │
       ┌───▼─────────────────┐
       │ WHAT DO WE ACTUALLY  │
       │ KNOW FROM THIS RUN?  │
       └───┬───────────┬──────┘
           │           │
     ESTABLISHED     VERIFIED
       by prior       here
      literature   in this repo
           │           │
           └─────┬─────┘
                 ▼
             OPEN QUESTION
```

## Experiments

| Experiment | Visual idea | Core observation | Epistemic status |
|---|---|---|---|
| [barren-plateaus](../barren-plateaus/) | **Signal → silence** | Global parity gradients collapse much faster than the local observable in the same shallow random-circuit family. | Reproduction + verified run |
| [double-descent](../double-descent/) | **The interpolation cliff** | Minimum-norm regression reproduces the sharp risk spike at the interpolation threshold and the immediate post-threshold collapse. | Reproduction + verified run |
| [colibri-glm](../colibri-glm/) | **A model bigger than the machine** | Published GLM/Colibri numbers imply only ~5.4% active parameters per token, while cold-token disk traffic is much slower than rated sequential NVMe throughput. | Arithmetic validation of published claims |
| [sorting-network-depth](../sorting-network-depth/) | **One layer too deep** | Batcher's construction sorts correctly, but at n=16 it uses depth 10 while the proven optimum is 9. | Reproduction + verification |
| [quantum-advantage-boundary](../quantum-advantage-boundary/) | **Where does the classical chase stop?** | A from-scratch 14-qubit RCS toy model reaches Porter–Thomas statistics with depth; exact full-statevector storage becomes enormous at real-system width. | Validation / framing, not a new advantage claim |
| [emergence-mirage](../emergence-mirage/) | **Same curve, different illusion** | A smooth underlying accuracy curve can look like a sudden “emergence” event when exact-match requires many simultaneous correct tokens. | Reproduction of a known metric effect |
| [grokking-silence](https://github.com/abhays02/grokking-silence) | **Learning after memorization** | Training can reach perfect memorization long before test performance later improves toward the learned rule. | Standalone reproduction |

## What counts as “ours”

The repository contains **our implementation, our runs, our logs, and our visual explanations**. That does not make the underlying phenomenon ours.

Use these labels precisely:

- **ESTABLISHED** — supported by prior literature or a primary source.
- **VERIFIED HERE** — independently recomputed in this repository.
- **HYPOTHESIS** — an explicit question or interpretation that remains open.
- **NOT CLAIMED** — deliberately excluded from the lab's novelty claims.

## Visual language

Each experiment should explain itself in three layers:

1. **Phenomenon:** one image / animation that makes the question intuitive.
2. **Measurement:** one chart or compact table that shows exactly what was measured.
3. **Evidence:** the script + raw log + validation notes that make the result reproducible.

Do not use decorative visuals that imply evidence that was not measured.

## Provenance

This index is intentionally conservative. It is a map of reproducible experiments, not a claim that every experiment is a new scientific contribution.
