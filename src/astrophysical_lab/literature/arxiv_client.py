import arxiv

from astrophysical_lab.models import ScientificPaper


class ArxivRetrievalError(RuntimeError):
    """Raised when scientific papers cannot be retrieved from arXiv."""


def search_papers(
    query: str,
    max_results: int = 20,
) -> list[ScientificPaper]:
    """Retrieve scientific papers from arXiv.

    Params:
        - query: arXiv search query.
        - max_results: Maximum number of papers to retrieve.

    Returns:
        - list[ScientificPaper]: Structured paper metadata and abstracts.
    """
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )

    client = arxiv.Client()

    try:
        results = list(client.results(search))
    except Exception as exc:
        raise ArxivRetrievalError(
            "Could not retrieve papers from arXiv."
        ) from exc

    papers = []

    for result in results:
        paper_id = result.get_short_id()

        papers.append(
            ScientificPaper(
                paper_id=paper_id,
                title=" ".join(result.title.split()),
                abstract=" ".join(result.summary.split()),
                authors=tuple(
                    author.name
                    for author in result.authors
                ),
                published=result.published.date().isoformat(),
                url=result.entry_id,
            )
        )

    return papers