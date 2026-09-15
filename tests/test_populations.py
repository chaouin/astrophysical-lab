import pandas as pd
import pytest

from astrophysical_lab.analysis.populations import build_giant_planet_host_populations


def test_build_giant_planet_host_populations():
    dataframe = pd.DataFrame(
        {
            "hostname": [
                "Star A",
                "Star A",
                "Star B",
                "Star C",
                "Star D",
            ],
            "pl_name": [
                "Planet A1",
                "Planet A2",
                "Planet B1",
                "Planet C1",
                "Planet D1",
            ],
            "pl_orbper": [
                5.0,  # short-period giant
                20.0,  # same host, longer-period giant
                30.0,  # comparison giant
                3.0,  # too small to be a giant
                4.0,  # too massive to be a planet in our definition
            ],
            "pl_bmassj": [
                1.0,
                2.0,
                1.5,
                0.1,
                20.0,
            ],
            "st_met": [
                0.20,
                0.20,
                -0.10,
                0.05,
                0.30,
            ],
        }
    )

    populations = build_giant_planet_host_populations(dataframe)

    short_hosts = populations.short_period_hosts
    comparison_hosts = populations.comparison_hosts

    # Star A should appear only once even though it has two giant planets.
    assert len(short_hosts) == 1
    assert short_hosts.iloc[0]["hostname"] == "Star A"

    # Star B hosts a giant planet, but not a short-period one.
    assert len(comparison_hosts) == 1
    assert comparison_hosts.iloc[0]["hostname"] == "Star B"

    # The two populations must not overlap.
    assert set(short_hosts["hostname"]).isdisjoint(set(comparison_hosts["hostname"]))


def test_missing_required_columns_raises_error():
    dataframe = pd.DataFrame(
        {
            "hostname": ["Star A"],
            "st_met": [0.1],
        }
    )

    with pytest.raises(ValueError, match="missing required columns"):
        build_giant_planet_host_populations(dataframe)
