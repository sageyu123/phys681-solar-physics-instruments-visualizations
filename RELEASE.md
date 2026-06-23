# Release Checklist

Use this checklist before creating a DOI-citable release.

1. Confirm `_site-manifest.json` includes every publishable page and excludes dev, backup, and planning files.
2. Render the narrative HTML:

   ```sh
   quarto render emission-mechanism-explorer-narratives.qmd --to html
   ```

3. Preview locally:

   ```sh
   python3 -m http.server 8765
   ```

4. Open `index.html`, both module pages, and all Core pages.
5. Run the QA script once Playwright is installed:

   ```sh
   python3 tools/qa/playwright_qa.py
   ```

6. Build the static release-candidate copy and Zenodo upload archive:

   ```sh
   python3 tools/release/build_dist.py
   ```

7. Preview `dist/index.html` through a local server and confirm no broken internal links.
8. Inspect `dist/DEPOSIT_CONTENTS.md` and confirm the package includes only publishable materials.
9. Upload `zenodo-package/phys681-solar-physics-instruments-teaching-visualizations-<version>.zip` for manual Zenodo deposition. If using GitHub-Zenodo integration instead, first confirm that the tagged repository archive does not include dev, backup, planning, or generated local files.
10. Update `CITATION.cff`, `.zenodo.json`, `_site-manifest.json`, and this checklist with the final version/date.
