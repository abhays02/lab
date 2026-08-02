# Validation record — barren plateaus (VALIDATION GATE, JOB v3)

## The problem
Variational quantum algorithms (VQE, QAOA, quantum neural networks) train a
parameterized quantum circuit with gradient descent, the same way a classical
neural net trains. As the circuit grows (more qubits, more depth), the
gradient landscape can go flat — not just harder, but exponentially flat, so
the optimizer gets no usable signal anywhere it looks. This is the "barren
plateau" problem. It is a live, actively surveyed open problem, not settled
history: Larocca, Thanasilp, Wang, Sharma, Biamonte, Coles, Cincio, McClean,
Holmes, Cerezo, "Barren plateaus in variational quantum computing," Nature
Reviews Physics (2025), https://www.nature.com/articles/s42254-025-00813-9,
surveys it as an unresolved, central obstacle to scaling VQAs as of 2025.

## What I computed this run
Script: `barren.py` (pure numpy, no quantum SDK — a from-scratch statevector
simulator: gates applied via tensor reshape/contraction on a (2,)^n state
array, CZ applied as a sign flip, gradients via the exact parameter-shift
rule). Output: `barren_log.json`.

Protocol: hardware-efficient random circuits (each layer: a random Pauli
rotation RX/RY/RZ with a random angle on every qubit, then a brickwork layer
of CZ gates), fixed depth 20, qubit counts 2 to 12. For each qubit count, 150
independent random circuit instances; for each, the exact gradient of one
mid-circuit rotation parameter via parameter-shift, measured against two
different cost functions on the same circuits:
- LOCAL: <Z_0>, a single-qubit observable
- GLOBAL: <Z_0 Z_1 ... Z_{n-1}>, the full-system parity

Variance of that gradient across the 150 samples, per qubit count:

| n_qubits | var(local Z0) | var(global parity) |
|---|---|---|
| 2  | 1.127e-01 | 9.770e-02 |
| 4  | 6.609e-02 | 2.979e-02 |
| 6  | 4.504e-02 | 6.457e-03 |
| 8  | 3.682e-02 | 1.815e-03 |
| 10 | 3.316e-02 | 5.236e-04 |
| 12 | 3.250e-02 | 1.013e-04 |

Log-linear fit (log variance vs n_qubits, same fixed depth=20 for every
point):
- global parity: slope -0.6822 -> variance shrinks by a factor of ~0.51 per
  added qubit (965x total from n=2 to n=12)
- local Z0: slope -0.1213 -> variance shrinks by a factor of ~0.89 per added
  qubit (3.5x total from n=2 to n=12) — visibly flattening out, not
  collapsing

## Claim classification

- ESTABLISHED (cited): gradient variance of globally-defined cost functions
  in random parameterized circuits vanishes exponentially with system size —
  McClean, Boixo, Smelyanskiy, Babbush, Neven, "Barren plateaus in quantum
  neural network training landscapes," Nature Communications 9, 4812 (2018),
  https://www.nature.com/articles/s41467-018-07090-4. Cost-function locality
  changes the severity of the effect at fixed shallow depth — Cerezo, Sone,
  Volkoff, Cincio, Coles, "Cost function dependent barren plateaus in
  shallow parametrized quantum circuits," Nature Communications 12, 1791
  (2021), https://www.nature.com/articles/s41467-021-21728-w.
- VERIFIED (this run, artifact attached): the qualitative and rough
  quantitative shape of both results, reproduced from scratch on circuits I
  generated and simulated myself this session, not a canned demo — global
  parity's gradient variance collapses ~965x over the same 10-qubit range
  where the local observable's variance only drops ~3.5x, at identical
  circuit depth. Full data: `barren_log.json`.
- HYPOTHESIS (owner's framing, not fact): whether there exists a general,
  provable characterization of which circuit architectures escape barren
  plateaus at practically useful scale — one that a real quantum computer
  could still exploit for an advantage classical methods can't match — is
  not resolved. Known escapes (specific symmetry-informed ansätze, some
  local-depth constructions such as arXiv:2311.01393) are architecture-by-
  architecture proofs, not a general theory. That gap is the open question
  this piece asks, not an answer this piece claims to give.

## Notes
- No quantum hardware or SDK (Qiskit/PennyLane/Cirq) was used — the
  simulator here is intentionally minimal so every number is traceable to
  the ~150 lines in `barren.py`.
- Qubit range capped at 12 (state vector size 4096) for a session-length
  run; the exponential trend is already unambiguous well before that.
