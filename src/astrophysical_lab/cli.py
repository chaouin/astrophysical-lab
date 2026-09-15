import argparse
import json
from dataclasses import asdict

from astrophysical_lab.config import DEFAULT_MAX_PAPERS, DEFAULT_TOP_K
from astrophysical_lab.models import InvestigationReport
from astrophysical_lab.pipeline import investigate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="astrolab",
        description=(
            "Investigate an astrophysical hypothesis using "
            "scientific literature and observational data."
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    investigate_parser = subparsers.add_parser(
        "investigate",
        help="Run the literature-to-evidence investigation.",
    )

    investigate_parser.add_argument(
        "--max-papers",
        type=int,
        default=DEFAULT_MAX_PAPERS,
        help=(
            "Maximum number of arXiv papers to retrieve "
            f"(default: {DEFAULT_MAX_PAPERS})."
        ),
    )

    investigate_parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=(
            "Number of scientific passages to retain "
            f"(default: {DEFAULT_TOP_K})."
        ),
    )

    investigate_parser.add_argument(
        "--json",
        action="store_true",
        help="Print the complete investigation report as JSON.",
    )

    return parser


def print_report(report: InvestigationReport) -> None:
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
        print(
            f"{index}. [{evidence.label.upper()}] "
            f"{evidence.paper_title}"
        )

        print(
            f"   retrieval={evidence.retrieval_similarity:.3f} | "
            f"NLI={evidence.raw_nli_label} "
            f"({evidence.confidence:.3f})"
        )

        print(f"   {evidence.passage}")

    short = experiment.short_period_hosts
    comparison = experiment.comparison_hosts
    stats = experiment.statistical_result

    print("\nEMPIRICAL VALIDATION")
    print("-" * 70)

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

    print("\nEMPIRICAL EVIDENCE")
    print(stats.conclusion.upper())


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command != "investigate":
        parser.error(f"Unknown command: {args.command}")

    report = investigate(
        max_papers=args.max_papers,
        top_k=args.top_k,
    )

    if args.json:
        print(
            json.dumps(
                asdict(report),
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print_report(report)


if __name__ == "__main__":
    main()