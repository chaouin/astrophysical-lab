from astrophysical_lab.analysis.populations import build_giant_planet_host_populations
from astrophysical_lab.analysis.statistics import compare_metallicity,summarize_population
from astrophysical_lab.data.nasa_exoplanet import fetch_exoplanets
from astrophysical_lab.models import ExperimentResult
from astrophysical_lab.reporting import plot_metallicity_distributions,save_result_json


QUESTION = (
    "Are short-period giant planets preferentially found "
    "around metal-rich stars?"
)

HYPOTHESIS = (
    "Host stars of short-period giant planets have higher "
    "stellar metallicity than host stars of longer-period giant planets."
)


def run_experiment() -> ExperimentResult:
    """Run the complete metallicity experiment."""
    dataframe = fetch_exoplanets()

    populations = build_giant_planet_host_populations(dataframe)

    short_summary = summarize_population(
        "Hosts with short-period giants",
        populations.short_period_hosts,
    )

    comparison_summary = summarize_population(
        "Other giant-planet hosts",
        populations.comparison_hosts,
    )

    statistical_result = compare_metallicity(
        populations.short_period_hosts,
        populations.comparison_hosts,
    )

    result = ExperimentResult(
        question=QUESTION,
        hypothesis=HYPOTHESIS,
        short_period_hosts=short_summary,
        comparison_hosts=comparison_summary,
        statistical_result=statistical_result,
    )

    save_result_json(result)

    plot_metallicity_distributions(
        populations.short_period_hosts,
        populations.comparison_hosts,
    )

    return result


if __name__ == "__main__":
    result = run_experiment()

    print()
    print("ASTROPHYSICAL LAB")
    print("=" * 60)

    print(f"\nQuestion:\n{result.question}")
    print(f"\nHypothesis:\n{result.hypothesis}")

    print("\nPopulations")
    print("-" * 60)

    short = result.short_period_hosts
    comparison = result.comparison_hosts

    print(
        f"{short.name}: "
        f"n={short.sample_size}, "
        f"median metallicity={short.median_metallicity:.3f}"
    )

    print(
        f"{comparison.name}: "
        f"n={comparison.sample_size}, "
        f"median metallicity={comparison.median_metallicity:.3f}"
    )

    stats = result.statistical_result

    print("\nStatistical test")
    print("-" * 60)
    print(f"Test:        {stats.test}")
    print(f"Statistic:   {stats.statistic:.3f}")
    print(f"p-value:     {stats.p_value:.6f}")
    print(f"Effect size: {stats.effect_size:.3f}")

    print("\nEvidence")
    print("-" * 60)
    print(stats.conclusion.upper())
    print()