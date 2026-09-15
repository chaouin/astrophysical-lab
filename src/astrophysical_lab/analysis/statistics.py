import pandas as pd
from scipy.stats import mannwhitneyu

from astrophysical_lab.config import SIGNIFICANCE_LEVEL
from astrophysical_lab.models import PopulationSummary, StatisticalResult


def summarize_population(
    name: str,
    dataframe: pd.DataFrame,
) -> PopulationSummary:
    """Compute descriptive metallicity statistics for a population."""

    # Stellar metallicity [Fe/H]: positive values are metal-rich
    # relative to the Sun, while negative values are metal-poor.
    metallicity = dataframe["st_met"]

    return PopulationSummary(
        name=name,
        sample_size=len(metallicity),
        mean_metallicity=float(metallicity.mean()),
        median_metallicity=float(metallicity.median()),
    )


def compare_metallicity(
    short_period_hosts: pd.DataFrame,
    comparison_hosts: pd.DataFrame,
    alpha: float = SIGNIFICANCE_LEVEL,
) -> StatisticalResult:
    """Compare stellar metallicity between two giant-planet populations."""

    short_met = short_period_hosts["st_met"].dropna()
    comparison_met = comparison_hosts["st_met"].dropna()

    if short_met.empty or comparison_met.empty:
        raise ValueError(
            "Both populations must contain metallicity observations."
        )

    # Mann-Whitney U is used because it does not assume normally
    # distributed metallicity values.
    result = mannwhitneyu(
        short_met,
        comparison_met,
        alternative="two-sided",
    )

    n_short = len(short_met)
    n_comparison = len(comparison_met)

    # Statistical significance does not indicate effect magnitude,
    # so we also report rank-biserial correlation.
    # Positive values indicate higher metallicity in the short-period group.
    rank_biserial = (
        2 * float(result.statistic) / (n_short * n_comparison)
    ) - 1

    median_short = float(short_met.median())
    median_comparison = float(comparison_met.median())

    # Significance establishes whether a difference is detectable;
    # the medians determine whether it follows the predicted direction.
    if result.pvalue >= alpha:
        conclusion = "inconclusive"
    elif median_short > median_comparison:
        conclusion = "supported"
    else:
        conclusion = "not_supported"

    return StatisticalResult(
        test="Mann-Whitney U",
        statistic=float(result.statistic),
        p_value=float(result.pvalue),
        effect_size=rank_biserial,
        conclusion=conclusion,
    )