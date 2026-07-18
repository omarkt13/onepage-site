#!/usr/bin/env python3
"""Inline assets/*.jpg into template.html as data URIs -> index.html.

Keeps the site a single self-contained file (artifact CSP allows no external
requests) while the repo stays editable: change template.html or swap a
render in assets/, then `python3 build.py`.
"""
import base64
import re
import sys
from pathlib import Path

root = Path(__file__).parent
template = (root / "template.html").read_text()


def inline(match):
    name = match.group(1)
    path = root / "assets" / f"{name}.jpg"
    if not path.exists():
        sys.exit(f"missing asset: {path}")
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:image/jpeg;base64,{b64}"


out, n = re.subn(r"\{\{IMG:([a-z0-9-]+)\}\}", inline, template)
(root / "index.html").write_text(out)
size_mb = (root / "index.html").stat().st_size / 1e6
print(f"index.html written: {n} images inlined, {size_mb:.1f} MB")
