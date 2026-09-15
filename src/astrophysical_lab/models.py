from dataclasses import dataclass
from typing import Literal


EvidenceConclusion = Literal[
    "supported",
    "not_supported",
    "inconclusive",
]


@dataclass(frozen=True)
class PopulationSummary:
    name: str
    sample_size: int
    mean_metallicity: float
    median_metallicity: float


@dataclass(frozen=True)
class StatisticalResult:
    test: str
    statistic: float
    p_value: float
    effect_size: float
    conclusion: EvidenceConclusion


@dataclass(frozen=True)
class ExperimentResult:
    question: str
    hypothesis: str
    short_period_hosts: PopulationSummary
    comparison_hosts: PopulationSummary
    statistical_result: StatisticalResult


@dataclass(frozen=True)
class ScientificPaper:
    paper_id: str
    title: str
    abstract: str
    authors: tuple[str, ...]
    published: str
    url: str


@dataclass(frozen=True)
class ScientificPassage:
    paper_id: str
    paper_title: str
    text: str


@dataclass(frozen=True)
class RetrievedPassage:
    paper_id: str
    paper_title: str
    text: str
    similarity: float