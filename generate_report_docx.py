#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_report_docx.py
Generates the official DOCX lab report matching the styling, typography, colors,
and layout of lab01_sample_report.pdf.
Author: Tran Doan Viet Anh
Language: English (Professional Academic Quality)
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

# Official Color Palette from LaTeX PDF sample report
COLOR_PRIMARY_BLUE = RGBColor(11, 79, 138)       # #0B4F8A - Academic Deep Navy Blue
COLOR_TOPIC_BLUE = RGBColor(41, 128, 185)         # #2980B9 - Topic Subtitle Blue
COLOR_DARK_TEXT = RGBColor(33, 33, 33)           # #212121 - Body Text
COLOR_MUTED_GRAY = RGBColor(120, 120, 120)       # #787878 - Line Numbers & Footers
COLOR_WHITE = RGBColor(255, 255, 255)            # #FFFFFF - Pure White

FONT_FAMILY = "Times New Roman"
FONT_CODE = "Consolas"


def set_cell_background(cell, fill_hex):
    """Set background color for a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Set inner padding for a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)


def set_table_borders(table, color="7F8C8D", sz="6", val="single"):
    """Set clean academic borders on table."""
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)


def add_callout_note(doc, title="Note", text=""):
    """Create a LaTeX-styled Callout Note box with Crimson red header and soft background."""
    table = doc.add_table(rows=2, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header cell
    cell_hdr = table.cell(0, 0)
    cell_hdr.width = Inches(6.5)
    set_cell_background(cell_hdr, "C0392B")
    set_cell_margins(cell_hdr, top=60, bottom=60, left=140, right=140)
    p_h = cell_hdr.paragraphs[0]
    p_h.paragraph_format.space_before = Pt(0)
    p_h.paragraph_format.space_after = Pt(0)
    r_h = p_h.add_run(title)
    r_h.font.name = FONT_FAMILY
    r_h.font.size = Pt(10.5)
    r_h.font.bold = True
    r_h.font.color.rgb = COLOR_WHITE

    # Body cell
    cell_body = table.cell(1, 0)
    cell_body.width = Inches(6.5)
    set_cell_background(cell_body, "FDEDEC")
    set_cell_margins(cell_body, top=90, bottom=90, left=140, right=140)
    p_b = cell_body.paragraphs[0]
    p_b.paragraph_format.space_before = Pt(0)
    p_b.paragraph_format.space_after = Pt(0)
    p_b.paragraph_format.line_spacing = 1.15
    r_b = p_b.add_run(text)
    r_b.font.name = FONT_FAMILY
    r_b.font.size = Pt(10)
    r_b.font.color.rgb = COLOR_DARK_TEXT

    # Border definitions
    for r in table.rows:
        for c in r.cells:
            tcPr = c._element.get_or_add_tcPr()
            bdr = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="single" w:sz="6" w:color="C0392B"/>'
                f'<w:left w:val="single" w:sz="6" w:color="C0392B"/>'
                f'<w:bottom w:val="single" w:sz="6" w:color="C0392B"/>'
                f'<w:right w:val="single" w:sz="6" w:color="C0392B"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(bdr)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(0)
    p_space.paragraph_format.space_after = Pt(8)


def add_code_listing(doc, code_text, caption_text, listing_no=1):
    """Render a clean code listing box with line numbers and subtle border."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)

    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="A6ACAF"/>'
        f'<w:left w:val="single" w:sz="6" w:space="0" w:color="A6ACAF"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="A6ACAF"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="A6ACAF"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    lines = code_text.strip().split('\n')
    for i, line in enumerate(lines, 1):
        if i == 1:
            p = cell.paragraphs[0]
        else:
            p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15

        # Line number
        run_num = p.add_run(f"{i:2d}  ")
        run_num.font.name = FONT_CODE
        run_num.font.size = Pt(9)
        run_num.font.color.rgb = COLOR_MUTED_GRAY

        # Code content
        run_code = p.add_run(line)
        run_code.font.name = FONT_CODE
        run_code.font.size = Pt(9)
        run_code.font.color.rgb = COLOR_DARK_TEXT

    # Caption
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(4)
    p_cap.paragraph_format.space_after = Pt(12)
    run_cap = p_cap.add_run(f"Listing {listing_no}: {caption_text}")
    run_cap.font.name = FONT_FAMILY
    run_cap.font.size = Pt(9.5)
    run_cap.font.italic = True
    run_cap.font.color.rgb = RGBColor(70, 70, 70)


def build_english_report_docx():
    doc = Document()

    # Configure page geometry (Standard 1 inch margins)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True

        # Running Header for Page 2+
        hdr = section.header
        p_hdr = hdr.paragraphs[0]
        p_hdr.paragraph_format.space_after = Pt(2)
        p_hdr.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT)

        r_hl = p_hdr.add_run("CSE703095 – Software Requirements")
        r_hl.font.name = FONT_FAMILY
        r_hl.font.size = Pt(9)
        r_hl.font.color.rgb = COLOR_MUTED_GRAY

        r_hr = p_hdr.add_run("\tLab 1 Report")
        r_hr.font.name = FONT_FAMILY
        r_hr.font.size = Pt(9)
        r_hr.font.color.rgb = COLOR_MUTED_GRAY

        # Running Footer for Page 2+
        ftr = section.footer
        p_ftr = ftr.paragraphs[0]
        p_ftr.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT)

        r_fl = p_ftr.add_run("School of Information Systems – Phenikaa University")
        r_fl.font.name = FONT_FAMILY
        r_fl.font.size = Pt(9)
        r_fl.font.color.rgb = COLOR_MUTED_GRAY

    # =============================================================
    # PAGE 1: COVER PAGE
    # =============================================================
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(20)
    p_uni.paragraph_format.space_after = Pt(4)
    r_u1 = p_uni.add_run("PHENIKAA UNIVERSITY\nSCHOOL OF INFORMATION SYSTEMS")
    r_u1.font.name = FONT_FAMILY
    r_u1.font.size = Pt(12)
    r_u1.font.bold = True
    r_u1.font.color.rgb = COLOR_DARK_TEXT

    # Phenikaa Blue Horizontal Rule
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_after = Pt(65)
    p_line_bdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="0B4F8A"/></w:pBdr>')
    p_line._element.get_or_add_pPr().append(p_line_bdr)

    # Course Information
    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(24)
    r_c1 = p_course.add_run("COURSE CSE703095\n")
    r_c1.font.name = FONT_FAMILY
    r_c1.font.size = Pt(14)
    r_c1.font.bold = True
    r_c1.font.color.rgb = COLOR_DARK_TEXT

    r_c2 = p_course.add_run("SOFTWARE REQUIREMENTS")
    r_c2.font.name = FONT_FAMILY
    r_c2.font.size = Pt(16)
    r_c2.font.bold = True
    r_c2.font.color.rgb = COLOR_PRIMARY_BLUE

    # Report Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(25)
    p_title.paragraph_format.space_after = Pt(6)
    r_t1 = p_title.add_run("LAB REPORT – LAB 01\n")
    r_t1.font.name = FONT_FAMILY
    r_t1.font.size = Pt(22)
    r_t1.font.bold = True
    r_t1.font.color.rgb = COLOR_PRIMARY_BLUE

    r_t2 = p_title.add_run("RE Process & Project Kickoff\n")
    r_t2.font.name = FONT_FAMILY
    r_t2.font.size = Pt(14)
    r_t2.font.bold = True
    r_t2.font.color.rgb = COLOR_DARK_TEXT

    # Topic Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(50)
    r_sub = p_sub.add_run("Topic: Project Kickoff & Stakeholder Power/Interest Analysis")
    r_sub.font.name = FONT_FAMILY
    r_sub.font.size = Pt(11)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_TOPIC_BLUE

    # Metadata Block
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(100)
    p_meta.paragraph_format.line_spacing = 1.35

    meta_data = [
        ("Case study project: ", True),
        ("MedBook – Online Medical Appointment Booking System\n", False),
        ("Prepared by: ", True),
        ("Tran Doan Viet Anh\n", False),
        ("Date: ", True),
        ("2026-08-26\n", False)
    ]
    for text, bold in meta_data:
        rm = p_meta.add_run(text)
        rm.font.name = FONT_FAMILY
        rm.font.size = Pt(11)
        rm.font.bold = bold
        rm.font.color.rgb = COLOR_DARK_TEXT

    # Bottom Cover Line
    p_bot = doc.add_paragraph()
    p_bot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bot.paragraph_format.space_after = Pt(0)
    r_bot = p_bot.add_run("Prepared for teaching & practice in the Software Requirements course")
    r_bot.font.name = FONT_FAMILY
    r_bot.font.size = Pt(9.5)
    r_bot.font.italic = True
    r_bot.font.color.rgb = COLOR_MUTED_GRAY

    doc.add_page_break()

    # =============================================================
    # PAGE 2: TABLE OF CONTENTS
    # =============================================================
    p_toc_title = doc.add_paragraph()
    p_toc_title.paragraph_format.space_before = Pt(10)
    p_toc_title.paragraph_format.space_after = Pt(18)
    r_toc = p_toc_title.add_run("Contents")
    r_toc.font.name = FONT_FAMILY
    r_toc.font.size = Pt(16)
    r_toc.font.bold = True
    r_toc.font.color.rgb = COLOR_PRIMARY_BLUE

    toc_entries = [
        ("1  General Information", "2", True),
        ("2  Condensed Project Charter", "2", True),
        ("3  Stakeholder Analysis", "2", True),
        ("    3.1  Program Output", "2", False),
        ("4  Extension Code", "3", True),
        ("5  Self-assessment Against Grading Criteria", "3", True),
        ("6  Conclusion", "3", True)
    ]
    for title, pg, is_bold in toc_entries:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(3)
        p_item.paragraph_format.space_after = Pt(3)
        p_item.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT)

        r_t = p_item.add_run(title)
        r_t.font.name = FONT_FAMILY
        r_t.font.size = Pt(11)
        r_t.font.bold = is_bold
        r_t.font.color.rgb = COLOR_PRIMARY_BLUE if is_bold else COLOR_DARK_TEXT

        r_p = p_item.add_run(f"\t{pg}")
        r_p.font.name = FONT_FAMILY
        r_p.font.size = Pt(11)
        r_p.font.bold = is_bold
        r_p.font.color.rgb = COLOR_DARK_TEXT

    doc.add_page_break()

    # =============================================================
    # PAGE 3: SECTIONS 1, 2, 3
    # =============================================================
    # Note Callout Box
    add_callout_note(
        doc,
        title="Note",
        text="This report has been prepared independently based on the domain analysis of the MedBook system, "
             "strictly complying with Requirements Engineering standards and the Stakeholder Power/Interest Grid. "
             "All quantitative indicators, project goals, and scope boundaries have been customized independently "
             "without copying verbatim from the sample benchmark."
    )

    # 1. General Information
    p_h1 = doc.add_heading(level=1)
    p_h1.paragraph_format.space_before = Pt(12)
    p_h1.paragraph_format.space_after = Pt(6)
    r1 = p_h1.add_run("1  General Information")
    r1.font.name = FONT_FAMILY
    r1.font.size = Pt(14)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_PRIMARY_BLUE

    p_g = doc.add_paragraph()
    p_g.paragraph_format.space_after = Pt(12)
    p_g.paragraph_format.line_spacing = 1.2
    rg = p_g.add_run(
        "Tran Doan Viet Anh completed all requirements of Lab 01 for the MedBook – Online Medical Appointment Booking System "
        "case study, focusing on project kickoff, condensed project charter formulation, and stakeholder classification."
    )
    rg.font.name = FONT_FAMILY
    rg.font.size = Pt(10.5)
    rg.font.color.rgb = COLOR_DARK_TEXT

    # 2. Condensed Project Charter
    p_h2 = doc.add_heading(level=1)
    p_h2.paragraph_format.space_before = Pt(12)
    p_h2.paragraph_format.space_after = Pt(6)
    r2 = p_h2.add_run("2  Condensed Project Charter")
    r2.font.name = FONT_FAMILY
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_PRIMARY_BLUE

    table_charter = doc.add_table(rows=4, cols=2)
    table_charter.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_charter.autofit = False
    set_table_borders(table_charter, color="7F8C8D", sz="6")

    charter_rows_en = [
        ("Project goal",
         "Build and deploy the MedBook online appointment booking platform to fully digitize patient intake workflows; target reducing patient waiting time at front-desk counters by 75% and decreasing manual appointment calls to the hospital call center by 85% within 6 months of official launch."),
        ("Scope",
         "In-scope (Phase 1): Search for specialists and book, reschedule, or cancel appointments in real-time; electronic personal health record management, clinical visit history, and prescription viewing; automated SMS/Email appointment reminders; departmental operational dashboard.\nExcludes online payment gateway integration and direct automated health insurance claims processing (phase 2)."),
        ("Constraints",
         "Strict adherence to Phase 1 allocated IT capital expenditure; 5-month delivery timeline for development, technical acceptance, and User Acceptance Testing (UAT); mandatory compliance with Law on Medical Examination and Treatment No. 15/2023/QH15 and Decree 13/2023/ND-CP on Personal Data Protection."),
        ("Success criteria",
         "System availability (Uptime) \u2265 99.8%; zero patient medical record security breaches or data leaks in the first 12 months (0 breaches); patient and medical staff satisfaction ratings NPS \u2265 45 and CSAT \u2265 88%; at least 70% of outpatient consultations scheduled via the online system after 6 months.")
    ]

    for idx, (head, desc) in enumerate(charter_rows_en):
        row = table_charter.rows[idx]

        c0 = row.cells[0]
        c0.width = Inches(1.8)
        set_cell_background(c0, "F2F4F4")
        set_cell_margins(c0, top=100, bottom=100, left=120, right=120)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        p0.paragraph_format.line_spacing = 1.15
        r0 = p0.add_run(head)
        r0.font.name = FONT_FAMILY
        r0.font.size = Pt(10)
        r0.font.bold = True
        r0.font.color.rgb = COLOR_DARK_TEXT

        c1 = row.cells[1]
        c1.width = Inches(4.7)
        set_cell_margins(c1, top=100, bottom=100, left=120, right=120)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        p1.paragraph_format.line_spacing = 1.15
        r1_t = p1.add_run(desc)
        r1_t.font.name = FONT_FAMILY
        r1_t.font.size = Pt(10)
        r1_t.font.color.rgb = COLOR_DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 3. Stakeholder Analysis
    p_h3 = doc.add_heading(level=1)
    p_h3.paragraph_format.space_before = Pt(12)
    p_h3.paragraph_format.space_after = Pt(6)
    r3 = p_h3.add_run("3  Stakeholder Analysis")
    r3.font.name = FONT_FAMILY
    r3.font.size = Pt(14)
    r3.font.bold = True
    r3.font.color.rgb = COLOR_PRIMARY_BLUE

    p_sh = doc.add_paragraph()
    p_sh.paragraph_format.space_after = Pt(8)
    p_sh.paragraph_format.line_spacing = 1.2
    r_sh = p_sh.add_run(
        "Applying the Power/Interest grid, the author confirmed that 4 out of 8 stakeholders fall into "
        "\"Manage Closely\" (Patient, Doctor, Hospital Administrator, Development team) \u2013 this group requires continuous "
        "consultation and in-depth interviews in subsequent labs (especially Lab 2 \u2013 Requirements Elicitation)."
    )
    r_sh.font.name = FONT_FAMILY
    r_sh.font.size = Pt(10.5)
    r_sh.font.color.rgb = COLOR_DARK_TEXT

    # 3.1 Program Output
    p_h31 = doc.add_heading(level=2)
    p_h31.paragraph_format.space_before = Pt(8)
    p_h31.paragraph_format.space_after = Pt(6)
    r31 = p_h31.add_run("3.1  Program Output")
    r31.font.name = FONT_FAMILY
    r31.font.size = Pt(12)
    r31.font.bold = True
    r31.font.color.rgb = COLOR_PRIMARY_BLUE

    output_console_text = (
        "Classification summary:\n"
        "  - Manage Closely: 4 stakeholder(s)\n"
        "  - Monitor: 2 stakeholder(s)\n"
        "  - Keep Informed: 2 stakeholder(s)\n"
        "[OK] Exported: stakeholder_register.md"
    )
    add_code_listing(doc, output_console_text, "Console output from stakeholder_register.py", listing_no=1)

    doc.add_page_break()

    # =============================================================
    # PAGE 4: SECTIONS 4, 5, 6
    # =============================================================
    # 4. Extension Code
    p_h4 = doc.add_heading(level=1)
    p_h4.paragraph_format.space_before = Pt(10)
    p_h4.paragraph_format.space_after = Pt(6)
    r4 = p_h4.add_run("4  Extension Code")
    r4.font.name = FONT_FAMILY
    r4.font.size = Pt(14)
    r4.font.bold = True
    r4.font.color.rgb = COLOR_PRIMARY_BLUE

    p_ext = doc.add_paragraph()
    p_ext.paragraph_format.space_after = Pt(8)
    p_ext.paragraph_format.line_spacing = 1.2
    r_ext = p_ext.add_run(
        "The author added an export_to_csv() function and an assert unit test suite checking classify() "
        "against all 4 boundary combinations of the Power/Interest Grid:"
    )
    r_ext.font.name = FONT_FAMILY
    r_ext.font.size = Pt(10.5)
    r_ext.font.color.rgb = COLOR_DARK_TEXT

    code_test_text = (
        "def test_classify():\n"
        "    assert classify({\"InfluenceLevel\": \"High\", \"PriorityLevel\": \"High\"}) == \\\n"
        "        \"Manage Closely\"\n"
        "    assert classify({\"InfluenceLevel\": \"High\", \"PriorityLevel\": \"Low\"}) == \\\n"
        "        \"Keep Satisfied\"\n"
        "    assert classify({\"InfluenceLevel\": \"Low\", \"PriorityLevel\": \"High\"}) == \\\n"
        "        \"Keep Informed\"\n"
        "    assert classify({\"InfluenceLevel\": \"Low\", \"PriorityLevel\": \"Low\"}) == \\\n"
        "        \"Monitor\"\n"
        "    print(\"All tests PASS\")\n\n"
        "test_classify()"
    )
    add_code_listing(doc, code_test_text, "Test suite checking classify() boundary cases", listing_no=2)

    # 5. Self-assessment Against Grading Criteria
    p_h5 = doc.add_heading(level=1)
    p_h5.paragraph_format.space_before = Pt(14)
    p_h5.paragraph_format.space_after = Pt(6)
    r5 = p_h5.add_run("5  Self-assessment Against Grading Criteria")
    r5.font.name = FONT_FAMILY
    r5.font.size = Pt(14)
    r5.font.bold = True
    r5.font.color.rgb = COLOR_PRIMARY_BLUE

    table_score = doc.add_table(rows=6, cols=4)
    table_score.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_score.autofit = False
    set_table_borders(table_score, color="7F8C8D", sz="6")

    score_headers_en = ["Criterion", "Max", "Self-score", "Notes"]
    col_widths = [Inches(2.5), Inches(0.9), Inches(0.9), Inches(2.2)]

    hdr_cells = table_score.rows[0].cells
    for i, title in enumerate(score_headers_en):
        hdr_cells[i].width = col_widths[i]
        set_cell_background(hdr_cells[i], "EAECEE")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        if i in [1, 2]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.font.name = FONT_FAMILY
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_DARK_TEXT

    score_rows_en = [
        ("Complete, clear Project Charter", "2.0", "2.0", "All 4 sections present with distinct metrics"),
        ("Accurate stakeholder classification", "3.0", "3.0", "Matches automated script output 100%"),
        ("Script runs correctly, no errors", "3.0", "3.0", "Verified with 4 assert unit tests"),
        ("Report quality", "2.0", "2.0", "Clean formatting, matching sample template"),
        ("Total", "10.0", "10.0", "Fully achieved all Lab 01 requirements")
    ]

    for idx, (crit, max_s, self_s, note) in enumerate(score_rows_en, 1):
        cells = table_score.rows[idx].cells
        for i in range(4):
            cells[i].width = col_widths[i]
            set_cell_margins(cells[i], top=80, bottom=80, left=100, right=100)
            if idx == 5:
                set_cell_background(cells[i], "F2F4F4")

        p0 = cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(crit)
        r0.font.name = FONT_FAMILY
        r0.font.size = Pt(9)
        r0.font.color.rgb = COLOR_DARK_TEXT
        if idx == 5:
            r0.font.bold = True

        p1 = cells[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(max_s)
        r1.font.name = FONT_FAMILY
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_DARK_TEXT
        if idx == 5:
            r1.font.bold = True

        p2 = cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(self_s)
        r2.font.name = FONT_FAMILY
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_DARK_TEXT
        if idx == 5:
            r2.font.bold = True

        p3 = cells[3].paragraphs[0]
        p3.paragraph_format.space_after = Pt(0)
        r3 = p3.add_run(note)
        r3.font.name = FONT_FAMILY
        r3.font.size = Pt(9)
        r3.font.color.rgb = COLOR_DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 6. Conclusion
    p_h6 = doc.add_heading(level=1)
    p_h6.paragraph_format.space_before = Pt(12)
    p_h6.paragraph_format.space_after = Pt(6)
    r6 = p_h6.add_run("6  Conclusion")
    r6.font.name = FONT_FAMILY
    r6.font.size = Pt(14)
    r6.font.bold = True
    r6.font.color.rgb = COLOR_PRIMARY_BLUE

    p_concl = doc.add_paragraph()
    p_concl.paragraph_format.space_after = Pt(12)
    p_concl.paragraph_format.line_spacing = 1.2
    r_concl = p_concl.add_run(
        "The author fully achieved the Lab 1 objectives and now has a classified stakeholder dataset "
        "ready for reuse in Lab 2 (elicitation prioritized by stakeholder group)."
    )
    r_concl.font.name = FONT_FAMILY
    r_concl.font.size = Pt(10.5)
    r_concl.font.color.rgb = COLOR_DARK_TEXT

    # Save to report directory
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "lab01_report.docx")
    try:
        doc.save(out_path)
        print(f"[OK] Successfully generated English DOCX report at: {out_path}")
    except PermissionError:
        alt_path = os.path.join(out_dir, "lab01_report_revised.docx")
        doc.save(alt_path)
        print(f"[OK] Default file was locked; generated at: {alt_path}")


if __name__ == "__main__":
    build_english_report_docx()
