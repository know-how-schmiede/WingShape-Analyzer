from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import os

import numpy as np
import pandas as pd


@dataclass
class AirfoilData:
    name: str
    upper: np.ndarray
    lower: np.ndarray
    source_format: str

    def to_dataframe(self) -> pd.DataFrame:
        upper_df = pd.DataFrame(self.upper, columns=["x", "y"])
        upper_df["surface"] = "upper"
        lower_df = pd.DataFrame(self.lower, columns=["x", "y"])
        lower_df["surface"] = "lower"
        return pd.concat([upper_df, lower_df], ignore_index=True)


class AirfoilParser:
    def __init__(self, text: str) -> None:
        self.raw_text = text
        self.name = "Unknown"
        self._rows: List[List[float]] = []
        self._parse_lines()

    @classmethod
    def from_file(cls, path: str) -> "AirfoilParser":
        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
            text = handle.read()
        parser = cls(text)
        if parser.name == "Unknown":
            parser.name = os.path.splitext(os.path.basename(path))[0]
        return parser

    def detect_format(self) -> str:
        if not self._rows:
            return "unknown"

        lengths = [len(row) for row in self._rows]

        third_const = self._third_column_constant()

        if self._paired_order() is not None and not third_const:
            return "paired"

        if third_const and self._paired_rows_possible():
            return "paired_rows"

        if third_const:
            return "xyz_cloud"

        if self._paired_rows_possible():
            return "paired_rows"

        first = self._rows[0]
        if len(first) == 2 and self._is_int_like(first[0]) and self._is_int_like(first[1]):
            n_upper = int(round(first[0]))
            n_lower = int(round(first[1]))
            if n_upper > 1 and n_lower > 1 and len(self._rows) >= 1 + n_upper + n_lower:
                return "lednicer"

        if all(length >= 2 for length in lengths):
            return "selig"

        return "unknown"

    def parse(self) -> AirfoilData:
        fmt = self.detect_format()
        if fmt == "paired":
            upper, lower = self._parse_paired()
        elif fmt == "xyz_cloud":
            upper, lower = self._parse_xyz_cloud()
        elif fmt == "paired_rows":
            upper, lower = self._parse_paired_rows()
        elif fmt == "lednicer":
            upper, lower = self._parse_lednicer()
        elif fmt == "selig":
            upper, lower = self._parse_selig()
        else:
            raise ValueError("Unsupported or unknown airfoil format.")

        return AirfoilData(
            name=self.name,
            upper=upper,
            lower=lower,
            source_format=fmt,
        )

    def _parse_lines(self) -> None:
        for line in self.raw_text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(("#", ";", "//")):
                continue

            numbers = self._try_parse_numbers(stripped)
            if numbers is None or len(numbers) < 2:
                if self.name == "Unknown" and self._looks_like_name(stripped):
                    self.name = stripped
                continue

            self._rows.append(numbers)

    @staticmethod
    def _looks_like_name(line: str) -> bool:
        return any(char.isalpha() for char in line)

    @staticmethod
    def _try_parse_numbers(line: str) -> Optional[List[float]]:
        cleaned = line.replace(",", " ")
        tokens = cleaned.split()
        if not tokens:
            return None
        try:
            return [float(token) for token in tokens]
        except ValueError:
            return None

    @staticmethod
    def _is_int_like(value: float) -> bool:
        return abs(value - round(value)) < 1e-6

    @staticmethod
    def _to_array(rows: List[List[float]], cols: int = 2) -> np.ndarray:
        return np.array([row[:cols] for row in rows], dtype=float)

    @staticmethod
    def _ensure_le_to_te(points: np.ndarray) -> np.ndarray:
        if points.shape[0] < 2:
            return points
        if points[0, 0] > points[-1, 0]:
            return points[::-1]
        return points

    @staticmethod
    def _find_turning_index(xs: np.ndarray) -> Optional[int]:
        if xs.size < 3:
            return None
        for idx in range(1, len(xs) - 1):
            prev = xs[idx] - xs[idx - 1]
            nxt = xs[idx + 1] - xs[idx]
            if prev == 0 or nxt == 0:
                continue
            if (prev < 0 < nxt) or (prev > 0 > nxt):
                return idx
        return None

    def _paired_order(self) -> Optional[tuple[int, int]]:
        if not self._rows:
            return None

        rows = [row[:3] for row in self._rows if len(row) >= 3]
        if len(rows) < 4:
            return None

        if len(rows) / len(self._rows) < 0.6:
            return None

        pairs = np.array(rows, dtype=float)
        if pairs.shape[0] < 2:
            return None

        col_a = pairs[:, 1]
        col_b = pairs[:, 2]
        ratio_ab = float(np.mean(col_b >= col_a))
        ratio_ba = float(np.mean(col_a >= col_b))

        threshold = 0.6
        if max(ratio_ab, ratio_ba) < threshold:
            return None

        if ratio_ab >= ratio_ba:
            return (2, 1)
        return (1, 2)

    def _third_column_constant(self) -> bool:
        values = [row[2] for row in self._rows if len(row) >= 3]
        if len(values) < max(3, int(0.8 * len(self._rows))):
            return False

        min_v = min(values)
        max_v = max(values)
        return abs(max_v - min_v) < 1e-6

    def _paired_rows_possible(self) -> bool:
        if not self._rows or not all(len(row) >= 2 for row in self._rows):
            return False

        points = self._to_array(self._rows)
        if points.shape[0] < 6:
            return False

        xs = points[:, 0]
        tol = 1e-6
        dup_adj = int(np.sum(np.abs(xs[1:] - xs[:-1]) < tol))
        ratio = dup_adj / max(1, xs.size - 1)
        return ratio >= 0.4

    def _parse_paired(self) -> tuple[np.ndarray, np.ndarray]:
        points = [row[:3] for row in self._rows if len(row) >= 3]
        if len(points) < 2:
            raise ValueError("Not enough paired-coordinate points.")

        pairs = np.array(points, dtype=float)
        if pairs[0, 0] > pairs[-1, 0]:
            pairs = pairs[::-1]

        order = self._paired_order()
        if order is None:
            raise ValueError("Paired-coordinate columns are not consistent.")

        upper_idx, lower_idx = order
        upper = np.column_stack((pairs[:, 0], pairs[:, upper_idx]))
        lower = np.column_stack((pairs[:, 0], pairs[:, lower_idx]))

        return upper, lower

    def _parse_paired_rows(self) -> tuple[np.ndarray, np.ndarray]:
        points = self._to_array(self._rows)
        if points.shape[0] < 4:
            raise ValueError("Not enough paired-row points.")

        if points[0, 0] > points[-1, 0]:
            points = points[::-1]

        tol = 1e-6
        groups: list[tuple[float, list[float]]] = []
        for x_val, y_val in points:
            if not groups or abs(x_val - groups[-1][0]) > tol:
                groups.append((x_val, [float(y_val)]))
            else:
                groups[-1][1].append(float(y_val))

        if len(groups) < 2:
            raise ValueError("Not enough grouped points for paired-row format.")

        upper_list = []
        lower_list = []
        for x_val, ys in groups:
            y_max = max(ys)
            y_min = min(ys)
            upper_list.append([x_val, y_max])
            lower_list.append([x_val, y_min])

        upper = np.array(upper_list, dtype=float)
        lower = np.array(lower_list, dtype=float)

        return upper, lower

    def _parse_xyz_cloud(self) -> tuple[np.ndarray, np.ndarray]:
        points = self._to_array(self._rows)
        if points.shape[0] < 6:
            raise ValueError("Not enough XYZ points.")

        order = np.argsort(points[:, 0])
        pts = points[order]
        ys = pts[:, 1]

        pos_ratio = float(np.mean(ys > 0.0))
        neg_ratio = float(np.mean(ys < 0.0))

        if pos_ratio > 0.2 and neg_ratio > 0.2:
            upper = pts[ys >= 0.0]
            lower = pts[ys <= 0.0]
            upper, lower = self._resample_common_x(upper, lower)
            return upper, lower

        n_points = len(ys)
        window = max(7, min(31, (n_points // 10) * 2 + 1))
        half = window // 2

        upper_mask = np.zeros(n_points, dtype=bool)
        for idx in range(n_points):
            start = max(0, idx - half)
            end = min(n_points, idx + half + 1)
            slice_ys = ys[start:end]
            y_min = float(np.min(slice_ys))
            y_max = float(np.max(slice_ys))
            camber = 0.5 * (y_min + y_max)
            upper_mask[idx] = ys[idx] >= camber

        upper = pts[upper_mask]
        lower = pts[~upper_mask]

        if upper.shape[0] < 2 or lower.shape[0] < 2:
            raise ValueError("Could not separate XYZ points into two surfaces.")

        upper, lower = self._resample_common_x(upper, lower)

        return upper, lower

    @staticmethod
    def _resample_common_x(
        upper: np.ndarray, lower: np.ndarray, n_points: Optional[int] = None
    ) -> tuple[np.ndarray, np.ndarray]:
        upper = AirfoilParser._sort_unique_x(upper)
        lower = AirfoilParser._sort_unique_x(lower)

        x_min = max(float(upper[0, 0]), float(lower[0, 0]))
        x_max = min(float(upper[-1, 0]), float(lower[-1, 0]))
        if x_max <= x_min:
            raise ValueError("Upper/lower x ranges do not overlap.")

        if n_points is None:
            n_points = max(len(upper), len(lower))

        x_common = np.linspace(x_min, x_max, n_points)
        y_upper = np.interp(x_common, upper[:, 0], upper[:, 1])
        y_lower = np.interp(x_common, lower[:, 0], lower[:, 1])

        upper_res = np.column_stack((x_common, y_upper))
        lower_res = np.column_stack((x_common, y_lower))
        return upper_res, lower_res

    @staticmethod
    def _sort_unique_x(points: np.ndarray, tol: float = 1e-9) -> np.ndarray:
        points = points[np.argsort(points[:, 0])]
        merged = []
        cur_x = None
        cur_ys = []
        for x_val, y_val in points:
            if cur_x is None or abs(x_val - cur_x) > tol:
                if cur_x is not None:
                    merged.append([cur_x, float(np.mean(cur_ys))])
                cur_x = float(x_val)
                cur_ys = [float(y_val)]
            else:
                cur_ys.append(float(y_val))
        if cur_x is not None:
            merged.append([cur_x, float(np.mean(cur_ys))])
        return np.array(merged, dtype=float)
    def _parse_lednicer(self) -> tuple[np.ndarray, np.ndarray]:
        header = self._rows[0]
        n_upper = int(round(header[0]))
        n_lower = int(round(header[1]))

        upper_rows = self._rows[1 : 1 + n_upper]
        lower_rows = self._rows[1 + n_upper : 1 + n_upper + n_lower]

        if len(upper_rows) < n_upper or len(lower_rows) < n_lower:
            raise ValueError("Lednicer block counts do not match data length.")

        upper = self._ensure_le_to_te(self._to_array(upper_rows))
        lower = self._ensure_le_to_te(self._to_array(lower_rows))

        return upper, lower

    def _parse_selig(self) -> tuple[np.ndarray, np.ndarray]:
        points = self._to_array(self._rows)
        if points.shape[0] < 4:
            raise ValueError("Not enough coordinate points for Selig format.")

        turning = self._find_turning_index(points[:, 0])
        idx = turning if turning is not None else int(np.argmin(points[:, 0]))

        upper_raw = points[: idx + 1]
        lower_raw = points[idx:]

        upper = self._ensure_le_to_te(upper_raw[::-1])
        lower = self._ensure_le_to_te(lower_raw)

        return upper, lower
