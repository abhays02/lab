# lab

Small experiments, each behind one post: one question, one script, one real
run, raw logs included. Nothing here is a library — it is evidence.

| experiment | question | artifacts |
|---|---|---|
| [barren-plateaus](barren-plateaus/) | why does the training signal of a variational quantum circuit collapse 965x when the cost function is global? | numpy statevector sim, 150 circuits/qubit count, raw gradients |
| [matmul-omega](matmul-omega/) | Strassen's 1969 trick tops out at exponent 2.371 today. Can the true matrix multiplication exponent ever reach 2? | from-scratch numpy Strassen vs naive recursion, correctness-verified, empirical exponent matches theory exactly |
| [double-descent](double-descent/) | why does a model's test error spike 500,000x at exactly the point it can memorize its training data, then vanish one parameter later? | from-scratch numpy random-features regression, minimum-norm solution swept across the interpolation threshold, raw sweep log |
| [colibri-glm](colibri-glm/) | a 744B-parameter model just ran on a laptop by streaming 94.6% of itself from an SSD. Why is the achieved read speed still 3-13x under the drive's own rated spec? | arithmetic validation of the published Colibri/GLM-5.2 numbers, checked for internal consistency against known MoE routing math |
| [sorting-network-depth](sorting-network-depth/) | the exact minimum number of parallel comparison rounds to sort n numbers is proven up to n=17. why does even the textbook 1968 construction still miss that minimum, and why is the record past n=17 still moving? | from-scratch Batcher's bitonic network, correctness verified via brute-force 0-1 principle up to n=16, cross-checked against proven-optimal depths and the Nov 2025 arXiv record for 27/28 channels |

Deep, ongoing research graduates to its own repository.
Earlier standalone experiment: [grokking-silence](https://github.com/abhays02/grokking-silence).
