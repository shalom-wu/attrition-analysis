"""Load and clean the IBM HR attrition dataset.

The company is framed as a mid-size tech/SaaS firm: the "Research &
Development" department is relabelled "Engineering" and lab/research job
titles are mapped to tech equivalents. Labels only — no values change.
"""

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_CSV = REPO_ROOT / "data" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"

ROLE_MAP = {
    "Research Scientist": "Software Engineer",
    "Laboratory Technician": "QA / Support Engineer",
    "Research Director": "Engineering Director",
    "Manufacturing Director": "Platform / DevOps Lead",
    "Healthcare Representative": "Solutions Consultant",
}

SATISFACTION_LABELS = {1: "1 Low", 2: "2 Medium", 3: "3 High", 4: "4 Very High"}

TENURE_BINS = [-0.1, 1, 3, 6, 10, 100]
TENURE_LABELS = ["0-1 yr", "2-3 yrs", "4-6 yrs", "7-10 yrs", "10+ yrs"]


def load_raw(path: Path = RAW_CSV) -> pd.DataFrame:
    return pd.read_csv(path)


def quality_report(df: pd.DataFrame) -> list[str]:
    """Data quality notes for the raw dataset (documented, not auto-fixed)."""
    constant_cols = [c for c in df.columns if df[c].nunique() == 1]
    bad_tenure = df[
        (df["YearsAtCompany"] < df["YearsInCurrentRole"])
        | (df["YearsAtCompany"] < df["YearsWithCurrManager"])
        | (df["YearsAtCompany"] < df["YearsSinceLastPromotion"])
        | (df["TotalWorkingYears"] < df["YearsAtCompany"])
    ]
    return [
        f"Rows: {len(df)}, Columns: {df.shape[1]}",
        f"Missing values: {int(df.isna().sum().sum())}",
        f"Duplicate EmployeeNumber IDs: {int(df['EmployeeNumber'].duplicated().sum())}",
        f"Constant (zero-information) columns: {constant_cols}",
        f"Rows with internally inconsistent tenure fields: {len(bad_tenure)}",
        "PerformanceRating only takes values 3 and 4 — no low performers "
        "recorded, so it has almost no discriminative value.",
        "Single cross-sectional snapshot (synthetic, IBM-generated): no dates, "
        "so the 16.1% attrition is treated as an annualized rate for costing.",
    ]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Drop zero-variance columns, apply the tech-company framing, and add
    the derived fields used throughout the analysis."""
    out = df.copy()
    constant_cols = [c for c in out.columns if out[c].nunique() == 1]
    out = out.drop(columns=constant_cols)

    out["Department"] = out["Department"].replace(
        {"Research & Development": "Engineering"}
    )
    out["JobRole"] = out["JobRole"].replace(ROLE_MAP)

    out["AttritionFlag"] = (out["Attrition"] == "Yes").astype(int)
    out["TenureBand"] = pd.cut(
        out["YearsAtCompany"], bins=TENURE_BINS, labels=TENURE_LABELS
    )
    out["IncomeQuartile"] = pd.qcut(
        out["MonthlyIncome"], 4, labels=["Q1 (lowest)", "Q2", "Q3", "Q4 (highest)"]
    )
    out["JobSatisfactionLabel"] = out["JobSatisfaction"].map(SATISFACTION_LABELS)
    return out


def attrition_table(df: pd.DataFrame, col: str, sort_by_rate: bool = True) -> pd.DataFrame:
    """Attrition rate and headcount by a grouping column."""
    t = (
        df.groupby(col, observed=True)["AttritionFlag"]
        .agg(headcount="count", leavers="sum", attrition_rate="mean")
        .reset_index()
    )
    t["attrition_rate"] = (t["attrition_rate"] * 100).round(1)
    if sort_by_rate:
        t = t.sort_values("attrition_rate", ascending=False)
    return t
