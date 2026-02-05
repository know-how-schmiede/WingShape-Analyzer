# WingShape-Analyzer

WingShape-Analyzer is a Python GUI tool to load, detect, visualize, and export airfoil coordinates.
It focuses on robust format detection and clean plotting for CAD/CFD workflows.

## Features

- CustomTkinter GUI with file loading, plot view, and format/status panel.
- Matplotlib plot with equal aspect ratio.
- Format detection and parsing for common airfoil formats.
- CSV export of upper and lower surfaces.
- Version shown in the window title.

## Project Structure

- `src/` Python sources (`main.py`, `analyzer.py`, `version.py`)
- `doku/` Documentation (`logic.md`, `setup_guide.md`)
- `data/` Place airfoil CSV/DAT files here
- `setup_env.bat` Windows venv setup
- `setup_env.sh` Mac/Linux venv setup
- `requirements.txt` Dependencies
- `version.md` Version log

## Setup

Requirements: Python 3.10+.

Windows (PowerShell/CMD):
```bat
setup_env.bat
```

Mac/Linux:
```bash
bash setup_env.sh
```

## Run

Windows:
```bat
python src\main.py
```

Mac/Linux:
```bash
python src/main.py
```

## Supported Formats

- Selig (continuous loop)
- Lednicer (split blocks)
- Paired-Coordinates (X, Y-low, Y-high)
- XYZ CSV with constant third column (Z=0), separated into upper/lower

Details are documented in `doku/logic.md`.

## Export

Export writes a stacked CSV with columns:
`x, y, surface` where surface is `upper` or `lower`.

## Versioning

- Current version is stored in `src/version.py`.
- Changes are noted in `version.md`.

## Notes

If a dataset uses unusual ordering or coordinate conventions, please open an issue
with a short sample of the file so the parser can be adjusted.
