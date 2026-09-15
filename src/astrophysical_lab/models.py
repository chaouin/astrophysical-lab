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
    short_period_giants: PopulationSummary
    comparison_giants: PopulationSummary
    statistical_result: StatisticalResult