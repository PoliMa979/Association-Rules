# LLM4Rec HW4: Association Rules

Individual Week 4 assignment for the HSE LLM4Rec course. The project mines association rules from the cleaned UCI Online Retail transaction baskets supplied with the course starter.

## Contents

- `week4/` - browser application and embedded cleaned transaction data.
- `week4/script.js` - basket counting, metric helpers, Apriori mining, and bidirectional rule generation.
- `output/pdf/polina_maltseva_a04_report.pdf` - final IEEE-aligned assignment report.
- `build_report.py` - reproducible ReportLab source for the PDF.
- `README_SUBMISSION.md` - final verification and submission checklist.

## Run

Open `week4/index.html` in a modern browser. No build step, package installation, or server is required.

1. Press **Run tests**. The expected result is `pass 11, fail 0, pending 0`.
2. Set minimum support and minimum confidence.
3. Press **Run rules** and click a rule to inspect its counts and reverse direction.

## Reproduced results

| Minimum support | Minimum confidence | Frequent itemsets | Rules |
|---:|---:|---:|---:|
| 1% | 30% | 1,219 | 950 |
| 3% | 60% | 115 | 5 |

Selected actionable rule:

`22697 GREEN REGENCY TEACUP AND SAUCER -> 22699 ROSES REGENCY TEACUP AND SAUCER`

- `count(A U B) = 541`
- `count(A) = 691`
- `count(B) = 780`
- support `3.1674%`
- confidence `78.2923%`
- lift `17.1440`

## Dataset

UCI Machine Learning Repository, Online Retail, dataset 352: https://archive.ics.uci.edu/dataset/352/online+retail

The course starter already provides the cleaned baskets in `week4/transactions.js`. That file is retained unchanged.

