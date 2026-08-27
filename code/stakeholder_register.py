#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
from collections import Counter

# Xác định đường dẫn file dữ liệu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_PATHS = [
    os.path.join(BASE_DIR, "..", "datasets", "stakeholders.csv"),
    os.path.join(BASE_DIR, "datasets", "stakeholders.csv"),
    os.path.join(BASE_DIR, "..", "..", "..", "datasets", "stakeholders.csv")
]

DATA_PATH = None
for p in POSSIBLE_PATHS:
    if os.path.exists(p):
        DATA_PATH = os.path.join(p)
        break

if DATA_PATH is None:
    DATA_PATH = os.path.join(BASE_DIR, "..", "datasets", "stakeholders.csv")

OUT_MD_PATH = os.path.join(BASE_DIR, "stakeholder_register.md")
OUT_CSV_PATH = os.path.join(BASE_DIR, "stakeholder_register_output.csv")

# Bảng điểm quy đổi mức độ ảnh hưởng (Power) và mức độ ưu tiên (Interest)
LEVEL_SCORE = {"Low": 1, "Medium": 2, "High": 3}


def load_stakeholders(path):
    """Đọc dữ liệu stakeholder từ file CSV trả về danh sách các Dictionary."""
    with open(path, mode="r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def classify(sh):
    """
    Phân loại stakeholder theo ma trận Power / Interest Grid:
    - Power >= 3 (High) & Interest >= 3 (High)    -> Manage Closely (Quản lý chặt chẽ)
    - Power >= 3 (High) & Interest < 3 (Med/Low)   -> Keep Satisfied (Giữ cho hài lòng)
    - Power < 3 (Med/Low) & Interest >= 3 (High)   -> Keep Informed  (Cung cấp thông tin)
    - Power < 3 (Med/Low) & Interest < 3 (Med/Low) -> Monitor        (Theo dõi định kỳ)
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
    """Tạo bảng Markdown Stakeholder Register từ danh sách dữ liệu."""
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
# EXTENSION CODE: Xuất dữ liệu ra CSV & Bộ kiểm thử tự động (Unit Test)
# =========================================================================

def export_to_csv(rows, out_path):
    """Hàm mở rộng: Xuất danh sách stakeholder đã phân loại ra file CSV."""
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
    """Hàm kiểm thử tự động (Unit Test) kiểm tra 4 góc biên của ma trận Power/Interest Grid."""
    assert classify({"InfluenceLevel": "High", "PriorityLevel": "High"}) == "Manage Closely"
    assert classify({"InfluenceLevel": "High", "PriorityLevel": "Low"}) == "Keep Satisfied"
    assert classify({"InfluenceLevel": "Low", "PriorityLevel": "High"}) == "Keep Informed"
    assert classify({"InfluenceLevel": "Low", "PriorityLevel": "Low"}) == "Monitor"
    print("All tests PASS")


def main():
    # 1. Chạy bộ kiểm thử tự động
    test_classify()

    # 2. Đọc file dữ liệu đầu vào
    rows = load_stakeholders(DATA_PATH)

    # 3. Xuất file Markdown
    report_md = build_register(rows)
    with open(OUT_MD_PATH, "w", encoding="utf-8") as f:
        f.write(report_md)

    # 4. Xuất file CSV mở rộng
    export_to_csv(rows, OUT_CSV_PATH)

    # 5. In bảng thống kê ra màn hình Console (Chuẩn theo output mẫu)
    counts = Counter(classify(sh) for sh in rows)
    print("\nClassification summary:")
    for strategy, count in counts.items():
        print(f"  - {strategy}: {count} stakeholder(s)")
    print(f"[OK] Exported: stakeholder_register.md")


if __name__ == "__main__":
    main()
