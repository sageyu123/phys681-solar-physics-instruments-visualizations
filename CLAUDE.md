# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Teaching visualizations for **Phys 681: Solar Physics and Instruments (Spring 2026, Sijie Yu, NJIT)** — a solar physics, solar radio, and instrumentation course. Each top-level `*.html` is a **standalone single-page interactive visualization** that students open directly in a browser. There is no build step, no package manager, no bundler, and no test suite. Pages are the deliverable.

## Running / previewing

A local static server is required because some pages load sibling `.js` data files (`fasr_calibrators.js`) and ES modules. The `.claude/launch.json` debug config serves `/tmp/viz-serve` on port `8765` via Ruby's `httpd`. For local preview from inside the repo:

```sh
# from the repo root
python3 -m http.server 8765
# then open http://localhost:8765/<page>.html
```

To free port 8765 if it's already bound: `lsof -ti:8765 | xargs kill` (this command is pre-allowed in `.claude/settings.local.json`).

## Data-generation scripts

Two Python helpers pre-compute data that is then embedded into / loaded by HTML pages. Regenerate only when the underlying inputs change.

- `generate-uv-synthesis.py` — precomputes UV-synthesis frames (4 combinations of random/spiral array × snapshot/earth-rotation) and writes the entire self-contained `fourier-synthesis-gallery.html`. Requires `numpy`, `Pillow`. Running it **overwrites** the gallery HTML.
- `_convert_fasr_ecef_to_enu.py` — reads CASA `.cfg` antenna files from a specific absolute path on the author's filesystem (see the script) and prints JS arrays to stdout; the output is hand-pasted into `_fasr_enu_data.js`. Requires `numpy`.

## Repository layout

- **Top-level `*.html`** — the "published" visualizations students use. Titles (see `<title>` tags) map roughly to lecture topics: frequency tuning, ADC demux, corner-turn, delay patterns, fringes/bandwidth, UV synthesis, image reconstruction, aperture illumination / blockage, FASR shadowing, Zeeman, polarization ellipse, radiative transfer, gyro emission, coherent emission, receiver noise.
- **`dev/`** — `*-dev.html` work-in-progress copies of a subset of the published pages. The dev copies and their published counterparts drift independently (they are not kept in sync automatically). When editing, confirm with the user which copy is the intended target; do not propagate changes across the pair unless asked.
- **`figures/`** — static image assets (`<img>`-referenced) used by a few pages.
- **`_fasr_enu_data.js`, `fasr_calibrators.js`** — sibling JS data files loaded via `<script src="./...">` by the FASR pages. Must be served from the same directory as the HTML.
- **Files prefixed with `_` or suffixed `-backup`** — author-internal artifacts (data generators, backup pages). Don't modify unless asked.

## Architecture of a visualization page

Every `*.html` is self-contained: HTML + inline `<style>` + inline `<script>`. Common patterns across the pages:

- **Layout**: a fixed-width dark "control rail" (`~300–330px` left panel with sliders, selectors, preset buttons, formulas) plus a scrollable light "analysis wall" on the right containing plot-first cards. See `beam-pattern-feed-illumination-description.md` for the canonical layout description — the other pages follow the same idiom (styled after a `calwidget_html` frontend: Apple-like toolbar, glass panels, STIX Two Text for math).
- **Rendering**: most pages use plain `<canvas>` 2D contexts for plots and diagrams. Pages with 3D scenes (e.g. `gyro-emission-explorer.html`, `radio_interferometry_fundamentals.html`, `fasr_mutual_coupling_diagnostics.html`, `beam-pattern-feed-illumination.html`) import Three.js as an ES module from `cdn.jsdelivr.net/npm/three@0.168.0`. `delay_pattern_interactive.html` uses KaTeX from the same CDN for formula rendering. No other JS dependencies.
- **CSS variables**: each page defines its own `:root { --panel-bg, --panel-ink, --blue, --teal, --amber, --radius, ... }` palette. Colors and spacing are controlled through these vars — prefer editing the variable over hard-coding new values.
- **Physics/numerics**: each page ships its own model (e.g. the aperture-illumination beam model, PB17 calibrator polynomials, UV-synthesis FFT). Models live inline in `<script>` — there is no shared math library. Keep numeric constants and derived quantities close to where they're used.

## Editing conventions worth knowing

- These are teaching artifacts. Pedagogical clarity (labels, units, regime annotations, sensible defaults) matters as much as numerical correctness. When changing defaults, check that the page still lands in the regime the lecture text expects (e.g. "`Ta ~ 10^3 K` for EOVSA-like settings"; "`1 Jy` on a `10 m` dish ≈ `0.05 K`").
- Because every page is standalone, a fix in one file does not propagate. If the user describes a bug in terms of "the visualization," confirm which HTML file they mean before editing.
- Do not introduce a build step, package.json, or extract shared modules unless explicitly asked — the standalone-HTML constraint is load-bearing (pages are distributed as single files to students).
- For UI changes, the only reliable verification is opening the page in a browser. Static checks won't catch broken interactivity.
