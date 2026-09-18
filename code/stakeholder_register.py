#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stakeholder_register.py
Lab 01 – RE Process & Project Kickoff
Course: CSE703095 – Software Requirements
Institution: Phenikaa University – School of Information Systems
Author: Tran Doan Viet Anh
------------------------------------------------------------------------
Key functionalities:
1. Load stakeholder records from CSV (datasets/stakeholders.csv).
2. Classify stakeholders using the Power (influence) / Interest (priority) grid.
3. Export Stakeholder Register table to Markdown (stakeholder_register.md).
4. Extension 1: Export classified records to CSV (stakeholder_register_output.csv).
5. Extension 2: Automated assert unit test suite validating boundary combinations.

Execution:
    py stakeholder_register.py
"""

import csv
import os
from collections import Counter

# Resolve dataset and output file paths dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_PATHS = [
    os.path.join(BASE_DIR, "..", "datasets", "stakeholders.csv"),
    os.path.join(BASE_DIR, "datasets", "stakeholders.csv"),
    os.path.join(BASE_DIR, "..", "..", "..", "datasets", "stakeholders.csv")
]

DATA_PATH = None
for p in POSSIBLE_PATHS:
    if os.path.exists(p):
        DATA_PATH = os.path.abspath(p)
        break

if DATA_PATH is None:
    DATA_PATH = os.path.join(BASE_DIR, "..", "datasets", "stakeholders.csv")

OUT_MD_PATH = os.path.join(BASE_DIR, "stakeholder_register.md")
OUT_CSV_PATH = os.path.join(BASE_DIR, "stakeholder_register_output.csv")

# Numeric score mapping for influence (Power) and priority (Interest)
LEVEL_SCORE = {"Low": 1, "Medium": 2, "High": 3}


def load_stakeholders(path):
    """Load stakeholder records from CSV into a list of dictionaries."""
    with open(path, mode="r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classify(sh):
    """
    Classify a stakeholder using the Power/Interest Grid:
    - Power >= 3 (High) & Interest >= 3 (High)    -> Manage Closely
    - Power >= 3 (High) & Interest < 3 (Med/Low)   -> Keep Satisfied
    - Power < 3 (Med/Low) & Interest >= 3 (High)   -> Keep Informed
    - Power < 3 (Med/Low) & Interest < 3 (Med/Low) -> Monitor
    """
    power = LEVEL_SCORE.get(sh.get("InfluenceLevel"), 1)
    interest = LEVEL_SCORE.get(sh.get("PriorityLevel"), 1)

    if power >= 3 and interest >= 3:
        return "Manage Closely"
    if power >= 3 and interest < 3:
        return "Keep Satisfied"
    if power < 3 and interest >= 3:
        return "Keep Informed"
    return "Monitor"


def build_register(rows):
    """Construct Markdown Stakeholder Register from loaded rows."""
    lines = [
        "# Stakeholder Register",
        "",
        "Project: MedBook - Online Medical Appointment Booking System",
        "Author: Tran Doan Viet Anh",
        "",
        "| ID | Name | Category | Power | Interest | Management Strategy |",
        "|---|---|---|---|---|---|"
    ]
    for sh in rows:
        strategy = classify(sh)
        lines.append(
            f"| {sh['StakeholderID']} | {sh['StakeholderName']} | {sh['Category']} | "
            f"{sh['InfluenceLevel']} | {sh['PriorityLevel']} | {strategy} |"
        )
    return "\n".join(lines)


# =========================================================================
# EXTENSION CODE: CSV Export & Boundary Unit Testing
# =========================================================================

def export_to_csv(rows, out_path):
    """Extension: Export classified stakeholder dataset to CSV."""
    fieldnames = [
        "StakeholderID",
        "StakeholderName",
        "Category",
        "InfluenceLevel",
        "PriorityLevel",
        "ManagementStrategy"
    ]
    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for sh in rows:
            row_dict = dict(sh)
            row_dict["ManagementStrategy"] = classify(sh)
            writer.writerow(row_dict)


def test_classify():
    """Automated assert unit test suite validating 4 boundary combinations."""
    assert classify({"InfluenceLevel": "High", "PriorityLevel": "High"}) == "Manage Closely"
    assert classify({"InfluenceLevel": "High", "PriorityLevel": "Low"}) == "Keep Satisfied"
    assert classify({"InfluenceLevel": "Low", "PriorityLevel": "High"}) == "Keep Informed"
    assert classify({"InfluenceLevel": "Low", "PriorityLevel": "Low"}) == "Monitor"
    print("All tests PASS")


def main():
    # 1. Run automated boundary unit tests
    test_classify()

    # 2. Read stakeholder records
    rows = load_stakeholders(DATA_PATH)

    # 3. Export Markdown register
    report_md = build_register(rows)
    with open(OUT_MD_PATH, "w", encoding="utf-8") as f:
        f.write(report_md)

    # 4. Export CSV register
    export_to_csv(rows, OUT_CSV_PATH)

    # 5. Output classification summary and export confirmation to console
    counts = Counter(classify(sh) for sh in rows)
    print("\nClassification summary:")
    for strategy, count in counts.items():
        print(f"  - {strategy}: {count} stakeholder(s)")
    print(f"[OK] Exported: stakeholder_register.md")


if __name__ == "__main__":
    main()
