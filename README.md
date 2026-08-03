# lab

Small experiments, each behind one post: one question, one script, one real
run, raw logs included. Nothing here is a library — it is evidence.

| experiment | question | artifacts |
|---|---|---|
| [barren-plateaus](barren-plateaus/) | why does the training signal of a variational quantum circuit collapse 965x when the cost function is global? | numpy statevector sim, 150 circuits/qubit count, raw gradients |
| [matmul-omega](matmul-omega/) | Strassen's 1969 trick tops out at exponent 2.371 today. Can the true matrix multiplication exponent ever reach 2? | from-scratch numpy Strassen vs naive recursion, correctness-verified, empirical exponent matches theory exactly |
| [double-descent](double-descent/) | why does a model's test error spike 500,000x at exactly the point it can memorize its training data, then vanish one parameter later? | from-scratch numpy random-features regression, minimum-norm solution swept across the interpolation threshold, raw sweep log |

Deep, ongoing research graduates to its own repository.
Earlier standalone experiment: [grokking-silence](https://github.com/abhays02/grokking-silence).
