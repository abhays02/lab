# ABHAYS02 / LAB

<p align="center">
  <img src="assets/lab-hook.svg" alt="I don't start with answers. I start with something worth checking." width="100%" />
</p>

## The lab in one screen

Six experiments. Six different questions. One rule: **make the result easy to see before asking anyone to read the code.**

| # | Experiment | The question | The result |
|---|---|---|---|
| 01 | [Barren plateaus](barren-plateaus/) | Does the gradient survive as qubits increase? | **965×** global variance drop |
| 02 | [Double descent](double-descent/) | Why can one extra feature change test error so sharply? | **238,807 → 32.9** |
| 03 | [Colibri / GLM](colibri-glm/) | How much of a huge model is active per token? | **5.38% active**; ~**11 GB** implied reads, from published figures |
| 04 | [Sorting networks](sorting-network-depth/) | Can a correct sorting network still be too deep? | **10 vs 9** rounds at `n = 16` |
| 05 | [Quantum advantage boundary](quantum-advantage-boundary/) | Why does exact simulation hit a memory wall? | **144.12 PB** at 53 qubits |
| 06 | [Emergence mirage](emergence-mirage/) | Can a metric make a smooth curve look like a jump? | **Same curve, much sharper story** |

## What happens inside a folder?

```text
           QUESTION
               ↓
        WHAT DID WE RUN?
               ↓
          WHAT CAME OUT?
               ↓
       WHY SHOULD I CARE?
               ↓
     WHAT IS ACTUALLY VERIFIED?
               ↓
       CODE + RAW EVIDENCE
```

Every experiment README answers those questions directly.

## What the visuals are for

The visual is not decoration.

It should let you understand:

```text
WHAT IS MOVING?
WHAT IS BEING COMPARED?
WHERE IS THE SURPRISE?
WHAT NUMBER PROVES IT?
```

Then the reader can choose how deep to go.

## Evidence language

| Label | Meaning |
|---|---|
| **Established** | Known before this run. |
| **Verified here** | Independently computed in this repo. |
| **Not claimed** | Not presented as a new scientific discovery. |

## One consistent evidence trail

<p align="center">
  <img src="assets/evidence-workflow.gif" alt="Schematic workflow: a question leads to an experiment script, its raw JSON output, and provenance notes." width="100%" />
</p>

<p align="center"><em>Schematic only; it contains no experimental data.</em> · <a href="assets/evidence-workflow.svg">Static SVG fallback</a></p>

## The six experiments

**Barren plateaus** — [see the signal collapse](barren-plateaus/)

**Double descent** — [see the interpolation spike](double-descent/)

**Colibri / GLM** — [see the storage bottleneck](colibri-glm/)

**Sorting networks** — [see the depth gap](sorting-network-depth/)

**Quantum advantage boundary** — [see the memory wall](quantum-advantage-boundary/)

**Emergence mirage** — [see how the metric changes the story](emergence-mirage/)

## The research map

[Open the experiment notebook](docs/RESEARCH_NOTEBOOK.md)

## Reproduce a run

Use Python 3.10 or newer. NumPy is required for barren plateaus, double
descent, quantum advantage boundary, and emergence mirage; Colibri's
arithmetic check and the sorting verifier use only the standard library.

```bash
python3 -m pip install numpy
```

| Experiment | Command from the repository root |
|---|---|
| Barren plateaus | `cd barren-plateaus && python3 barren.py` |
| Double descent | `cd double-descent && python3 double_descent.py` |
| Colibri / GLM arithmetic | `cd colibri-glm && python3 colibri_math.py` |
| Sorting-network verifier | `cd sorting-network-depth && python3 batcher_verify.py` |
| Quantum advantage boundary | `cd quantum-advantage-boundary && python3 rcs_verify.py` |
| Emergence mirage | `cd emergence-mirage && python3 emergence_mirage.py` |

Run each script from its experiment folder so generated outputs stay beside
their evidence. Scripts that write JSON replace that folder's result file.
The Colibri script checks arithmetic against published inputs; it does not
run or benchmark the 372 GB model.

The checked-in GIFs can be regenerated from the committed JSON artifacts:

```bash
python3 -m pip install -r requirements-visuals.txt
python3 scripts/generate_visual_gifs.py
```

## Follow-up

The optional `colibri-glm/colibri-meme.hyperframes.html` visual expects
`node_modules/gsap/dist/gsap.min.js`, but the repository has no package
manifest to install it. The README links to the available calculation and
static/animated explainers instead.

[abhays02/lab](https://github.com/abhays02/lab)
