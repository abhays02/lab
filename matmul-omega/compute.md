# compute.md -- matmul-omega

## Established (cited, not computed by this run)
- Strassen's 1969 result: two 2x2 matrices multiply in 7 scalar
  multiplications instead of 8, giving a recursive algorithm with time
  complexity O(n^log2(7)) = O(n^2.807...). Source: V. Strassen, "Gaussian
  elimination is not optimal," Numerische Mathematik 13(4), 354-356 (1969).
- Best known upper bound on the matrix multiplication exponent omega as of
  this run: omega < 2.371339. Source: J. Alman, R. Duan, V. Vassilevska
  Williams, Y. Xu, Z. Xu, R. Zhou, "More Asymmetry Yields Faster Matrix
  Multiplication," arXiv:2404.16349 (SODA 2025).
- The only known lower bound is the trivial omega >= 2 (input and output
  size); whether omega = 2 is achievable remains the central open
  conjecture in this area.

## Verified (computed in this run, artifact attached)
- Implemented two block-recursive matrix multiplication algorithms from
  scratch in numpy (strassen.py in this folder): a naive
  divide-and-conquer version (8 recursive multiplications per split) and
  Strassen's algorithm (7 recursive multiplications per split), both
  sharing an identical recursion structure and leaf case (numpy's dense
  @ below a 32x32 threshold) so the only difference between them is the
  textbook one.
- Correctness: both implementations verified against numpy's own A @ B on
  random matrices at n=64, 128, 256 (allclose, atol=1e-8). See
  matmul_log.json "correctness" field.
- Instrumented every leaf-level multiplication call across n = 64 to 2048
  (doubling), then fit the empirical exponent via least-squares regression
  on log(calls) vs log(n):
  - naive recursion: empirical exponent 3.0000 (theoretical: log2(8) = 3.0)
  - Strassen: empirical exponent 2.8074 (theoretical: log2(7) = 2.8074)
- Wall-clock timing was also recorded (naive vs Strassen, n up to 2048) but
  is noisier and shows only a modest ~1.06x speedup at n=2048 -- Python
  recursion overhead and the leaf threshold (32) dominate at these sizes,
  so the real win only shows up asymptotically.
- Full raw data: matmul_log.json.

## Hypothesis / owner's framing (never asserted as fact)
- None asserted as a research claim in this piece. It does not claim to
  move the exponent -- it demonstrates, with real code, exactly how far
  the established 1969 trick goes (2.807) and names the honest, current,
  unresolved gap down to 2 as the open question.
