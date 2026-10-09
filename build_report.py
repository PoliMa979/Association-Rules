from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "polina_maltseva_a04_report.pdf"

PAGE_W, PAGE_H = A4
BLUE = colors.HexColor("#2E5FA3")
DARK = colors.HexColor("#25344D")
MID = colors.HexColor("#64748B")
PALE = colors.HexColor("#E8EEF7")
ALT = colors.HexColor("#F3F6FA")
LINE = colors.HexColor("#CCD6E4")
WHITE = colors.white


def register_fonts():
    candidates = [
        ("/System/Library/Fonts/Supplemental/Arial.ttf", "Arial"),
        ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", "Arial-Bold"),
        ("/System/Library/Fonts/Supplemental/Arial Italic.ttf", "Arial-Italic"),
    ]
    for path, name in candidates:
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont(name, path))


register_fonts()
BODY_FONT = "Arial" if "Arial" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
BOLD_FONT = "Arial-Bold" if "Arial-Bold" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Bold"
ITALIC_FONT = "Arial-Italic" if "Arial-Italic" in pdfmetrics.getRegisteredFontNames() else "Helvetica-Oblique"


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="ReportBody",
        parent=styles["BodyText"],
        fontName=BODY_FONT,
        fontSize=8.8,
        leading=11.1,
        textColor=DARK,
        spaceAfter=5.2,
        alignment=TA_LEFT,
    )
)
styles.add(
    ParagraphStyle(
        name="ReportBullet",
        parent=styles["ReportBody"],
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading1"],
        fontName=BODY_FONT,
        fontSize=13.5,
        leading=16,
        textColor=BLUE,
        spaceBefore=5,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Subsection",
        parent=styles["Heading2"],
        fontName=BODY_FONT,
        fontSize=10.3,
        leading=12.5,
        textColor=DARK,
        spaceBefore=4,
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="TitleKicker",
        parent=styles["BodyText"],
        fontName=BODY_FONT,
        fontSize=8.5,
        leading=10,
        textColor=BLUE,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName=BODY_FONT,
        fontSize=19,
        leading=22,
        textColor=DARK,
        alignment=TA_CENTER,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="Meta",
        parent=styles["BodyText"],
        fontName=BODY_FONT,
        fontSize=8.3,
        leading=10.4,
        textColor=DARK,
        alignment=TA_CENTER,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="Caption",
        parent=styles["BodyText"],
        fontName=BODY_FONT,
        fontSize=7.2,
        leading=9,
        textColor=MID,
        alignment=TA_CENTER,
        spaceBefore=3,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="Reference",
        parent=styles["BodyText"],
        fontName=BODY_FONT,
        fontSize=7.15,
        leading=9,
        textColor=DARK,
        leftIndent=12,
        firstLineIndent=-12,
        spaceAfter=3.5,
        splitLongWords=True,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="Formula",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8.1,
        leading=11,
        textColor=DARK,
        leftIndent=8,
        rightIndent=8,
        spaceBefore=4,
        spaceAfter=4,
    )
)


def p(text, style="ReportBody"):
    return Paragraph(text, styles[style])


def bullet(text):
    return p(f"- {text}", "ReportBullet")


def section(number, title):
    return p(f"{number}. {title}", "Section")


def subsection(title):
    return p(title, "Subsection")


def table(data, widths, header=True, font_size=7.3, alignments=None):
    converted = []
    for row_i, row in enumerate(data):
        converted_row = []
        for value in row:
            style = ParagraphStyle(
                name=f"Cell{row_i}",
                parent=styles["ReportBody"],
                fontName=BOLD_FONT if header and row_i == 0 else BODY_FONT,
                fontSize=font_size,
                leading=font_size + 2,
                textColor=WHITE if header and row_i == 0 else colors.black,
                spaceAfter=0,
            )
            converted_row.append(Paragraph(str(value), style))
        converted.append(converted_row)

    result = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ]
        )
        first_data_row = 1
    else:
        first_data_row = 0
    for row_i in range(first_data_row, len(data)):
        if (row_i - first_data_row) % 2 == 1:
            commands.append(("BACKGROUND", (0, row_i), (-1, row_i), ALT))
    if alignments:
        for col_i, alignment in enumerate(alignments):
            commands.append(("ALIGN", (col_i, first_data_row), (col_i, -1), alignment))
    result.setStyle(TableStyle(commands))
    return result


def formula_box(lines):
    content = "<br/>".join(lines)
    box = Table([[Paragraph(content, styles["Formula"])]], colWidths=[166 * mm])
    box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE),
                ("BOX", (0, 0), (-1, -1), 0.7, BLUE),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return box


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.45)
    canvas.line(18 * mm, PAGE_H - 18 * mm, PAGE_W - 18 * mm, PAGE_H - 18 * mm)
    canvas.setFont(BODY_FONT, 7.1)
    canvas.setFillColor(BLUE)
    canvas.drawString(18 * mm, PAGE_H - 14 * mm, "AI-ASSISTED STUDENT REPORT")
    canvas.setFillColor(MID)
    canvas.drawRightString(PAGE_W - 18 * mm, PAGE_H - 14 * mm, "LLM4Rec | Assignment A04")

    canvas.line(18 * mm, 15 * mm, PAGE_W - 18 * mm, 15 * mm)
    canvas.setFont(BODY_FONT, 7.1)
    canvas.setFillColor(MID)
    canvas.drawString(18 * mm, 11 * mm, "Association Rule Mining on UCI Online Retail")
    canvas.drawRightString(PAGE_W - 18 * mm, 11 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_story():
    story = [Spacer(1, 9 * mm)]
    story.extend(
        [
            p("LLM4REC | ASSIGNMENT A04", "TitleKicker"),
            p("Apriori Association Rules on UCI Online Retail:<br/>Thresholds, Direction, and Validation", "ReportTitle"),
            p("Student: Polina Maltseva&nbsp;&nbsp;&nbsp;&nbsp; Team: Individual", "Meta"),
            p("Email: pdmaltseva@edu.hse.ru&nbsp;&nbsp;&nbsp;&nbsp; Date: 2026-10-09", "Meta"),
            p("Assignment: A04 - Association Rules (Week 4)", "Meta"),
            Spacer(1, 4 * mm),
            subsection("Abstract"),
            p(
                "Association-rule mining can turn retail baskets into interpretable cross-sell candidates, but raw co-occurrence may overstate business value. "
                "I implemented set-based basket construction, an inverted-index Apriori miner, bidirectional rule generation, and guarded support, confidence, and lift calculations for 17,080 cleaned UCI Online Retail invoices. "
                "At 1% support and 30% confidence the system found 1,219 frequent itemsets and 950 rules; tightening the thresholds to 3% and 60% left 115 itemsets and 5 rules. "
                "The strongest actionable pair was GREEN REGENCY TEACUP AND SAUCER -&gt; ROSES REGENCY TEACUP AND SAUCER (support 3.17%, confidence 78.29%, lift 17.14), while a popular-item rule with lift 1.21 was rejected."
            ),
            p("Index Terms - association rules, Apriori, market basket analysis, support, confidence, lift", "ReportBody"),
            section("1", "Introduction"),
            p(
                "The goal is to discover interpretable item affinities in retail invoices. Each invoice is treated as one transaction, StockCode is the item identity, and Description is used only as a human-readable label. The practical question is whether seeing item A in a basket changes the likelihood of also seeing item B enough to justify a cross-sell or bundle experiment."
            ),
            p(
                "The starter application runs entirely in the browser and exposes support and confidence controls. The implementation preserves that interface, constructs a sparse logical invoice-item matrix through posting lists, mines frequent itemsets with Apriori, and generates rules in both directions."
            ),
            subsection("Contributions"),
            bullet("Implemented all seven required TODO(hw4) functions, including defensive zero-denominator handling and both-direction rule generation."),
            bullet("Compared two threshold settings, verified one rule directly from counts, and separated an actionable rule from a weak popular-item association."),
            section("2", "Related Work"),
            p(
                "The assignment starter and cleaned transaction export come from the instructor's Week 4 repository [1]. The underlying UCI Online Retail source contains 541,909 line items recorded from December 2010 through December 2011 [2]. Apriori uses the downward-closure property to avoid counting candidates whose subsets are not frequent [3]. Brin, Motwani, and Silverstein show why support and confidence alone can confuse association with meaningful correlation [4]."
            ),
            p(
                "Alternatives considered. FP-Growth avoids explicit candidate generation and can be faster at very low support, but Apriori was selected because its level-wise pruning is directly visible and matches the teaching objective. A dense 17,080 by 3,653 Boolean matrix was avoided; an inverted index represents the same binary membership relation with less memory. Repeated full basket scans were also rejected in favor of posting-list intersection."
            ),
        ]
    )

    story.append(PageBreak())
    story.extend(
        [
            section("3", "Method"),
            subsection("Representation and counting"),
            p(
                "Every decoded invoice is converted to a set of distinct StockCode values in first-appearance order. The buildIndex helper maps each stock code to the set of basket identifiers containing it. countItemset first removes duplicate requested codes, selects the shortest posting list, and counts identifiers present in every remaining list. This makes basket membership binary even if an invoice contains multiple units or duplicate rows."
            ),
            subsection("Metrics"),
            p("For N baskets, the implementation uses the assignment definitions:"),
            formula_box(
                [
                    "support(A -&gt; B)    = count(A U B) / N",
                    "confidence(A -&gt; B) = count(A U B) / count(A)",
                    "lift(A -&gt; B)       = confidence(A -&gt; B) / (count(B) / N)",
                ]
            ),
            Spacer(1, 2 * mm),
            p(
                "Each metric returns both a numeric value and a defined flag. N = 0, count(A) = 0, and count(B) = 0 are handled explicitly, so the interface never emits Infinity or NaN. Confidence is directional because its denominator changes; lift is symmetric because the joint probability is divided by both marginal probabilities."
            ),
            subsection("Apriori and rule generation"),
            p(
                "The miner starts with frequent single items. At each level it joins itemsets sharing the same prefix, removes duplicate candidates, and applies downward-closure pruning: every size k - 1 subset must appear in the previous frequent level. Surviving candidates are counted by posting-list intersection. The loop stops when no candidates remain."
            ),
            p(
                "For every frequent itemset of size at least two, a bit mask enumerates each non-empty proper antecedent; the complement becomes the consequent. Complementary masks naturally generate A -&gt; B and B -&gt; A. The rule list is filtered by confidence and sorted by lift, confidence, and support."
            ),
            subsection("Implementation configuration"),
            table(
                [
                    ["Component", "Configuration"],
                    ["Dataset", "17,080 baskets; 3,653 distinct StockCode items"],
                    ["Basket semantics", "One InvoiceNo; duplicate item rows counted once"],
                    ["Representation", "Sparse stock-to-basket inverted index"],
                    ["Miner", "Apriori with join and downward-closure pruning"],
                    ["Final thresholds", "Support &gt;= 3%; confidence &gt;= 60%; retain lift &gt; 1"],
                    ["Runtime", "Browser JavaScript; Node.js 24.19.0 used for reproducible checks"],
                    ["Verification", "11 self-checks plus two full-data threshold runs"],
                ],
                [42 * mm, 124 * mm],
                font_size=7.5,
            ),
            p("Table 1. Fixed implementation and evaluation settings.", "Caption"),
            subsection("Manual arithmetic sanity check"),
            p(
                "For GREEN REGENCY TEACUP AND SAUCER (A) -&gt; ROSES REGENCY TEACUP AND SAUCER (B), N = 17,080, count(A) = 691, count(B) = 780, and count(A U B) = 541."
            ),
            formula_box(
                [
                    "support    = 541 / 17,080 = 0.031674 = 3.1674%",
                    "confidence = 541 / 691    = 0.782923 = 78.2923%",
                    "lift       = 0.782923 / (780 / 17,080) = 17.1440",
                ]
            ),
            Spacer(1, 2 * mm),
            p(
                "The values match the program output. Reversing the rule changes confidence to 541 / 780 = 69.3590%, while lift remains 17.1440."
            ),
        ]
    )

    story.append(PageBreak())
    story.extend(
        [
            section("4", "Experiments"),
            p(
                "Setup. The full cleaned export was decoded in memory and mined twice. The first run used the starter defaults (1% support, 30% confidence). The second run used the final conservative setting (3% support, 60% confidence). Support changes frequent-itemset discovery; confidence only changes which rule directions are retained."
            ),
            subsection("Threshold trade-off"),
            table(
                [
                    ["Support", "Confidence", "Min count", "L1", "L2", "L3", "L4", "Itemsets", "Rules"],
                    ["1%", "30%", "171", "691", "413", "109", "6", "1,219", "950"],
                    ["3%", "60%", "513", "109", "6", "0", "0", "115", "5"],
                ],
                [18 * mm, 20 * mm, 20 * mm, 15 * mm, 15 * mm, 15 * mm, 15 * mm, 24 * mm, 20 * mm],
                font_size=7.1,
                alignments=["CENTER"] * 9,
            ),
            p("Table 2. Frequent itemsets by size and generated rule counts for two threshold settings.", "Caption"),
            p(
                "Raising support removed 1,104 itemsets and eliminated all frequent triples and quadruples. This follows directly from downward closure: once a pair is infrequent, every larger set containing it is pruned. Raising confidence further reduced the number of surviving directions. The final 3%/60% setting leaves five rules, all with lift above 1, and requires at least 513 joint baskets; this is more interpretable and more actionable than a 950-row rule table."
            ),
            subsection("Useful and weak rules"),
            table(
                [
                    ["Decision", "A", "B", "Joint", "count(A)", "count(B)", "Support", "Confidence", "Lift"],
                    ["Investigate", "GREEN REGENCY TEACUP", "ROSES REGENCY TEACUP", "541", "691", "780", "3.17%", "78.29%", "17.14"],
                    ["Reject", "REGENCY CAKESTAND 3 TIER", "WHITE HANGING HEART", "234", "1,681", "1,959", "1.37%", "13.92%", "1.21"],
                ],
                [19 * mm, 32 * mm, 32 * mm, 14 * mm, 17 * mm, 17 * mm, 18 * mm, 21 * mm, 14 * mm],
                font_size=6.5,
                alignments=["LEFT", "LEFT", "LEFT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT", "RIGHT"],
            ),
            p("Table 3. One actionable rule and one diagnostic low-threshold rule to reject.", "Caption"),
            p(
                "Useful rule. The teacup rule has 541 joint baskets, an antecedent count of 691, 78.29% confidence, and lift 17.14. Its reverse direction is also strong but less confident (69.36%). A cross-sell panel or two-color bundle is plausible because both directions have substantial counts and the association is far above the marginal purchase rate."
            ),
            p(
                "Weak rule. The cake stand -&gt; white heart rule appeared only in a diagnostic 1% support, 10% confidence run. The 234 joint baskets may look substantial, but confidence is only 13.92% versus an 11.47% baseline for the very popular white heart item; lift is just 1.21. Its small incremental signal and unrelated product semantics make it a poor intervention candidate, so the 60% final confidence threshold correctly excludes it."
            ),
            subsection("Verification"),
            p(
                "All 11 supplied checks passed: item and pair counts, lift equal to/above/below 1, directional confidence, duplicate handling, empty-state rendering, threshold validation, zero-denominator guards, frequent itemsets, and rule generation. On the bundled Node runtime the 1%/30% full-data run completed in about 2.3 seconds and the 3%/60% run in about 0.13 seconds; these timings are diagnostics, not performance claims."
            ),
        ]
    )

    story.append(PageBreak())
    story.extend(
        [
            section("5", "Discussion"),
            subsection("Business action and limitation"),
            p(
                "The first experiment would place ROSES REGENCY TEACUP AND SAUCER as a companion recommendation when GREEN REGENCY TEACUP AND SAUCER is viewed or added to a basket. A second treatment could offer a two-color bundle without an automatic discount, allowing the experiment to separate placement effects from price effects. The most important limitation is customer mix: the source includes wholesalers, whose coordinated purchases can produce high lift without representing an ordinary retail preference."
            ),
            subsection("Association is not causation"),
            p(
                "Lift 17.14 states that the two teacup variants co-occur much more often than independence predicts; it does not show that promoting green teacups causes rose teacup purchases. Plausible confounders include shared product-line exposure, collectors buying matching colors, wholesale restocking, promotions, seasonality, and long baskets. A recommendation intervention can also cannibalize purchases that would have happened anyway."
            ),
            subsection("Validation before action"),
            p(
                "The exported starter contains baskets but no usable per-basket timestamp, even though the UCI source includes InvoiceDate. Temporal values must not be simulated. With a later dated extract, I would recompute count(A), count(B), joint count, confidence, and lift in a pre-specified later window. The rule would proceed only if count(A) is at least 200, confidence remains at least 60%, and the lower bound of a bootstrap interval for lift exceeds 1."
            ),
            p(
                "Next, shoppers who view or add the green teacup would be randomly assigned to control (standard page) or treatment (rose teacup companion placement). The primary metric would be incremental rose-teacup attach rate; secondary metrics would be order margin, total revenue, returns, and substitution. Deployment would require a positive confidence interval for incremental attach rate and no material guardrail deterioration."
            ),
            subsection("Failure case, root cause, and fix"),
            p(
                "Failure case. The automated visual smoke test could not open the local file URL because the embedded browser blocks file:// navigation. Root cause. This was an execution-environment security policy, not an application exception. Fix and verification. The same transactions.js and script.js files were evaluated with Node's VM API, a minimal DOM object exercised the empty-state renderer, all 11 self-checks passed, and the full dataset was mined twice. A final human browser check remains appropriate before submission."
            ),
            subsection("What worked"),
            bullet("Posting-list intersection made the full-data runs fast without materializing a dense matrix."),
            bullet("Downward-closure pruning reduced the candidate space sharply at the higher support threshold."),
            bullet("Generating both directions exposed a 78.29% versus 69.36% confidence difference while preserving lift."),
            subsection("What surprised me or did not work"),
            bullet("The default 1%/30% setting produced 950 rules, which is too many for direct business review."),
            bullet("High lift can occur among product variants because product taxonomy and merchandising create strong shared context."),
            bullet("The cleaned starter cannot support temporal stability analysis because dates are not exported."),
            subsection("Next improvement"),
            p(
                "With more time, I would add a dated evaluation pipeline that reports period-over-period confidence and lift with uncertainty intervals, then use the stable-rule subset to power a controlled cross-sell experiment."
            ),
        ]
    )

    story.append(PageBreak())
    story.extend(
        [
            section("6", "AI Usage Disclosure"),
            subsection("Tools used"),
            p(
                "OpenAI Codex desktop was used for source inspection, JavaScript implementation, debugging, automated checks, experiment execution, reference verification, and PDF generation. The reproducible checks used the bundled Node.js 24.19.0 runtime; the report was generated with Python 3.12.14 and ReportLab 4.4.9."
            ),
            subsection("How AI was used"),
            bullet("Code generation and editing: implemented the seven TODO(hw4) functions while preserving the starter interface and provided scaffolding."),
            bullet("Debugging and testing: executed the supplied 11-check harness and two full-data threshold runs."),
            bullet("Analysis: computed rule counts, selected useful and weak rules, and derived a validation plan."),
            bullet("Documentation: checked the UCI source and primary Apriori/correlation papers, then formatted this report."),
            subsection("Verification performed in this work"),
            p(
                "The code output was cross-checked three ways: the supplied five-basket fixture passed all 11 checks; the selected rule was recomputed directly from integer counts in Section 3; and both threshold settings were re-run from the unchanged embedded transaction export. The local file URL could not be opened in the embedded browser, so no independent visual browser execution by the student is claimed here. The student should perform that final check before submission."
            ),
            subsection("What remains unverified"),
            p(
                "No later-period stability claim or causal sales impact is made because the starter has no timestamped evaluation split and no experiment data. The proposed A/B test is a plan, not an observed result."
            ),
            subsection("Session log"),
            p(
                "The complete tool-native session should be exported separately as polina_maltseva_a04_session.json and submitted as the audit trail."
            ),
            p("References", "Section"),
            p(
                "[1] S. Jin, \"RecSys-LLMs: HW4 - Association Rules (Week 4),\" GitHub repository, 2026. [Online]. Available: https://github.com/dryjins/RecSys-LLMs/tree/main/week4. [Accessed: 2026-10-09].",
                "Reference",
            ),
            p(
                "[2] D. Chen, \"Online Retail,\" UCI Machine Learning Repository, 2015, doi: 10.24432/C5BW33. [Online]. Available: https://archive.ics.uci.edu/dataset/352/online+retail. [Accessed: 2026-10-09].",
                "Reference",
            ),
            p(
                "[3] R. Agrawal and R. Srikant, \"Fast Algorithms for Mining Association Rules in Large Databases,\" in Proc. 20th Int. Conf. Very Large Data Bases (VLDB), Santiago, Chile, 1994, pp. 487-499. [Online]. Available: https://www.vldb.org/conf/1994/P487.PDF. [Accessed: 2026-10-09].",
                "Reference",
            ),
            p(
                "[4] S. Brin, R. Motwani, and C. Silverstein, \"Beyond Market Baskets: Generalizing Association Rules to Correlations,\" in Proc. ACM SIGMOD Int. Conf. Management of Data, 1997, pp. 265-276, doi: 10.1145/253260.253327.",
                "Reference",
            ),
        ]
    )
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=22 * mm,
        bottomMargin=20 * mm,
        title="A04 Association Rules Report",
        author="Polina Maltseva",
        subject="LLM4Rec Assignment A04",
    )
    doc.build(build_story(), onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
