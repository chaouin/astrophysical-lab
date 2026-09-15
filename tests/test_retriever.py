from astrophysical_lab.literature.retriever import split_into_passages
from astrophysical_lab.models import ScientificPaper


def test_split_into_passages_keeps_scientific_sentences():
    paper = ScientificPaper(
        paper_id="1234.5678",
        title="Test Paper",
        abstract=(
            "Giant planets are frequently observed around metal-rich stars. "
            "This is short. "
            "Their occurrence rate appears to depend strongly on stellar metallicity."
        ),
        authors=("Test Author",),
        published="2026-01-01",
        url="https://arxiv.org/abs/1234.5678",
    )

    passages = split_into_passages([paper])

    assert len(passages) == 2
    assert all(
        passage.paper_id == "1234.5678"
        for passage in passages
    )