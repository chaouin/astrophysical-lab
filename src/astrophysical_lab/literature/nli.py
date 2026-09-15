import numpy as np
from scipy.special import softmax
from sentence_transformers import CrossEncoder

from astrophysical_lab.config import NLI_MIN_CONFIDENCE, NLI_MODEL
from astrophysical_lab.models import EvidenceAssessment, EvidenceLabel, RetrievedPassage


NLI_TO_EVIDENCE = {
    "entailment": "support",
    "neutral": "neutral",
    "contradiction": "contradict",
}


def resolve_evidence_label(
    raw_label: str,
    confidence: float,
    min_confidence: float = NLI_MIN_CONFIDENCE,
) -> EvidenceLabel:
    """Convert an NLI prediction into a conservative evidence label."""
    if confidence < min_confidence:
        return "neutral"

    try:
        return NLI_TO_EVIDENCE[raw_label]
    except KeyError as exc:
        raise ValueError(
            f"Unsupported NLI label: {raw_label}"
        ) from exc


class NLIClassifier:
    """Estimate the relation between retrieved passages and a claim."""

    def __init__(
        self,
        model_name: str = NLI_MODEL,
    ) -> None:
        self.model = CrossEncoder(model_name)

        self.id2label = {
            int(index): label.lower()
            for index, label
            in self.model.model.config.id2label.items()
        }

    def assess(
        self,
        claim: str,
        passages: list[RetrievedPassage],
    ) -> list[EvidenceAssessment]:
        if not passages:
            return []

        pairs = [
            (passage.text, claim)
            for passage in passages
        ]

        logits = np.asarray(
            self.model.predict(
                pairs,
                show_progress_bar=False,
            )
        )

        if logits.ndim == 1:
            logits = logits.reshape(1, -1)

        probabilities = softmax(logits, axis=1)

        assessments = []

        for passage, scores in zip(passages, probabilities):
            score_by_label = {
                self.id2label[index]: float(score)
                for index, score in enumerate(scores)
            }

            raw_label = max(
                score_by_label,
                key=score_by_label.get,
            )

            confidence = score_by_label[raw_label]

            label = resolve_evidence_label(
                raw_label,
                confidence,
            )

            assessments.append(
                EvidenceAssessment(
                    paper_id=passage.paper_id,
                    paper_title=passage.paper_title,
                    passage=passage.text,
                    claim=claim,
                    retrieval_similarity=passage.similarity,
                    raw_nli_label=raw_label,
                    label=label,
                    confidence=confidence,
                    support_score=score_by_label["entailment"],
                    neutral_score=score_by_label["neutral"],
                    contradict_score=score_by_label["contradiction"],
                )
            )

        return assessments