#!/usr/bin/env python3
"""Smoke-test the publishable visualization HTML pages.

The script starts a local HTTP server, opens each page listed in
``_site-manifest.json`` with Playwright, captures desktop/mobile screenshots,
and reports console errors. It is intentionally a lightweight publication gate,
not a full visual-regression framework.
"""

from __future__ import annotations

import http.server
import json
import socketserver
import sys
import threading
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "_site-manifest.json"
SCREENSHOT_DIR = ROOT / "figures" / "qa-screenshots"
PORT = 0


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def start_server() -> socketserver.TCPServer:
    handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(ROOT), **kwargs)
    server = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def main() -> int:
    try:
      from playwright.sync_api import sync_playwright
    except ImportError:
      print("Playwright is not installed. Install with: python3 -m pip install playwright && python3 -m playwright install chromium", file=sys.stderr)
      return 2

    manifest = json.loads(MANIFEST.read_text())
    pages = [
        {"filename": "index.html"},
        {"filename": "module-emission-propagation.html"},
        {"filename": "module-interferometry-instrumentation.html"},
    ]
    pages.extend(page for page in manifest["pages"] if page.get("status") != "defer")
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    failures: list[str] = []
    warnings: list[str] = []
    server = start_server()
    port = server.server_address[1]
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for page_info in pages:
                filename = page_info["filename"]
                url = f"http://127.0.0.1:{port}/{filename}"
                for label, viewport in {
                    "desktop": {"width": 1280, "height": 800},
                    "mobile": {"width": 375, "height": 667},
                }.items():
                    page = browser.new_page(viewport=viewport)
                    errors: list[str] = []
                    page_errors: list[str] = []
                    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
                    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
                    try:
                        response = page.goto(url, wait_until="networkidle", timeout=15000)
                        if response is None or response.status >= 400:
                            failures.append(f"{filename} [{label}] failed to load: {response.status if response else 'no response'}")
                        title = page.title()
                        if not title:
                            failures.append(f"{filename} [{label}] has no document title")
                        if not page.locator("meta[name='viewport']").count():
                            failures.append(f"{filename} [{label}] missing viewport meta")
                        try:
                            page.wait_for_function(
                                "() => Array.from(document.images).every((image) => image.complete)",
                                timeout=5000,
                            )
                        except Exception:
                            pass
                        broken_images = page.locator("img").evaluate_all(
                            """images => images
                                .filter((image) => image.complete && image.naturalWidth === 0)
                                .map((image) => image.getAttribute('src') || image.currentSrc || '[inline image]')"""
                        )
                        if broken_images:
                            failures.append(f"{filename} [{label}] broken images: {', '.join(broken_images[:5])}")
                        shot = SCREENSHOT_DIR / f"{Path(filename).stem}-{label}.png"
                        try:
                            page.screenshot(path=str(shot), full_page=True)
                        except Exception as full_page_exc:
                            try:
                                page.screenshot(path=str(shot), full_page=False)
                            except Exception as viewport_exc:
                                warnings.append(f"{filename} [{label}] screenshot skipped: {viewport_exc or full_page_exc}")
                        if errors:
                            failures.append(f"{filename} [{label}] console errors: {' | '.join(errors[:3])}")
                        if page_errors:
                            failures.append(f"{filename} [{label}] page errors: {' | '.join(page_errors[:3])}")
                    except Exception as exc:
                        failures.append(f"{filename} [{label}] exception: {exc}")
                    finally:
                        page.close()
            browser.close()
    finally:
        server.shutdown()

    if failures:
        print("QA failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    if warnings:
        print("QA warnings:")
        for warning in warnings:
            print(f"- {warning}")

    print(f"QA passed for {len(pages)} pages. Screenshots written to {SCREENSHOT_DIR}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
