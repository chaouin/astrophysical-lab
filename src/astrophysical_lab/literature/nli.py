import numpy as np
from scipy.special import softmax
from sentence_transformers import CrossEncoder

from astrophysical_lab.models import (
    EvidenceAssessment,
    RetrievedPassage,
)


DEFAULT_NLI_MODEL = "cross-encoder/nli-MiniLM2-L6-H768"

# Translate NLI terminology into labels that are easier to interpret in the scientific evidence pipeline.
NLI_TO_EVIDENCE = {
    "entailment": "support",
    "neutral": "neutral",
    "contradiction": "contradict",
}

MIN_CONFIDENCE = 0.70


class NLIClassifier:
    """Assess how scientific passages relate to a textual claim."""

    def __init__(
        self,
        model_name: str = DEFAULT_NLI_MODEL,
    ) -> None:
        self.model = CrossEncoder(model_name)

        # Read the model's label mapping instead of assuming an ordering.
        # For the default model these are: contradiction, entailment, neutral.
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
        """Classify retrieved passages as support, neutral, or contradict.

        In NLI terminology:
            - passage = premise
            - claim = hypothesis
        """
        if not passages:
            return []

        # Each retrieved passage is evaluated against the same claim.
        pairs = [
            (passage.text, claim)
            for passage in passages
        ]

        # CrossEncoder outputs raw classification scores (logits).
        logits = np.asarray(
            self.model.predict(
                pairs,
                show_progress_bar=False,
            )
        )

        # Ensure a two-dimensional shape even if only one passage is used.
        if logits.ndim == 1:
            logits = logits.reshape(1, -1)

        # Convert raw model scores into probabilities.
        probabilities = softmax(
            logits,
            axis=1,
        )

        assessments = []

        for passage, scores in zip(passages, probabilities):
            score_by_label = {
                self.id2label[index]: float(score)
                for index, score in enumerate(scores)
            }

            # Select the NLI class with the highest probability.
            nli_label = max(
                score_by_label,
                key=score_by_label.get,
            )

            confidence = score_by_label[nli_label]

            if confidence < MIN_CONFIDENCE:
                evidence_label = "neutral"
            else:
                evidence_label = NLI_TO_EVIDENCE[nli_label]

            assessments.append(
                EvidenceAssessment(
                    paper_id=passage.paper_id,
                    paper_title=passage.paper_title,
                    passage=passage.text,
                    claim=claim,
                    retrieval_similarity=passage.similarity,
                    raw_nli_label=nli_label,
                    label=evidence_label,
                    confidence=confidence,
                    support_score=score_by_label["entailment"],
                    neutral_score=score_by_label["neutral"],
                    contradict_score=score_by_label["contradiction"],
                )
            )

        return assessments