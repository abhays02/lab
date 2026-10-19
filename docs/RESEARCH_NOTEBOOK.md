# Lab notebook

[← Repository overview](../README.md) · [Interactive lab ↗](https://abhays02.github.io/lab/) · [Windows releases](https://github.com/abhays02/lab/releases)

## Six experiments, one visual language

Every experiment is organized around the same questions:

```text
WHAT IS THE QUESTION?
        ↓
WHAT DID WE RUN?
        ↓
WHAT CAME OUT?
        ↓
WHAT DOES IT MEAN?
        ↓
WHAT IS ACTUALLY VERIFIED?
        ↓
WHERE IS THE EVIDENCE?
```

| # | Experiment | Core question | Main measured result |
|---|---|---|---|
| 01 | [Barren plateaus](../barren-plateaus/) | Does the training signal survive as qubits increase? | Global gradient variance: `0.0977 → 0.000101` |
| 02 | [Double descent](../double-descent/) | What happens at the interpolation threshold? | Test MSE: `238,807 → 32.9` from `p=100 → 101` |
| 03 | [Colibri / GLM](../colibri-glm/) | How much of a huge model is active per token? | `5.38%` active; about `11 GB` implied cold-token reads, checked arithmetically from published figures |
| 04 | [Sorting networks](../sorting-network-depth/) | Can a correct network still be too deep? | `10` rounds vs proven optimum `9` at `n=16` |
| 05 | [Quantum advantage boundary](../quantum-advantage-boundary/) | Why does exact simulation hit a memory wall? | `144.12 PB` for a 53-qubit complex128 statevector |
| 06 | [Emergence mirage](../emergence-mirage/) | Can a metric make a smooth curve look discontinuous? | Exact-match crossing shifts and sharpens as `k` grows |

## How to read the evidence

```text
VISUAL
  ↓
MEASUREMENT
  ↓
CODE
  ↓
RAW OUTPUT
  ↓
PROVENANCE
```

| Label | Meaning |
|---|---|
| **Established** | Known before this run. |
| **Verified here** | Independently computed in this repo. |
| **Not claimed** | Not presented as a new discovery. |

The purpose of the notebook is not to make every experiment sound novel.

It is to make the **actual evidence easy to inspect**.

## Publishing and distribution

### Preview the website

From the repository root, run `python3 scripts/build_site.py`, then
`python3 scripts/desktop.py`. The launcher opens the assembled site in your
default browser, bound only to `127.0.0.1` on an available port. Stop it with
Ctrl+C. No JavaScript packages, CDN, or model downloads are needed.

`site/` owns the interactive experience. Experiment folders own their detailed
READMEs, code, raw results, and provenance. The build copies only the website,
public evidence assets, and research files into `dist/site`; it does not
publish the repository's Git metadata, workflows, or local environment.
Historical standalone HTML explainers remain in the repository; the site
uses the self-contained evidence previews instead.

### GitHub Pages

1. In **Settings → Pages → Build and deployment**, set **Source** to
   **GitHub Actions**.
2. Merge the website changes into `main`. The **Publish research explorer**
   workflow builds the site and deploys it separately from Windows releases.
   You can also run it from the **Actions** tab.
3. Check the deployment job and open its environment URL. The default address
   is `https://abhays02.github.io/lab/`.

Pull requests build and smoke-test the bundle without deploying it. The
deployment requires repository Pages permissions; a successful local build
does not mean the public website has already been deployed.

### Optional docs subdomain

Do this only for a hostname you own; there is intentionally no placeholder
`CNAME` in this repository.

1. Verify domain ownership in your account's **Settings → Pages** using the
   GitHub-provided DNS TXT record.
2. In your DNS provider, create a `CNAME` for your chosen subdomain (for
   example, `docs`) pointing to **`abhays02.github.io`**, without `https://`
   or `/lab`.
3. In this repository's **Settings → Pages → Custom domain**, enter your
   actual hostname, save it, wait for the DNS check and certificate, and
   enable **Enforce HTTPS**.
4. Update the public explorer links in the root README, experiment READMEs,
   this notebook, and `site/` to your verified hostname.
5. Re-run the publishing workflow and verify links on both desktop and mobile.

DNS and repository settings require owner access and are not changed by the
site build. See [GitHub's custom-domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

### Windows executable

The Windows download is an **offline research explorer**, not a replacement
for the Python experiments. It bundles the same website and recorded
evidence, serves them on a loopback port, and opens your existing browser.
Source/provenance links on GitHub still require internet access.

- **Try a build:** run **Build Windows explorer** manually in Actions.
  Download the `Lab-Explorer-windows-x64` artifact after it passes.
- **Publish a release:** after reviewing and merging, push a version tag
  such as `v1.0.0`. The workflow builds on Windows, runs the executable's
  smoke test, and uploads `Lab-Explorer.exe` and `SHA256SUMS.txt` to the
  matching GitHub Release. Only the release job has repository write access.
- **Verify:** use PowerShell's `Get-FileHash .\Lab-Explorer.exe -Algorithm SHA256`
  and compare with `SHA256SUMS.txt` from that release.
- **Run:** double-click the executable and keep its console open. Press
  Ctrl+C in the console when finished. It uses an available local port and
  does not need an administrator account or Python installation.

The build targets Windows x64 and is unsigned. SmartScreen may warn about a
new publisher; inspect the release and checksum rather than disabling system
protection. A checksum checks download integrity, not publisher identity.
Building locally requires Windows, Python 3.12, and `pyinstaller==6.16.0`:

```powershell
python -m pip install pyinstaller==6.16.0
python scripts/build_site.py
python -m PyInstaller --clean --noconfirm --onefile --console --name Lab-Explorer --add-data "dist/site:site" scripts/desktop.py
.\dist\Lab-Explorer.exe --smoke-test
```

PyInstaller cannot cross-compile a Windows executable on Linux. The Windows
workflow must finish successfully before a Windows binary can be described
as built and tested.
