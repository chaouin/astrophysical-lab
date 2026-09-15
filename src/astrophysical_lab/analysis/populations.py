from dataclasses import dataclass

import pandas as pd

from astrophysical_lab.config import (
    MAX_GIANT_MASS_JUPITER,
    MIN_GIANT_MASS_JUPITER,
    SHORT_PERIOD_DAYS,
)


@dataclass(frozen=True)
class GiantPlanetHostPopulations:
    short_period_hosts: pd.DataFrame
    comparison_hosts: pd.DataFrame


def build_giant_planet_host_populations(
    dataframe: pd.DataFrame,
) -> GiantPlanetHostPopulations:
    """Build independent host-star populations for the experiment.

    Giant planets are defined as planets with masses between
    0.3 and 13 Jupiter masses.

    A short-period host contains at least one giant planet with an
    orbital period <= 10 days.

    The comparison population contains giant-planet hosts with no
    short-period giant planet.
    """
    required_columns = {
        "hostname",
        "pl_name",
        "pl_orbper",
        "pl_bmassj",
        "st_met",
    }

    missing = required_columns - set(dataframe.columns)

    if missing:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing)}"
        )

    clean = dataframe.dropna(
        subset=[
            "hostname",
            "pl_orbper",
            "pl_bmassj",
            "st_met",
        ]
    ).copy()

    giants = clean[
        clean["pl_bmassj"].between(
            MIN_GIANT_MASS_JUPITER,
            MAX_GIANT_MASS_JUPITER,
            inclusive="both",
        )
    ].copy()

    giants = clean[
        clean["pl_bmassj"].between(
            MIN_GIANT_MASS_JUPITER,
            MAX_GIANT_MASS_JUPITER,
            inclusive="both",
        )
    ].copy()

    giants["has_short_period_giant"] = (
            giants["pl_orbper"] <= SHORT_PERIOD_DAYS
    )

    hosts = (
        giants.groupby("hostname", as_index=False)
        .agg(
            st_met=("st_met", "median"),
            has_short_period_giant=(
                "has_short_period_giant",
                "max",
            ),
            n_giant_planets=("pl_name", "nunique"),
            min_giant_period=("pl_orbper", "min"),
        )
    )

    short_period_hosts = hosts[
        hosts["has_short_period_giant"]
    ].copy()

    comparison_hosts = hosts[
        ~hosts["has_short_period_giant"]
    ].copy()

    return GiantPlanetHostPopulations(
        short_period_hosts=short_period_hosts,
        comparison_hosts=comparison_hosts,
    )