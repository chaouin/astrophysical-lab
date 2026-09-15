import pandas as pd
from scipy.stats import mannwhitneyu

from astrophysical_lab.models import PopulationSummary, StatisticalResult


# Significance threshold used to decide whether the observed difference
# between the two populations is statistically detectable.
#
# If p-value < 0.05, we reject the null hypothesis that the two
# populations behave similarly.
ALPHA = 0.05


def summarize_population(
    name: str,
    dataframe: pd.DataFrame,
) -> PopulationSummary:
    """Compute descriptive metallicity statistics for a population."""

    # st_met represents stellar metallicity [Fe/H].
    # Positive values indicate a star richer in metals than the Sun,
    # while negative values indicate a more metal-poor star.
    metallicity = dataframe["st_met"]

    # These descriptive statistics tell us what the population looks like,
    # but do not yet tell us whether differences between populations
    # are statistically meaningful.
    return PopulationSummary(
        name=name,
        sample_size=len(metallicity),
        mean_metallicity=float(metallicity.mean()),
        median_metallicity=float(metallicity.median()),
    )


def compare_metallicity(
    short_period_giants: pd.DataFrame,
    comparison_giants: pd.DataFrame,
    alpha: float = ALPHA,
) -> StatisticalResult:
    """Compare stellar metallicity between two giant-planet populations."""

    # Extract metallicity measurements and remove missing observations.
    short_met = short_period_giants["st_met"].dropna()
    comparison_met = comparison_giants["st_met"].dropna()

    # A statistical comparison is impossible if one of the two
    # populations contains no usable metallicity measurements.
    if short_met.empty or comparison_met.empty:
        raise ValueError(
            "Both populations must contain metallicity observations."
        )

    # Mann-Whitney U is a non-parametric test.
    #
    # It evaluates whether metallicity values in one population tend
    # to be systematically higher or lower than those in the other,
    # without assuming that metallicity follows a normal distribution.
    #
    # "two-sided" tests for any difference between the populations,
    # regardless of direction.
    result = mannwhitneyu(
        short_met,
        comparison_met,
        alternative="two-sided",
    )

    n_short = len(short_met)
    n_comparison = len(comparison_met)

    # Statistical significance alone does not tell us how large the
    # difference is. We therefore compute a rank-biserial correlation
    # as an effect-size measure.
    #
    # Values are approximately between -1 and +1:
    #
    #   near  0 -> little difference between the populations
    #   > 0     -> short-period population tends to have higher metallicity
    #   < 0     -> comparison population tends to have higher metallicity
    #
    # The closer the absolute value is to 1, the stronger the separation.
    rank_biserial = (
        2 * float(result.statistic) / (n_short * n_comparison)
    ) - 1

    # The Mann-Whitney test tells us whether a difference exists,
    # but our scientific hypothesis also predicts a direction:
    #
    # hosts of short-period giant planets should have HIGHER metallicity.
    #
    # We compare the medians to determine whether the observed
    # difference goes in that predicted direction.
    median_short = float(short_met.median())
    median_comparison = float(comparison_met.median())

    # Interpret the statistical evidence.
    #
    # 1. If p >= alpha, there is not enough evidence to distinguish
    #    the two populations -> inconclusive.
    #
    # 2. If the difference is significant and short-period hosts have
    #    higher median metallicity -> hypothesis supported.
    #
    # 3. If the difference is significant but goes in the opposite
    #    direction -> hypothesis not supported.
    if result.pvalue >= alpha:
        conclusion = "inconclusive"
    elif median_short > median_comparison:
        conclusion = "supported"
    else:
        conclusion = "not_supported"

    # Return a structured result rather than raw numbers so that other
    # components of the pipeline can consume the evidence consistently.
    return StatisticalResult(
        test="Mann-Whitney U",
        statistic=float(result.statistic),
        p_value=float(result.pvalue),
        effect_size=rank_biserial,
        conclusion=conclusion,
    )