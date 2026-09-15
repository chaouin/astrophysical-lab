from astrophysical_lab.literature.arxiv_client import search_papers
from astrophysical_lab.literature.retriever import SemanticRetriever


QUESTION = (
    "Are short-period giant planets preferentially found around metal-rich stars?"
)

ARXIV_QUERY = (
    'cat:astro-ph.EP AND ' # Limit research to the arXiv category Earth and Planetary Astrophysics
    '(all:"giant planet" OR all:"hot Jupiter") AND ' # Article needs to contain the words "giant planet" or "hot jupiter"
    'all:metallicity' # Article needs to contain de word "metallicity"
)


def main() -> None:
    print("Retrieving papers from arXiv...")

    papers = search_papers(
        ARXIV_QUERY,
        max_results=20,
    )

    print(f"Retrieved {len(papers)} papers.")

    retriever = SemanticRetriever()

    passages = retriever.retrieve(
        question=QUESTION,
        papers=papers,
        top_k=5,
    )

    print("\nTOP SCIENTIFIC PASSAGES")
    print("=" * 70)

    for rank, passage in enumerate(passages, start=1):
        print()
        print(f"{rank}. {passage.paper_title}")
        print(f"   arXiv: {passage.paper_id}")
        print(f"   similarity: {passage.similarity:.3f}")
        print()
        print(f"   {passage.text}")


if __name__ == "__main__":
    main()