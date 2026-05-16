#!/usr/bin/env python3
"""Count tdTomato/Ly6G classes from CellProfiler object-level CSV output."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Classify DAPI-defined CellProfiler objects by tdTomato and Ly6G "
            "mean-intensity thresholds."
        )
    )
    parser.add_argument("cellrois_csv", type=Path, help="CellProfiler CellROIs.csv file")
    parser.add_argument("--tdtom-threshold", type=float, required=True)
    parser.add_argument("--ly6g-threshold", type=float, required=True)
    parser.add_argument(
        "--tdtom-column",
        default="Intensity_MeanIntensity_tdTomato",
        help="tdTomato intensity column name",
    )
    parser.add_argument(
        "--ly6g-column",
        default="Intensity_MeanIntensity_Ly6G",
        help="Ly6G intensity column name",
    )
    parser.add_argument(
        "--group-column",
        default="ImageNumber",
        help="Column used to produce per-image/per-sample counts",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tdTom_Ly6G_counts.csv"),
        help="Output summary CSV",
    )
    return parser.parse_args()


def classify_cell(tdtom: float, ly6g: float, tdtom_threshold: float, ly6g_threshold: float) -> str:
    tdtom_state = "Pos" if tdtom >= tdtom_threshold else "Neg"
    ly6g_state = "Pos" if ly6g >= ly6g_threshold else "Neg"
    return f"tdTom{tdtom_state}_Ly6G{ly6g_state}"


def main() -> None:
    args = parse_args()

    counts_by_group: dict[str, Counter[str]] = defaultdict(Counter)

    with args.cellrois_csv.open(newline="") as handle:
        reader = csv.DictReader(handle)
        required = {args.tdtom_column, args.ly6g_column, args.group_column}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            available = ", ".join(reader.fieldnames or [])
            raise SystemExit(f"Missing column(s): {', '.join(sorted(missing))}\nAvailable: {available}")

        for row in reader:
            group = row[args.group_column]
            tdtom = float(row[args.tdtom_column])
            ly6g = float(row[args.ly6g_column])
            cell_class = classify_cell(tdtom, ly6g, args.tdtom_threshold, args.ly6g_threshold)
            counts_by_group[group][cell_class] += 1

    classes = [
        "tdTomNeg_Ly6GNeg",
        "tdTomPos_Ly6GNeg",
        "tdTomNeg_Ly6GPos",
        "tdTomPos_Ly6GPos",
    ]

    with args.output.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                args.group_column,
                "Total_DAPI_cells",
                *[f"{name}_count" for name in classes],
                *[f"{name}_percent" for name in classes],
            ]
        )

        for group in sorted(counts_by_group):
            counts = counts_by_group[group]
            total = sum(counts.values())
            percents = [
                (100.0 * counts[name] / total) if total else 0.0
                for name in classes
            ]
            writer.writerow(
                [
                    group,
                    total,
                    *[counts[name] for name in classes],
                    *[f"{value:.4f}" for value in percents],
                ]
            )

    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
