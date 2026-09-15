import pandas as pd
import pytest

from astrophysical_lab.analysis.statistics import (
    compare_metallicity,
    summarize_population,
)


def test_summarize_population():
    dataframe = pd.DataFrame(
        {
            "st_met": [0.0, 0.1, 0.2],
        }
    )

    summary = summarize_population(
        "Test population",
        dataframe,
    )

    assert summary.name == "Test population"
    assert summary.sample_size == 3
    assert summary.mean_metallicity == pytest.approx(0.1)
    assert summary.median_metallicity == pytest.approx(0.1)


def test_higher_metallicity_supports_hypothesis():
    short_period = pd.DataFrame(
        {
            "st_met": [0.30, 0.40, 0.50, 0.60, 0.70],
        }
    )

    comparison = pd.DataFrame(
        {
            "st_met": [-0.30, -0.20, -0.10, 0.00, 0.05],
        }
    )

    result = compare_metallicity(
        short_period,
        comparison,
    )

    assert result.test == "Mann-Whitney U"
    assert result.p_value < 0.05
    assert result.effect_size > 0
    assert result.conclusion == "supported"


def test_similar_populations_are_inconclusive():
    short_period = pd.DataFrame(
        {
            "st_met": [0.0, 0.1, 0.2, 0.3, 0.4],
        }
    )

    comparison = pd.DataFrame(
        {
            "st_met": [0.0, 0.1, 0.2, 0.3, 0.4],
        }
    )

    result = compare_metallicity(
        short_period,
        comparison,
    )

    assert result.p_value >= 0.05
    assert result.conclusion == "inconclusive"


def test_empty_population_raises_error():
    short_period = pd.DataFrame(
        {
            "st_met": [],
        }
    )

    comparison = pd.DataFrame(
        {
            "st_met": [0.0, 0.1, 0.2],
        }
    )

    with pytest.raises(
        ValueError,
        match="Both populations must contain",
    ):
        compare_metallicity(
            short_period,
            comparison,
        )
