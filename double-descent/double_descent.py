"""
Minimal reproduction of double descent via random-Fourier-features
regression, in the spirit of Belkin, Hsu & Xu (2019) and Mei & Montanari
(2019). Pure numpy, no sklearn, no torch.

Ground truth: y = x . beta + noise, x in R^d.
We never give the learner beta or d. Instead we fit a linear model on top
of p random Fourier features z = cos(W x + b), sweeping p from far below
the number of training points n to far above it, and always solving with
the minimum-norm least-squares solution (np.linalg.pinv), exactly as an
interpolating learner would.

Reported quantity: held-out test MSE as a function of p.
"""
import json

import numpy as np

RNG = np.random.default_rng(0)

D_TRUE = 20            # dimensionality of the true signal
N_TRAIN = 100           # fixed training set size (the interpolation threshold)
N_TEST = 2000
NOISE_STD = 0.5
FEATURE_COUNTS = [5, 10, 20, 40, 60, 80, 95, 99, 100, 101, 105, 110,
                   120, 140, 160, 200, 260, 340, 450, 600, 800, 1100, 1500, 2000]
N_TRIALS = 30           # average over this many resamples of noise + features


def make_data(n, beta, rng):
    x = rng.standard_normal((n, D_TRUE))
    y = x @ beta + NOISE_STD * rng.standard_normal(n)
    return x, y


def random_fourier_features(x, w, b):
    return np.cos(x @ w.T + b)


def run_trial(p, rng):
    beta = rng.standard_normal(D_TRUE)
    beta /= np.linalg.norm(beta)

    x_train, y_train = make_data(N_TRAIN, beta, rng)
    x_test, y_test = make_data(N_TEST, beta, rng)

    w = rng.standard_normal((p, D_TRUE)) / np.sqrt(D_TRUE)
    b = rng.uniform(0, 2 * np.pi, size=p)

    z_train = random_fourier_features(x_train, w, b)
    z_test = random_fourier_features(x_test, w, b)

    # Minimum-norm least-squares solution, whatever the regime.
    coef, *_ = np.linalg.lstsq(z_train, y_train, rcond=None)

    train_pred = z_train @ coef
    test_pred = z_test @ coef

    train_mse = float(np.mean((train_pred - y_train) ** 2))
    test_mse = float(np.mean((test_pred - y_test) ** 2))
    return train_mse, test_mse


def main():
    results = []
    for p in FEATURE_COUNTS:
        train_errs, test_errs = [], []
        for trial in range(N_TRIALS):
            rng = np.random.default_rng(1000 * p + trial)
            train_mse, test_mse = run_trial(p, rng)
            train_errs.append(train_mse)
            test_errs.append(test_mse)
        row = {
            "p": p,
            "p_over_n": round(p / N_TRAIN, 3),
            "train_mse_mean": float(np.mean(train_errs)),
            "test_mse_mean": float(np.mean(test_errs)),
            "test_mse_median": float(np.median(test_errs)),
        }
        results.append(row)
        print(f"p={p:5d}  p/n={row['p_over_n']:.2f}  "
              f"train_mse={row['train_mse_mean']:.4f}  "
              f"test_mse={row['test_mse_mean']:.4f}")

    peak = max(results, key=lambda r: r["test_mse_mean"])
    far_underparam = results[0]
    far_overparam = results[-1]
    at_n = min(results, key=lambda r: abs(r["p"] - N_TRAIN))

    summary = {
        "n_train": N_TRAIN,
        "d_true": D_TRUE,
        "noise_std": NOISE_STD,
        "n_trials_per_p": N_TRIALS,
        "results": results,
        "peak": peak,
        "far_underparam_p5": far_underparam,
        "far_overparam_p2000": far_overparam,
        "closest_to_interpolation_threshold": at_n,
        "peak_to_overparam_ratio": peak["test_mse_mean"] / far_overparam["test_mse_mean"],
        "peak_to_underparam_ratio": peak["test_mse_mean"] / far_underparam["test_mse_mean"],
    }

    with open("double_descent_log.json", "w") as f:
        json.dump(summary, f, indent=2)

    print()
    print(f"peak test MSE at p={peak['p']} (p/n={peak['p_over_n']}): {peak['test_mse_mean']:.4f}")
    print(f"test MSE at p=5 (far underparameterized): {far_underparam['test_mse_mean']:.4f}")
    print(f"test MSE at p=2000 (far overparameterized): {far_overparam['test_mse_mean']:.4f}")
    print(f"peak / far-overparameterized ratio: {summary['peak_to_overparam_ratio']:.1f}x")
    print(f"peak / far-underparameterized ratio: {summary['peak_to_underparam_ratio']:.1f}x")


if __name__ == "__main__":
    main()
