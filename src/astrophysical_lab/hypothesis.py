from astrophysical_lab.models import HypothesisSpec


def build_metallicity_hypothesis() -> HypothesisSpec:
    """Return the structured hypothesis used by the investigation."""

    return HypothesisSpec(
        question="Are short-period giant planets preferentially found around metal-rich stars?",
        statement=("Host stars of short-period giant planets have higher stellar metallicity "
                    "than other giant-planet hosts."),
        literature_claim=( "Giant planets are more common around metal-rich stars than around "
                           "metal-poor stars."),
        independent_variable="giant-planet host population",
        dependent_variable="stellar metallicity [Fe/H]",
        expected_relation="short-period hosts > comparison hosts",
        population_a="hosts with at least one giant planet with period <= 10 days",
        population_b="giant-planet hosts with no giant planet with period <= 10 days",
        statistical_test="Mann-Whitney U",
        data_source="NASA Exoplanet Archive",
    )