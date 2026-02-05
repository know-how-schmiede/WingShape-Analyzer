# WingShape-Analyzer ✈️

**WingShape-Analyzer** is a Python-based utility designed to automatically detect, analyze, and visualize aerodynamic airfoil coordinates. It serves as a bridge between raw coordinate data (from databases like UIUC or legacy CSV exports) and CAD/CFD software by ensuring point-cloud data is converted into a logical, continuous path.

## ✨ Key Features

* **Smart Format Detection:** Automatically identifies the structure of the input data (Selig, Lednicer, or Paired-Coordinate format).
* **Interactive GUI:** A user-friendly interface to load files and inspect airfoil shapes instantly.
* **Coordinate Normalization:** Ensures the airfoil is correctly scaled and oriented for engineering applications.
* **CAD-Ready Logic:** Reorders points into a continuous spline path to prevent "zigzag" artifacts during CAD import.

---

## 🛠 Technical Logic & Pattern Recognition

The core of the analyzer is its ability to distinguish between common airfoil data standards:

### 1. Paired-Coordinate Format (Vertical Pairs)
* **Pattern:** Consecutive rows share identical or near-identical X-coordinates but provide both the upper (positive Y) and lower (negative Y) surface points.
* **Algorithm:** The tool splits the data into two sets, reverses the upper set, and joins them to create a smooth loop starting from the trailing edge, moving to the nose, and back.



### 2. Selig Format
* **Pattern:** A single continuous block of data. Points typically start at the trailing edge ($x \approx 1.0$), wrap around the leading edge ($x \approx 0.0$), and return to the trailing edge.
* **Algorithm:** Interpreted as a direct sequence for spline generation.

### 3. Lednicer Format
* **Pattern:** Data is divided into two distinct blocks (Upper and Lower), often separated by a header or a blank line. Both blocks usually start from the leading edge ($x=0$).
* **Algorithm:** Merges blocks by reversing the upper surface and appending the lower surface to ensure a consistent flow.



---

## 📈 Visualizing the Geometry

The application utilizes a **Matplotlib** backend to render the airfoil. To ensure geometric accuracy, the "Equal Aspect Ratio" is enforced, preventing the common mistake of displaying thin airfoils as overly thick or distorted.



---

## 📝 Roadmap

* [ ] **Core Engine:** Automatic format detection logic.
* [ ] **UI:** File dialog integration and info panel for airfoil metadata.
* [ ] **Export:** Save processed coordinates as `.dat` (Selig format) or `.dxf` for CAD.
* [ ] **Analysis:** Real-time calculation of maximum thickness and camber position.

## 🤝 Contribution

This project is developed with the assistance of **CodeX**. Feel free to open an issue or submit a pull request if you encounter unsupported coordinate patterns.
