from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VERSION_FILE = ROOT / "src" / "version.py"
OUTPUT_FILE = Path(__file__).resolve().parent / "version.iss"

content = VERSION_FILE.read_text(encoding="utf-8")
match = re.search(r"VERSION\s*=\s*\"([^\"]+)\"", content)
if not match:
    raise SystemExit("VERSION not found in src/version.py")

version = match.group(1)
OUTPUT_FILE.write_text(f'#define APP_VERSION "{version}"\n', encoding="ascii")
print(f"Wrote {OUTPUT_FILE} with version {version}")
