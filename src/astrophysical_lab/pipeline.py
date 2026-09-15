from astrophysical_lab.config import (
    ARXIV_QUERY,
    DEFAULT_MAX_PAPERS,
    DEFAULT_TOP_K,
)
from astrophysical_lab.experiment import run_experiment
from astrophysical_lab.hypothesis import build_metallicity_hypothesis
from astrophysical_lab.literature.arxiv_client import search_papers
from astrophysical_lab.literature.nli import NLIClassifier
from astrophysical_lab.literature.retriever import SemanticRetriever
from astrophysical_lab.models import InvestigationReport


def investigate(
    max_papers: int = DEFAULT_MAX_PAPERS,
    top_k: int = DEFAULT_TOP_K,
) -> InvestigationReport:
    """Run the complete literature-to-evidence investigation."""

    hypothesis = build_metallicity_hypothesis()

    # Literature branch: retrieve and assess textual evidence.
    papers = search_papers(
        ARXIV_QUERY,
        max_results=max_papers,
    )

    retriever = SemanticRetriever()

    passages = retriever.retrieve(
        question=hypothesis.literature_claim,
        papers=papers,
        top_k=top_k,
    )

    classifier = NLIClassifier()

    evidence = classifier.assess(
        claim=hypothesis.literature_claim,
        passages=passages,
    )

    # Empirical branch: test the hypothesis independently on observational data.
    experiment = run_experiment()

    return InvestigationReport(
        hypothesis=hypothesis,
        literature_evidence=tuple(evidence),
        experiment=experiment,
    )