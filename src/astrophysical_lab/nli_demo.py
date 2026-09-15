from astrophysical_lab.literature.arxiv_client import search_papers
from astrophysical_lab.literature.nli import NLIClassifier
from astrophysical_lab.literature.retriever import SemanticRetriever


QUESTION = (
    "Are short-period giant planets preferentially found "
    "around metal-rich stars?"
)

LITERATURE_CLAIM = (
    "Giant planets are more common around metal-rich stars than around metal-poor stars."
)

ARXIV_QUERY = (
    'cat:astro-ph.EP AND '
    '(all:"giant planet" OR all:"hot Jupiter") AND '
    'all:metallicity'
)


def main() -> None:
    print("Retrieving papers...")

    papers = search_papers(
        ARXIV_QUERY,
        max_results=20,
    )

    print(f"Retrieved {len(papers)} papers.")

    print("\nRunning semantic retrieval...")

    retriever = SemanticRetriever()

    passages = retriever.retrieve(
        question=LITERATURE_CLAIM,
        papers=papers,
        top_k=5,
    )

    print("\nRunning NLI...")

    classifier = NLIClassifier()

    assessments = classifier.assess(
        claim=LITERATURE_CLAIM,
        passages=passages,
    )

    print("\nSCIENTIFIC EVIDENCE")
    print("=" * 70)

    print(f"\nClaim:\n{LITERATURE_CLAIM}")

    for rank, evidence in enumerate(
        assessments,
        start=1,
    ):
        print()
        print("-" * 70)
        print(f"{rank}. {evidence.paper_title}")
        print(f"   arXiv: {evidence.paper_id}")

        print(
            f"   retrieval similarity: "
            f"{evidence.retrieval_similarity:.3f}"
        )

        print()
        print(f"   {evidence.passage}")

        print()
        print(
            f"   assessment: {evidence.label.upper()}"
        )

        print()
        print(
            f"   raw NLI prediction: "
            f"{evidence.raw_nli_label.upper()} "
            f"({evidence.confidence:.3f})"
        )

        print(
            "   "
            f"support={evidence.support_score:.3f} | "
            f"neutral={evidence.neutral_score:.3f} | "
            f"contradict={evidence.contradict_score:.3f}"
        )

        print("   note: heuristic language-model assessment")


if __name__ == "__main__":
    main()