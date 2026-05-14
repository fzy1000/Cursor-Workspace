#!/usr/bin/env python3
"""
从 materials/ 中的周度净值表计算周收益与 Pearson 相关（仅标准库，便于无 pip 环境复现）。
口径：docs/consensus.md §2.1–2.3
"""
from __future__ import annotations

import csv
import math
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
XLSX = REPO / "materials" / "CTA&混合中性_周度净值序列.xlsx"
OUT_DIR = REPO / "results"
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def xl_serial_to_datetime(serial: float) -> datetime:
    return datetime(1899, 12, 30) + timedelta(days=int(serial))


def load_sheet(path: Path) -> tuple[list[str], list[tuple[datetime, float, float | None]]]:
    with zipfile.ZipFile(path, "r") as z:
        sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
        strings: list[str] = []
        for si in sst.findall("m:si", NS):
            parts: list[str] = []
            for t in si.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"):
                if t.text:
                    parts.append(t.text)
            strings.append("".join(parts))

        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))

        def cell_value(c: ET.Element):
            t = c.get("t")
            v = c.find("m:v", NS)
            if v is None or v.text is None:
                return None
            if t == "s":
                return strings[int(v.text)]
            return float(v.text)

        rows_data: dict[int, dict[str, object]] = {}
        for row in sheet.findall(".//m:sheetData/m:row", NS):
            ridx = int(row.get("r", 0))
            row_cells: dict[str, object] = {}
            for c in row.findall("m:c", NS):
                ref = c.get("r", "")
                col = "".join(x for x in ref if x.isalpha())
                row_cells[col] = cell_value(c)
            rows_data[ridx] = row_cells

        def get_cell(r: int, col: str):
            return rows_data.get(r, {}).get(col)

        headers = [
            str(get_cell(1, "A")),
            str(get_cell(1, "B")),
            str(get_cell(1, "C")),
        ]
        series: list[tuple[datetime, float, float | None]] = []
        for r in range(2, 202):
            d = get_cell(r, "A")
            b = get_cell(r, "B")
            c = get_cell(r, "C")
            if d is None or b is None or not isinstance(d, float):
                continue
            nav_c = float(c) if isinstance(c, float) else None
            series.append((xl_serial_to_datetime(d), float(b), nav_c))
        return headers, series


def pearson(x: list[float], y: list[float]) -> float:
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    cov = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    vx = sum((xi - mx) ** 2 for xi in x)
    vy = sum((yi - my) ** 2 for yi in y)
    return cov / math.sqrt(vx * vy) if vx > 0 and vy > 0 else float("nan")


def main() -> None:
    if not XLSX.is_file():
        raise SystemExit(f"Missing source file: {XLSX}")

    headers, series = load_sheet(XLSX)
    overlap = [(t, b, c) for t, b, c in series if c is not None]

    rb: list[float] = []
    rc: list[float] = []
    for i in range(1, len(overlap)):
        _, b0, c0 = overlap[i - 1]
        _, b1, c1 = overlap[i]
        rb.append(b1 / b0 - 1.0)
        rc.append(c1 / c0 - 1.0)

    n_ret = len(rb)
    r_xy = pearson(rb, rc)
    mean_b = sum(rb) / n_ret
    mean_c = sum(rc) / n_ret
    var_b = sum((x - mean_b) ** 2 for x in rb) / n_ret
    var_c = sum((x - mean_c) ** 2 for x in rc) / n_ret
    std_b = math.sqrt(var_b)
    std_c = math.sqrt(var_c)

    both_pos = sum(1 for i in range(n_ret) if rb[i] > 0 and rc[i] > 0)
    both_neg = sum(1 for i in range(n_ret) if rb[i] < 0 and rc[i] < 0)
    disagree = n_ret - both_pos - both_neg

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    stats_path = OUT_DIR / "exploratory_stats.csv"
    with stats_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["metric", "value"])
        w.writerow(["source_file", str(XLSX.relative_to(REPO))])
        w.writerow(["sheet", "Sheet"])
        w.writerow(["header_A", headers[0]])
        w.writerow(["header_B", headers[1]])
        w.writerow(["header_C", headers[2]])
        w.writerow(["rows_with_date_and_nav_b", len(series)])
        w.writerow(["rows_overlap_b_and_c", len(overlap)])
        w.writerow(["n_weekly_return_pairs", n_ret])
        w.writerow(["overlap_first_date", overlap[0][0].strftime("%Y-%m-%d")])
        w.writerow(["overlap_last_date", overlap[-1][0].strftime("%Y-%m-%d")])
        w.writerow(["pearson_r_weekly_returns", f"{r_xy:.9f}"])
        w.writerow(["mean_weekly_return_hedge9", f"{mean_b:.9f}"])
        w.writerow(["mean_weekly_return_cta", f"{mean_c:.9f}"])
        w.writerow(["std_weekly_return_hedge9", f"{std_b:.9f}"])
        w.writerow(["std_weekly_return_cta", f"{std_c:.9f}"])
        w.writerow(["min_weekly_return_hedge9", f"{min(rb):.9f}"])
        w.writerow(["max_weekly_return_hedge9", f"{max(rb):.9f}"])
        w.writerow(["min_weekly_return_cta", f"{min(rc):.9f}"])
        w.writerow(["max_weekly_return_cta", f"{max(rc):.9f}"])
        w.writerow(["weeks_both_positive", both_pos])
        w.writerow(["weeks_both_negative", both_neg])
        w.writerow(["weeks_mixed_sign", disagree])
        w.writerow(["weak_linear_per_consensus_abs_r_lt_0_30", abs(r_xy) < 0.30])

    print(f"Wrote {stats_path}")
    print(f"Pearson r = {r_xy:.6f}  (n={n_ret})")


if __name__ == "__main__":
    main()
