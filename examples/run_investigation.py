from astrophysical_lab.pipeline import investigate


def main() -> None:
    print("Running Astrophysical Lab investigation...")

    report = investigate()

    hypothesis = report.hypothesis
    experiment = report.experiment

    print()
    print("ASTROPHYSICAL LAB")
    print("=" * 70)

    print("\nSCIENTIFIC QUESTION")
    print(hypothesis.question)

    print("\nSTRUCTURED HYPOTHESIS")
    print(f"Statement: {hypothesis.statement}")
    print(f"Independent variable: {hypothesis.independent_variable}")
    print(f"Dependent variable: {hypothesis.dependent_variable}")
    print(f"Expected relation: {hypothesis.expected_relation}")
    print(f"Statistical test: {hypothesis.statistical_test}")
    print(f"Data source: {hypothesis.data_source}")

    print("\nLITERATURE CONTEXT")
    print("-" * 70)
    print(f"Claim: {hypothesis.literature_claim}")

    for index, evidence in enumerate(
        report.literature_evidence,
        start=1,
    ):
        print()
        print(f"{index}. [{evidence.label.upper()}] {evidence.paper_title}")
        print(
            f"   retrieval={evidence.retrieval_similarity:.3f} | "
            f"NLI={evidence.raw_nli_label} "
            f"({evidence.confidence:.3f})"
        )
        print(f"   {evidence.passage}")

    print("\nEMPIRICAL VALIDATION")
    print("-" * 70)

    short = experiment.short_period_hosts
    comparison = experiment.comparison_hosts
    stats = experiment.statistical_result

    print(
        f"{short.name}: "
        f"n={short.sample_size}, "
        f"median [Fe/H]={short.median_metallicity:.3f}"
    )

    print(
        f"{comparison.name}: "
        f"n={comparison.sample_size}, "
        f"median [Fe/H]={comparison.median_metallicity:.3f}"
    )

    print()
    print(f"Test: {stats.test}")
    print(f"p-value: {stats.p_value:.3e}")
    print(f"Effect size: {stats.effect_size:.3f}")

    print("\n EMPIRICAL CONCLUSION")
    print(stats.conclusion.upper())


if __name__ == "__main__":
    main()
