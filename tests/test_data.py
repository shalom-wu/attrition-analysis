"""Sanity tests for data loading and cleaning."""

import pytest

from attrition import data as adata


@pytest.fixture(scope="module")
def clean_df():
    return adata.clean(adata.load_raw())


def test_raw_shape_matches_canonical_dataset():
    raw = adata.load_raw()
    assert raw.shape == (1470, 35)
    assert raw.isna().sum().sum() == 0
    assert raw["EmployeeNumber"].is_unique


def test_attrition_rate_matches_canonical_dataset(clean_df):
    # 237 of 1470 leavers = 16.12% in the published dataset
    assert clean_df["AttritionFlag"].sum() == 237
    assert clean_df["AttritionFlag"].mean() == pytest.approx(0.1612, abs=1e-3)


def test_constant_columns_dropped(clean_df):
    for col in ("EmployeeCount", "StandardHours", "Over18"):
        assert col not in clean_df.columns


def test_tech_reframing_is_labels_only(clean_df):
    raw = adata.load_raw()
    assert "Research & Development" not in clean_df["Department"].values
    # Same headcount before/after: relabelling must not move anyone
    assert (clean_df["Department"] == "Engineering").sum() == (
        raw["Department"] == "Research & Development"
    ).sum()


def test_derived_fields_present_and_complete(clean_df):
    for col in ("AttritionFlag", "TenureBand", "IncomeQuartile"):
        assert col in clean_df.columns
        assert clean_df[col].notna().all()
