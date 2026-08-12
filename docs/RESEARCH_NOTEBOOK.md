# Lab notebook

## What is in this repo

Six experiments. Six folders. Every one keeps the visual, measurement, code, raw output, and provenance close together.

| # | Experiment | Visual idea | What the run actually shows |
|---|---|---|---|
| 01 | [Barren plateaus](../barren-plateaus/) | **Signal → silence** | Global gradient variance falls from `0.0977` to `0.000101`; local variance falls much less. |
| 02 | [Double descent](../double-descent/) | **The interpolation cliff** | Test MSE reaches `238,807` at `p = 100`, then drops to `32.9` at `p = 101`. |
| 03 | [Colibri / GLM](../colibri-glm/) | **A model bigger than the machine** | Published numbers imply only `5.38%` active parameters per token and about `11 GB` of cold-token disk reads. |
| 04 | [Sorting networks](../sorting-network-depth/) | **One layer too deep** | Batcher gives depth `10` at `n = 16`; the proven optimum is `9`. |
| 05 | [Quantum advantage boundary](../quantum-advantage-boundary/) | **The memory wall** | An exact 53-qubit complex128 statevector needs `144.12 PB`; the RCS checks also reproduce the expected depth trend. |
| 06 | [Emergence mirage](../emergence-mirage/) | **Same curve, different jump** | The same smooth per-token curve can look much more abrupt when exact-match requires many correct steps. |

## The visual language

Every experiment starts with the same four questions:

```text
WHAT AM I LOOKING AT?
        ↓
WHAT NUMBER DID WE MEASURE?
        ↓
HOW DID WE CHECK IT?
        ↓
WHERE IS THE CODE?
```

Each folder contains an `animation.svg` for the first answer.

Interactive HTML and poster images stay available as deeper layers where they already exist.

## Provenance

The lab is intentionally conservative.

- **Established** — supported before this run.
- **Verified here** — independently computed in this repo.
- **Hypothesis** — an interpretation or next research question.
- **Not claimed** — deliberately not framed as a new discovery.

The existence of an implementation or a reproduction does not make the underlying phenomenon original.

## Evidence trail

```text
README
  ↓
animation.svg
  ↓
experiment code
  ↓
raw JSON / figure
  ↓
compute.md
```

That is the whole lab in one path.
