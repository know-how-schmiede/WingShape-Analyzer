# Airfoil Parsing Logic

This project supports three common airfoil coordinate formats and converts them into a unified
representation with two point sets: `upper` and `lower` surfaces. Both surfaces are stored in
leading-edge to trailing-edge order (x increasing whenever possible).

## 1) Selig (continuous loop)

Typical structure:
- Optional name line
- Two-column coordinates (x y)
- Points form a continuous loop: trailing edge -> upper surface -> leading edge -> lower surface -> trailing edge

Parsing steps:
1. Read all numeric rows with at least two columns.
2. Detect the leading edge as the turning point in x (change from decreasing to increasing),
   falling back to the minimum x value if no turn is found.
3. Split into upper and lower at the leading-edge index.
4. Reverse the upper block so both surfaces run from leading edge to trailing edge.

## 2) Lednicer (split blocks)

Typical structure:
- Optional name line
- Line with two integers: `N_upper N_lower`
- `N_upper` coordinate rows
- `N_lower` coordinate rows

Parsing steps:
1. Verify the count line and that enough rows are present.
2. Read upper and lower blocks.
3. If needed, reverse blocks so x increases from leading edge to trailing edge.

## 3) Paired-Coordinates (X, Y-low, Y-high)

Typical structure:
- Optional name line
- Three-column rows: `x  y_low  y_high`

Parsing steps:
1. Read all numeric rows with at least three columns.
2. If x is descending, reverse the list.
3. Build `upper` from (x, y_high) and `lower` from (x, y_low).

## Output Representation

The parser returns an `AirfoilData` object:
- `upper`: Nx2 array of (x, y)
- `lower`: Mx2 array of (x, y)
- `source_format`: detected format string

The GUI exports a stacked CSV with columns `x`, `y`, and `surface` (upper/lower).

## 4) XYZ (X, Y, Z=konstant)

Einige CSV-Dateien enthalten 3 Spalten, wobei die dritte Spalte (Z) durchgehend 0 ist. In diesem
Fall wird die Datei als 2D-Punktwolke interpretiert.

Parsing steps:
1. Ignoriere die Z-Spalte.
2. Sortiere nach X und schaetze lokal die Camber-Linie als Mittelwert aus lokalem Y-Min und Y-Max.
3. Teile Punkte oberhalb/unterhalb dieser Linie in obere und untere Flaeche.
4. Sortiere beide Flaechen nach X aufsteigend.
5. Resample beide Flaechen auf ein gemeinsames X-Gitter, damit Upper/Lower die gleiche Punktzahl haben.
