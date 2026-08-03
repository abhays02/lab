# lab

Small experiments, each behind one post: one question, one script, one real
run, raw logs included. Nothing here is a library — it is evidence.

| experiment | question | artifacts |
|---|---|---|
| [barren-plateaus](barren-plateaus/) | why does the training signal of a variational quantum circuit collapse 965x when the cost function is global? | numpy statevector sim, 150 circuits/qubit count, raw gradients |
| [matmul-omega](matmul-omega/) | Strassen's 1969 trick tops out at exponent 2.371 today. Can the true matrix multiplication exponent ever reach 2? | from-scratch numpy Strassen vs naive recursion, correctness-verified, empirical exponent matches theory exactly |

Deep, ongoing research graduates to its own repository.
Earlier standalone experiment: [grokking-silence](https://github.com/abhays02/grokking-silence).
