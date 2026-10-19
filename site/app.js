(() => {
  "use strict";
  const experiments = [
    {
      id: "barren-plateaus", title: "Barren plateaus", category: "quantum", label: "Quantum / Training signal", summary: "When the gradient goes quiet",
      question: "Does the training signal survive as a quantum circuit gets wider?",
      stat: "965×", statLabel: "lower global gradient variance, from 2 to 12 qubits",
      steps: [
        ["A wider circuit. A quieter signal?", "Keep the circuit family, depth, and differentiated parameter fixed. Increase only the number of qubits, then compare a local readout ⟨Z₀⟩ with a global parity readout."],
        ["Hold the experiment still.", "A NumPy statevector simulator evaluates exact parameter-shift gradients for 150 random hardware-efficient circuits at each of six widths: 2, 4, 6, 8, 10, and 12 qubits. Circuit depth stays at 20."],
        ["The objective changes the outcome.", "Local gradient variance falls from 0.1127 to 0.0325, about 3.5×. Global variance falls from 0.0977 to 0.000101, about 965×. The global objective loses signal much faster in this run."]
      ],
      boundary: "Barren-plateau suppression is established. This run independently checks the local/global contrast; it does not introduce a new theorem or optimizer.",
      caption: "Six recorded values per objective. Logarithmic variance axis; connecting lines are visual guides, not additional measurements.",
      alt: "Recorded gradient variance decreases with qubit count, much faster for the global objective than for the local objective.",
      script: "barren.py", raw: "barren_log.json"
    },
    {
      id: "double-descent", title: "Double descent", category: "learning", label: "Learning / Interpolation", summary: "One feature changes the picture",
      question: "Why can adding one more feature make test error collapse?",
      stat: "238,807 → 32.9", statLabel: "mean test MSE at 100 versus 101 features",
      steps: [
        ["More capacity, worse predictions?", "Fitting the training data perfectly is not the same as predicting well. Explore what happens near the interpolation threshold, where feature count matches the 100 training points."],
        ["Sweep across the threshold.", "Fit random Fourier features with minimum-norm least squares. The checked-in sweep covers 24 feature counts from 5 to 2,000, with 30 trials per feature count."],
        ["A spike, then a second descent.", "Mean test MSE reaches 238,807 at 100 features, then falls to 32.9 at 101. At 2,000 features it reaches 0.464. These are the recorded sweep means, not a guarantee for every dataset."]
      ],
      boundary: "Double descent is established in prior work. This experiment verifies one specific sweep, not a new theory or a universal benefit of adding parameters.",
      caption: "Recorded sweep means; the full 24-point, 30-trial sweep is in the raw log. Lines only guide the eye.",
      alt: "Mean test error peaks at 100 features before falling sharply at 101 features and further at 2,000.",
      script: "double_descent.py", raw: "double_descent_log.json"
    },
    {
      id: "colibri-glm", title: "Colibri / GLM", category: "systems", label: "Systems / Storage arithmetic", summary: "The model is large. The active part isn’t.",
      question: "How much of a 744B-parameter model is active for each token?",
      stat: "5.38%", statLabel: "active parameters per token, from published figures",
      steps: [
        ["Think beyond parameter count.", "Published architecture figures describe 744B total parameters and 40B active per token. The question is not only how much a model stores, but how much must move for each token."],
        ["Check the arithmetic, not the model.", "Divide active by total parameters, infer about 7.9 experts per layer, and estimate about 11.13 GB of cold-token expert reads. Combine that estimate with the published 0.05–0.1 tokens/s rate."],
        ["An implied storage constraint.", "The arithmetic gives 5.38% active parameters and roughly 0.55–1.1 GB/s effective reads. This is internally consistent with the published inputs. It is not a measurement of the implementation."]
      ],
      boundary: "No 372 GB model was run or benchmarked here. Read volume and throughput are arithmetic estimates from published inputs, not a diagnosis of a storage bottleneck.",
      caption: "Schematic proportions from published architecture: 40B active out of 744B total. Read-volume estimates are not benchmark measurements.",
      alt: "A proportion bar shows 5.38 percent active parameters and 94.62 percent inactive parameters per token.",
      script: "colibri_math.py", raw: "colibri_math.json"
    },
    {
      id: "sorting-network-depth", title: "Sorting network depth", category: "systems", label: "Systems / Parallel algorithms", summary: "Correct doesn’t mean optimal",
      question: "Can a sorting network be correct and still take too many parallel rounds?",
      stat: "10 vs 9", statLabel: "Batcher’s depth versus the proven optimum at n = 16",
      steps: [
        ["Two different questions.", "Does the network sort every input? And does it use the fewest possible parallel rounds? Correctness alone cannot answer the second question."],
        ["Turn correctness into a finite check.", "Build Batcher’s network, count comparators and parallel layers, then apply the 0/1 principle. At 16 inputs the verifier checks all 65,536 binary inputs; exhaustive checks cover sizes through 16."],
        ["Correct, with a round to spare.", "At 16 inputs, the construction has 80 comparators, 10 layers, and zero binary counterexamples. The established optimum is 9 layers. That optimum comes from prior work, not this verifier."]
      ],
      boundary: "No new optimal network is claimed. The verifier checks Batcher’s construction; the nine-round optimum is an established comparison. Best known does not always mean proven optimal.",
      caption: "Depth-only schematic at 16 inputs. Each block is one parallel round, not a comparator layout. The nine-layer optimum is from prior work.",
      alt: "Ten blocks for Batcher’s depth compared with nine blocks for the proven optimal depth at sixteen inputs.",
      script: "batcher_verify.py", raw: "batcher_results.json"
    },
    {
      id: "quantum-advantage-boundary", title: "Quantum advantage boundary", category: "quantum", label: "Quantum / Simulation limits", summary: "An exponential memory wall",
      question: "Why does exact full-state simulation run out of room so quickly?",
      stat: "144.12 PB", statLabel: "exact complex128 statevector storage at 53 qubits",
      steps: [
        ["One more qubit. Twice the storage.", "An exact statevector stores 2ⁿ complex amplitudes. With 16 bytes per complex128 amplitude, storage doubles for each added qubit, even before accounting for simulation overhead."],
        ["Separate the calculation from the run.", "The memory curve is exact arithmetic, 16 × 2ⁿ bytes. Separately, the repository simulates 14-qubit random circuits, using six circuit instances and 98,304 pooled values per depth."],
        ["A wall, not an advantage proof.", "53-qubit state storage is 144.12 PB in decimal units; it was not allocated. In the recorded depth sweep, the KS statistic decreases from 0.1225 at 9 layers to 0.00264 at 40, approaching the Porter–Thomas reference."]
      ],
      boundary: "The 53-qubit figure is storage arithmetic, not a 53-qubit simulation or a new quantum-advantage claim. Other classical methods can avoid storing a full statevector.",
      caption: "Exact storage arithmetic in decimal units, on a logarithmic axis. The separate simulated circuit uses 14 qubits, not 53.",
      alt: "Statevector memory grows exponentially from 16.38 kilobytes at ten qubits to 144.12 petabytes at fifty-three.",
      script: "rcs_verify.py", raw: "rcs_results.json"
    },
    {
      id: "emergence-mirage", title: "Emergence mirage", category: "learning", label: "Learning / The measurement lens", summary: "Same curve. A sharper story.",
      question: "Can a scoring rule make smooth capability look like a sudden breakthrough?",
      stat: "99.31%", statLabel: "per-token accuracy needed for 50% exact match over 100 steps",
      steps: [
        ["Change the lens, not the capability.", "Start with one smooth logistic capability curve p(x). Score success as getting every step right: p(x)ᵏ. Only the number of required steps changes."],
        ["A synthetic, deterministic calculation.", "No model is trained and no external data is used. Calculate exact-match thresholds for k = 1, 5, 20, 50, and 100 while keeping the underlying capability function fixed."],
        ["The apparent threshold moves.", "For one step, 50% per-token accuracy gives 50% exact match. For 100 steps, 99.31% is needed. The apparent crossing moves from x = 5.00 to 9.14; the scoring rule makes the transition look sharper."]
      ],
      boundary: "This known metric-artifact mechanism is independently checked here. It does not show that all real-world emergent abilities are artifacts of evaluation.",
      caption: "Computed 50% exact-match thresholds for five step counts. The x coordinate is a synthetic logistic input, not measured model scale.",
      alt: "As required correct steps rise from one to one hundred, the synthetic fifty-percent crossing shifts from five to 9.14.",
      script: "emergence_mirage.py", raw: "emergence_results.json"
    }
  ];
  const $ = (id) => document.getElementById(id);
  const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  let paused = mediaQuery.matches;
  let playing = false;
  let selected = experiments.find(e => e.id === location.hash.slice(1)) || experiments[0];
  let step = 0;
  let filter = "all";
  function stopPlayback() {
    playing = false;
    $("animated-visual").hidden = true;
    $("animated-visual").removeAttribute("src");
    $("static-visual").hidden = false;
    $("play-toggle").textContent = "▷ Play animation";
    $("play-toggle").setAttribute("aria-pressed", "false");
    $("visual-title").textContent = "OBSERVATION / STATIC VIEW";
  }
  function renderStep(index) {
    step = index;
    const tabs = [...document.querySelectorAll("[data-step]")];
    tabs.forEach((tab, i) => {
      tab.setAttribute("aria-selected", String(i === step));
      tab.tabIndex = i === step ? 0 : -1;
    });
    $("step-panel").setAttribute("aria-labelledby", tabs[step].id);
    const [heading, body] = selected.steps[step];
    $("step-panel").replaceChildren();
    const title = document.createElement("h4"), paragraph = document.createElement("p");
    title.textContent = heading;
    paragraph.textContent = body;
    $("step-panel").append(title, paragraph);
  }
  function renderList() {
    const visible = experiments.filter(e => filter === "all" || e.category === filter);
    $("experiment-list").replaceChildren();
    visible.forEach(e => {
      const index = experiments.indexOf(e) + 1, button = document.createElement("button");
      button.className = `experiment-option${e === selected ? " selected" : ""}`;
      button.id = e.id;
      button.setAttribute("aria-pressed", String(e === selected));
      button.setAttribute("aria-controls", "experiment-detail");
      button.innerHTML = `<span class="experiment-number">0${index}</span><span><span class="option-title">${e.title}</span><span class="option-summary">${e.summary}</span></span><span class="option-arrow" aria-hidden="true">↗</span>`;
      button.addEventListener("click", () => {
        select(e);
        history.replaceState(null, "", `#${e.id}`);
        // Keep keyboard focus on the newly rendered selection control.
        [...$("experiment-list").children][visible.indexOf(e)].focus({ preventScroll: true });
      });
      $("experiment-list").append(button);
    });
    $("result-count").textContent = `${visible.length} experiments`;
  }
  function select(e) {
    selected = e;
    stopPlayback();
    $("detail-category").textContent = e.label.toUpperCase();
    $("detail-index").textContent = `EXPERIMENT 0${experiments.indexOf(e) + 1} / 06`;
    $("detail-title").textContent = e.title;
    $("detail-question").textContent = e.question;
    $("detail-stat").textContent = e.stat;
    $("detail-stat-label").textContent = e.statLabel;
    $("detail-boundary").textContent = e.boundary;
    $("visual-caption").textContent = e.caption;
    $("animated-visual").alt = e.alt;
    $("static-visual").alt = e.alt;
    $("static-visual").src = `./${e.id}/evidence-still.png`;
    $("evidence-links").replaceChildren();
    [["Overview", "README.md"], ["Code", e.script], ["Raw JSON", e.raw], ["Provenance", "compute.md"]].forEach(([label, file], i) => {
      const link = document.createElement("a");
      link.href = `https://github.com/abhays02/lab/blob/main/${e.id}/${file}`;
      link.setAttribute("aria-label", `${e.title}: ${label} on GitHub`);
      link.innerHTML = `${label}<span aria-hidden="true">${i + 1 < 10 ? "0" : ""}${i + 1} ↗</span>`;
      $("evidence-links").append(link);
    });
    renderStep(0);
    renderList();
    $("selection-status").textContent = `Selected ${e.title}. ${e.stat}: ${e.statLabel}.`;
  }
  function updateMotion() {
    document.documentElement.classList.toggle("motion-paused", paused);
    $("motion-toggle").setAttribute("aria-pressed", String(paused));
    $("motion-toggle").innerHTML = paused ? '<span aria-hidden="true">▷</span> Resume motion' : '<span aria-hidden="true">Ⅱ</span> Pause motion';
    $("play-toggle").disabled = paused;
    $("play-toggle").title = paused ? "Resume global motion to enable animated visuals." : "Play the checked-in animated explainer.";
    if (paused) stopPlayback();
  }
  $("motion-toggle").addEventListener("click", () => { paused = !paused; updateMotion(); });
  mediaQuery.addEventListener("change", event => { paused = event.matches; updateMotion(); });
  $("play-toggle").addEventListener("click", () => {
    if (paused) return;
    if (playing) return stopPlayback();
    playing = true;
    $("animated-visual").src = `./${selected.id}/animation.gif`;
    $("animated-visual").hidden = false;
    $("static-visual").hidden = true;
    $("play-toggle").textContent = "■ Stop animation";
    $("play-toggle").setAttribute("aria-pressed", "true");
    $("visual-title").textContent = "OBSERVATION / ANIMATED VIEW";
  });
  $("animated-visual").addEventListener("error", () => {
    stopPlayback();
    $("selection-status").textContent = "Animation could not load. The static evidence view remains available.";
  });
  document.querySelectorAll("[data-filter]").forEach(button => button.addEventListener("click", () => {
    filter = button.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach(item => {
      item.classList.toggle("active", item === button);
      item.setAttribute("aria-pressed", String(item === button));
    });
    const visible = experiments.filter(e => filter === "all" || e.category === filter);
    if (!visible.includes(selected)) {
      select(visible[0]);
      if (!["#experiments", "#approach"].includes(location.hash)) {
        history.replaceState(null, "", `#${selected.id}`);
      }
    } else renderList();
  }));
  document.querySelectorAll("[data-step]").forEach(tab => {
    tab.addEventListener("click", () => renderStep(Number(tab.dataset.step)));
    tab.addEventListener("keydown", event => {
      let next;
      if (event.key === "ArrowRight") next = (step + 1) % 3;
      if (event.key === "ArrowLeft") next = (step + 2) % 3;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = 2;
      if (next !== undefined) {
        event.preventDefault();
        renderStep(next);
        document.querySelector(`[data-step="${next}"]`).focus();
      }
    });
  });
  window.addEventListener("hashchange", () => {
    const match = experiments.find(e => e.id === location.hash.slice(1));
    if (match) {
      if (filter !== "all" && filter !== match.category) document.querySelector('[data-filter="all"]').click();
      select(match);
      $("experiment-detail").scrollIntoView({ block: "start" });
    }
  });
  select(selected);
  updateMotion();
  if (experiments.some(e => e.id === location.hash.slice(1))) {
    requestAnimationFrame(() => $("experiment-detail").scrollIntoView({ block: "start", behavior: "instant" }));
  }
})();
