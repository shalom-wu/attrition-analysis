# Employee Attrition: Cost, Drivers, and a Retention Plan
### Data-driven retention strategy — prepared July 2026
*Analysis of 1,470 employees (Engineering, Sales, HR). Full methodology in Appendix.*

---

## Slide 1 — The problem: attrition costs us ~$8.7M a year

- **16.1% annual attrition** (237 departures / 1,470 employees) — at the high end of the 13–17% typical for mid-size tech/SaaS.
- Using a component-based replacement cost model (recruiting + onboarding + vacancy + ramp-up; see Appendix), the average departure costs **$36.6K ≈ 7.1 months of salary** — deliberately conservative vs. published benchmarks (SHRM: 6–9 months; Gallup: 0.5–2× salary).
- Total annual cost: **$8.67M, or 7.6% of total payroll ($114.7M)**.
- Sales bleeds fastest (20.6% attrition, $4.25M/yr); Engineering bleeds most in absolute dollars per head retained ($4.10M/yr at 13.8%).

| Department | Headcount | Attrition rate | Annual cost |
|---|---|---|---|
| Sales | 446 | 20.6% | $4.25M |
| Engineering | 961 | 13.8% | $4.10M |
| HR | 63 | 19.0% | $0.32M |

---

## Slide 2 — Where attrition concentrates: it's not random

Attrition is heavily concentrated in a few identifiable populations:

| Cut | Attrition rate | vs. company avg (16.1%) |
|---|---|---|
| **Working overtime** | **30.5%** | 2.9× the non-overtime rate (10.4%) |
| **First year at company** | **34.9%** | 4.3× the 10+ yr rate (8.1%) |
| **Job Level 1 (junior IC)** | **26.3%** | 2.7× Level 2 (9.7%) |
| **Bottom income quartile** | **29.3%** | 2.8× top quartile (10.3%) |
| **Frequent business travel** | **24.9%** | 3.1× non-travelers (8.0%) |
| Low job satisfaction (1/4) | 22.8% | 2.0× "very high" (11.3%) |

**The headline interaction: Junior + overtime = 52.6% attrition.** The 156 Level-1 employees working overtime produced 82 departures — **more than a third of all company attrition** — from 11% of headcount. Sales Representatives working overtime lost 2 in 3 people (66.7%).

*(Figures: `figures/attrition_joblevel_x_overtime.png`, `figures/attrition_by_tenureband.png`)*

---

## Slide 3 — What the predictive model confirms (and adds)

Two models trained (logistic regression + XGBoost); both rank the **same drivers**, which is what gives us confidence:

1. **Overtime** — strongest single predictor; doubles the odds of leaving (OR ≈ 2.0), holding everything else constant.
2. **Low pay / junior level / short tenure** — a correlated cluster; low monthly income and low stock option level are the top SHAP features after overtime.
3. **Frequent business travel** — OR ≈ 1.7, an underappreciated driver.
4. **Promotion stagnation** — years since last promotion **raises** attrition odds (OR ≈ 1.6 per SD) *once tenure is controlled for*. The raw data hides this (long-tenured people have both stale promotions and low attrition); the model surfaces it. Honest caveat: this driver shows up in the regression, not in the naive segment cut.
5. **Low environment/job satisfaction, distance from home, being single** — secondary but consistent.

**Model quality (held-out test set):** ROC-AUC 0.81 (logistic), 0.79 (XGBoost). At the chosen operating point the model catches **71% of true leavers while flagging only 33% of employees** — usable for prioritizing manager check-ins, not for automated decisions.

*(Figures: `figures/shap_summary.png`, `figures/roc_pr_curves.png`)*

---

## Slide 4 — Cost of inaction

If nothing changes, the run-rate is **$8.67M/yr, ~$26M over three years** (before headcount growth). Where it sits:

| Population | Leavers/yr | Annual replacement cost | Share of total cost |
|---|---|---|---|
| Overtime employees (n=416) | 127 | **$4.55M** | 52.5% |
| First-year employees (n=215) | 75 | $1.68M | 19.4% |
| Junior + overtime core (n=156) | 82 | $1.42M | 16.3% |

And the costs the model *excludes* — lost domain knowledge, customer relationship damage in Sales, team morale drag, manager time — all push the true number higher. Every dollar above is traceable to an explicit, conservative assumption.

*(Figure: `figures/cost_by_department.png`)*

---

## Slide 5 — Three intervention options

### Option A — Targeted overtime reduction (burnout program)
Target the 416 overtime employees, prioritizing the 156 junior+overtime core: on-call restructuring, workload rebalancing, comp-time policy, and a small backfill buffer (~4 hires) so overtime isn't structural.
- **Assumed effect:** 25% relative attrition reduction in this group (30.5% → 22.9% — still 2.2× the non-OT rate, so conservative). ≈ **32 fewer departures, $1.13M/yr saved.**
- **Cost:** ~$300K/yr (backfill buffer + program). **Net ≈ +$830K/yr, ~3.8× gross ROI.**
- **Tradeoff:** requires manager behavior change and some delivery-speed sacrifice; effect size unproven until piloted.

### Option B — Broad comp adjustment (bottom quartile +10%)
Raise the 369 bottom-quartile earners by 10%.
- **Cost:** ~$1.04M/yr **recurring**. **Assumed effect:** 25% relative reduction ≈ 27 fewer departures, but junior replacements are cheap (~$15K each) → only **$0.40M/yr saved. Net ≈ −$640K/yr.**
- **Verdict:** broad raises don't pay for themselves on replacement cost alone. Reserve *targeted* market-rate corrections for roles with proven external pay gaps — which requires comp benchmark data we don't have (flagged as open input).
- **Tradeoff:** strongest signal of investment in people; hardest to reverse; benefits stayers too (not captured in this model).

### Option C — First-year experience + promotion velocity
Structured 90-day onboarding, mentor/buddy program, and a defined L1→L2 promotion path with 12–18 month checkpoints (the model shows stalled promotions independently raise risk).
- **Assumed effect:** 20% relative reduction in first-year attrition (34.9% → 27.9%) ≈ **15 fewer departures, $0.34M/yr saved** — plus unquantified upside from promotion-velocity effects.
- **Cost:** ~$120K/yr. **Net ≈ +$215K/yr, ~2.8× gross ROI.**
- **Tradeoff:** cheapest and lowest-risk, but addresses only ~20% of the cost pool; effects take 2+ quarters to show.

---

## Slide 6 — Recommendation: A + C, model-assisted, piloted first

**Do Options A and C together; defer B pending market comp data.**

- Combined gross savings ≈ $1.47M/yr; after discounting ~15% for population overlap (first-year employees who also work overtime): **≈ $1.25M/yr saved for ~$420K/yr cost → net ≈ +$0.8M/yr, roughly 3× ROI.**
- Attrition rate impact: ~47 fewer departures ≈ **16.1% → ~13% company attrition**, moving us from the worst quartile to the middle of the tech benchmark band.
- **Use the model to sequence, not to decide:** the risk score prioritizes which teams get on-call restructuring and which new hires get the enhanced onboarding first. No automated or punitive use.
- **Pilot before scaling:** run Option A in the two highest-attrition Sales pods + one Engineering group for one quarter; a control-group comparison validates the assumed 25% effect size before full rollout.

**Key stated assumptions:** (1) effect sizes (25%/20% relative reductions) are industry-plausible but unproven here — the pilot exists to test them; (2) replacement costs are conservative (soft costs excluded); (3) salary figures are the dataset's — if real payroll is higher, savings scale linearly.

---

## Slide 7 — 12-month roadmap

| Quarter | Action | Owner | Success metric |
|---|---|---|---|
| Q1 | Overtime audit + pilot in 3 highest-risk teams; launch structured onboarding for all new hires | HRBP + Eng/Sales leads | Pilot vs. control attrition; onboarding NPS |
| Q2 | Read pilot results; scale Option A if ≥15% relative reduction observed; define L1→L2 promotion rubric | CHRO | Effect size confirmed; rubric shipped |
| Q3 | Full rollout; model-scored quarterly retention check-ins for top-risk decile | People Analytics | 71%+ of eventual leavers had a check-in |
| Q4 | Re-measure: target ≤14% trailing attrition; decide on targeted comp corrections with market data | CHRO + Finance | Attrition rate; $ saved vs. model |

---

## Slide 8 — Appendix: methodology & caveats

**Data.** IBM HR Analytics dataset (1,470 employees, 35 fields, no missing values; 3 constant columns dropped). "R&D" relabelled "Engineering" for narrative. **This is a synthetic, cross-sectional dataset** — a single snapshot, no dates, so attrition is treated as an annualized rate and no time-based validation is possible.

**Cost model (per departure).** Recruiting 20% of annual salary + onboarding 10% + vacancy (1.5–4 months × monthly salary, by level) + ramp-up (3–6 months at 50% productivity). Yields 55% of salary (junior) to 88% (exec); average $36.6K = 7.1 months of salary. Anchors: SHRM cost-per-hire and time-to-fill studies (~44-day average fill, longer for tech); SHRM 6–9-month replacement rule of thumb; Gallup 0.5–2× salary for fully-loaded cost. Soft costs deliberately excluded.

**Models.** 75/25 stratified split, 5-fold CV. Class imbalance (16% positive) handled with class weights / scale_pos_weight; accuracy deliberately not headlined. Logistic regression: test ROC-AUC 0.810, PR-AUC 0.562 (baseline 0.16), CV 0.842 ± 0.044. XGBoost: 0.785 / 0.522, CV 0.813 ± 0.033. The simpler model wins on this small dataset; we report both.

**Caveats (read before acting).**
1. Correlation ≠ causation — every intervention effect size is an assumption to be piloted, not a model output.
2. 237 positive cases → wide confidence intervals on per-role estimates.
3. No voluntary/involuntary split — some "attrition" may be terminations.
4. No external comp benchmarks — can't distinguish "paid low" from "paid below market."
5. Ethics: risk scores prioritize *support* (check-ins, workload relief), never punitive action; scores should not be visible in performance contexts.

**Open inputs needed from leadership:** real payroll scaling, market comp benchmarks, voluntary/involuntary attrition split, actual time-to-fill by role.
