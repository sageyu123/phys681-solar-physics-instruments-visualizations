# NJIT PHYS 681 Spring 2026: Solar Physics and Instruments Teaching Visualizations

This directory contains a publishable static subset of the NJIT PHYS 681 Spring 2026 Solar Physics and Instruments teaching
materials: interactive HTML visualizations, narrative notes, screenshots, and publication metadata
for solar physics, emission, propagation, interferometry, and instrumentation topics.

## Entry Points

- Live site: <https://sageyu123.github.io/phys681-solar-physics-instruments-visualizations/>
- `index.html` opens the teaching-site landing page.
- `module-emission-propagation.html` lists emission, transfer, propagation, and coherent-radiation materials.
- `module-interferometry-instrumentation.html` lists radio interferometry and instrumentation materials.
- `_site-manifest.json` is the source of truth for the publishable pages, module assignments, release level, and learning goals.

## Publication Model

The intended live version is GitHub Pages. The archival version is published on Zenodo.
Use the collection DOI for normal citation of the evolving teaching resource, and use the
version DOI when citing the exact v1.0.0 archived files:

- Collection DOI: `10.5281/zenodo.20820901`
- Version v1.0.0 DOI: `10.5281/zenodo.20820902`
- Version v1.0.0 record: <https://zenodo.org/records/20820902>

Zenodo's collection DOI resolves to the latest version in the version set.

The visualizations are static files. They should open from GitHub Pages and from an archived
release without a custom server.

## Quality Standard

Core pages are flagship teaching materials and should pass the full review standard:
consistent navigation, metadata, clear control labels and units, visible assumptions, responsive
layout, accessible canvas/SVG summaries, no console errors, and science red-team review.

Supplemental pages are publishable supporting materials and should pass the minimum standard:
navigation, metadata, visible labels/units, desktop rendering, no console errors, and a visible
regime or assumptions statement where relevant.

## Local Use

After downloading and unzipping the archive, open `index.html` in a browser. No local server is
required for normal use.

If a browser or institutional security setting blocks local files, serve the directory with:

```sh
python3 -m http.server 8765
```

Then open `http://localhost:8765/index.html`.

## Render Narrative Notes

From the repository root:

```sh
quarto render visualizations/emission-mechanism-explorer-narratives.qmd --to html
```

From this `visualizations/` directory:

```sh
quarto render emission-mechanism-explorer-narratives.qmd --to html
```
