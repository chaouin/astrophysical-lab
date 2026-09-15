import pytest

from astrophysical_lab.literature.nli import resolve_evidence_label


def test_entailment_becomes_support():
    assert resolve_evidence_label(
        "entailment",
        0.90,
    ) == "support"


def test_contradiction_becomes_contradict():
    assert resolve_evidence_label(
        "contradiction",
        0.90,
    ) == "contradict"


def test_low_confidence_prediction_becomes_neutral():
    assert resolve_evidence_label(
        "contradiction",
        0.69,
    ) == "neutral"


def test_unknown_nli_label_raises_error():
    with pytest.raises(ValueError, match="Unsupported NLI label"):
        resolve_evidence_label(
            "unknown",
            0.95,
        )