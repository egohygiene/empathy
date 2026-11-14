# Copyright 2026 Ego Hygiene
# SPDX-License-Identifier: MIT

"""Opt-in real Chromium/axe checks over a disposable, unchanged HTTPS site."""

from __future__ import annotations

import argparse
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import shutil
import ssl
import sys
import threading
from typing import Any

from playwright.sync_api import sync_playwright

AXE_SHA256 = "e9e5863c33a874f09bc01acd9234b7e3c871479f5eef8802fa582544465e6d01"
ORIGIN = "https://127.0.0.1:9443"
ROUTES = ("/", "/docs/", "/architecture/", "/legal/", "/legal/attribution/", "/docs/localization/")
VIEWPORTS = ((390, 844), (768, 1024), (1440, 1000))
FACTS = """() => ({
lang:document.documentElement.lang,title:document.title,
h1:document.querySelectorAll('h1').length,main:document.querySelectorAll('main').length,
canonical:document.querySelector('link[rel=canonical]')?.href,
description:document.querySelector('meta[name=description]')?.content,
overflow:document.documentElement.scrollWidth>innerWidth+1,
reduced:matchMedia('(prefers-reduced-motion: reduce)').matches,
accent:getComputedStyle(document.documentElement).getPropertyValue('--identity-color-accent').trim(),
text:document.body.innerText})"""


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, _format: str, *_args: object) -> None:
        """Keep temporary TLS paths and ordinary requests out of public receipts."""


def inventory(root: Path) -> dict[str, str]:
    """Hash every real published file before and after browser inspection."""
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def tls_context(certificate: Path, private_key: Path) -> ssl.SSLContext:
    """Create the fixture server context with TLS 1.2 as its minimum."""
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(certificate, private_key)
    return context


def check_skip_link(page: Any) -> dict[str, bool]:
    """Wait for the browser's actual keyboard navigation before judging its URL."""
    page.keyboard.press("Tab")
    focused = "Skip to content" in page.evaluate("document.activeElement.textContent")
    page.keyboard.press("Enter")
    page.wait_for_url(re.compile(r".*#(?:main-content|content)$"), timeout=5000)
    return {
        "keyboard_skip_link": focused,
        "keyboard_skip_destination": page.url.endswith("#main-content") or "#content" in page.url,
    }


def inspect(args: argparse.Namespace) -> dict[str, Any]:
    """Exercise actual generated DOM and the pinned automatic accessibility engine."""
    before = inventory(args.site_root)
    tokens = (args.site_root / "assets/identity/tokens.css").read_text(encoding="utf-8")
    accent = re.search(r"--identity-color-action-primary:\s*([^;]+);", tokens)
    if accent is None or hashlib.sha256(args.axe_script.read_bytes()).hexdigest() != AXE_SHA256:
        message = "Use the expected Identity token input and pinned axe4.11.0 script digest."
        raise ValueError(message)
    server = ThreadingHTTPServer(
        ("127.0.0.1", 9443), partial(QuietHandler, directory=str(args.site_root))
    )
    tls = tls_context(args.certificate, args.private_key)
    server.socket = tls.wrap_socket(server.socket, server_side=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    requests: list[dict[str, Any]] = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                executable_path=shutil.which("chromium"), headless=True
            )
            for width, height in VIEWPORTS:
                for scheme in ("light", "dark"):
                    context = browser.new_context(
                        ignore_https_errors=True,
                        viewport={"width": width, "height": height},
                        color_scheme=scheme,
                        reduced_motion="reduce",
                    )
                    page = context.new_page()
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.on(
                        "requestfailed",
                        lambda request: requests.append(
                            {"url": request.url, "failure": request.failure}
                        ),
                    )
                    page.on(
                        "response",
                        lambda response: (
                            requests.append({"url": response.url, "status": response.status})
                            if response.status >= 400
                            else None
                        ),
                    )
                    for route in ROUTES:
                        response = page.goto(ORIGIN + route, wait_until="networkidle")
                        page.add_script_tag(path=str(args.axe_script))
                        axe = page.evaluate(
                            "async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})"
                        )
                        facts = page.evaluate(FACTS)
                        checks = {
                            "http_200": response is not None and response.status == 200,
                            "semantic_document": facts["lang"] == "en"
                            and facts["h1"] == 1
                            and facts["main"] == 1,
                            "metadata": bool(facts["title"] and facts["description"])
                            and facts["canonical"] == ORIGIN + route,
                            "responsive": not facts["overflow"],
                            "reduced_motion": facts["reduced"],
                            "identity_accent": facts["accent"] == accent[1].strip(),
                        }
                        if route == "/":
                            checks.update(check_skip_link(page))
                            page.screenshot(
                                path=str(
                                    args.output.with_name(f"{args.variant}-{width}-{scheme}.png")
                                ),
                                full_page=True,
                            )
                        if route == "/legal/attribution/":
                            checks["attribution"] = (
                                "Made with love by Ego Hygiene." in facts["text"]
                            )
                        if route == "/docs/localization/":
                            checks["unicode_content"] = all(
                                text in facts["text"] for text in ("café", "ようこそ", "مرحبا")
                            )
                        violations = [
                            {"id": v["id"], "impact": v["impact"], "nodes": len(v["nodes"])}
                            for v in axe["violations"]
                        ]
                        rows.append(
                            {
                                "route": route,
                                "viewport": {"width": width, "height": height},
                                "color_scheme": scheme,
                                "checks": checks,
                                "axe_violations": violations,
                                "axe_pass_rules": len(axe["passes"]),
                                "axe_incomplete_rules": len(axe["incomplete"]),
                            }
                        )
                    context.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
    unchanged = before == inventory(args.site_root)
    passed = (
        unchanged
        and not errors
        and not requests
        and all(all(r["checks"].values()) and not r["axe_violations"] for r in rows)
    )
    return {
        "schema": "empathy.website-browser/v1",
        "result": "PASS" if passed else "FAIL",
        "variant": args.variant,
        "browser": browser.version,
        "axe": "4.11.0",
        "axe_js_sha256": AXE_SHA256,
        "artifact_unchanged": unchanged,
        "files": len(before),
        "artifact_sha256": hashlib.sha256(
            json.dumps(before, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "cases": rows,
        "page_errors": errors,
        "request_failures": requests,
        "scope": "Local disposable HTTPS fixture; automatic WCAG checks and keyboard/responsive/metadata evidence, not full accessibility certification. English with Unicode readiness; translated locales and deployment unselected.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", type=Path, required=True)
    parser.add_argument("--variant", choices=("generic", "launchkit"), required=True)
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--private-key", type=Path, required=True)
    parser.add_argument("--axe-script", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = inspect(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    sys.stdout.write(
        json.dumps(
            {"result": result["result"], "cases": len(result["cases"]), "variant": args.variant}
        )
        + "\n"
    )
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
