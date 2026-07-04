# Written summary: attrition cost, drivers, and retention economics

*One-page companion to the [strategy deck](strategy_deck.md). All numbers
are reproducible from the pipeline in this repository.*

## The problem

A 1,470-employee tech company loses 16.1% of its people a year (237
departures) — the high end of the typical 13–17% band for mid-size
tech/SaaS. Leadership needs three things before committing budget: a
defensible dollar figure for the problem, evidence of what actually drives
it, and intervention options costed well enough to compare.

## What the attrition costs

A component-based model (recruiting 20% of salary + onboarding 10% +
vacancy 1.5–4 months + ramp-up 3–6 months at 50% productivity, tiered by
job level) prices the average departure at **$36.6K ≈ 7.1 months of
salary** — inside SHRM's 6–9-month replacement benchmark and conservative
against Gallup's 0.5–2× range. Annual total: **$8.67M, or 7.6% of
payroll.** Soft costs (knowledge loss, morale, customer damage) are
deliberately excluded, so this is a floor.

## What drives it

Descriptive cuts and two predictive models (logistic regression ROC-AUC
0.81; XGBoost 0.79; drivers agree across both and across SHAP/odds-ratio
views) converge on the same picture:

- **Overtime** doubles the odds of leaving — the single strongest signal.
  The junior-plus-overtime segment runs **52.6% attrition and produces a
  third of all departures from 11% of headcount**.
- **First-year employees** leave at 34.9%, 4.3× the 10-year+ rate.
- **Low pay / junior level** cluster: bottom-quartile earners leave at 29.3%.
- **Frequent business travel** (OR ≈ 1.7) and **promotion stagnation**
  (OR ≈ 1.6 per SD once tenure is controlled — invisible in raw cuts)
  round out the actionable drivers.

At the chosen operating threshold the model catches 71% of true leavers
while flagging 33% of employees — useful for prioritizing manager
check-ins, not for automated decisions.

## What to do about it

Three options were costed. Broad bottom-quartile raises **fail the ROI
test** (−$640K/yr net: $1.04M recurring cost vs $0.40M replacement-cost
savings, because junior replacements are cheap). The recommended package —
**targeted overtime reduction plus a first-year experience program** —
projects **≈$1.25M/yr gross savings for ~$420K/yr cost (≈3× ROI, ~47 fewer
departures/yr)**, sequenced by model risk scores and validated by a
one-quarter pilot with a control group before scaling.

## Honest limitations

The dataset is synthetic and cross-sectional (no dates → no survival
analysis or temporal validation); effects are correlational; intervention
effect sizes (−25%/−20% relative) are industry-plausible assumptions the
pilot is designed to test, not model outputs; voluntary and involuntary
exits are not distinguished; and there is no external comp benchmark. See
`outputs/model_report.md` for the full list.
