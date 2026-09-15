import re

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import semantic_search

from astrophysical_lab.models import RetrievedPassage, ScientificPaper, ScientificPassage


DEFAULT_MODEL = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"


def split_into_passages(
    papers: list[ScientificPaper],
) -> list[ScientificPassage]:
    """Split paper abstracts into sentence-level passages."""
    passages = []

    for paper in papers:
        # Simple sentence segmentation suitable for short scientific abstracts.
        sentences = re.split(
            r"(?<=[.!?])\s+",
            paper.abstract,
        )

        for sentence in sentences:
            sentence = sentence.strip()

            # Assumption: very short fragments rarely contain useful scientific claims.
            if len(sentence.split()) < 8:
                continue

            passages.append(
                ScientificPassage(
                    paper_id=paper.paper_id,
                    paper_title=paper.title,
                    text=sentence,
                )
            )

    return passages


class SemanticRetriever:
    """Retrieve scientific passages using sentence embeddings."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
    ) -> None:
        self.model = SentenceTransformer(model_name)

    def retrieve(
        self,
        question: str,
        papers: list[ScientificPaper],
        top_k: int = 5,
    ) -> list[RetrievedPassage]:
        """Rank scientific passages by semantic similarity to a question."""
        passages = split_into_passages(papers)

        if not passages:
            return []

        corpus = [
            passage.text
            for passage in passages
        ]

        # The scientific question is encoded as a retrieval query.
        query_embedding = self.model.encode_query(
            question,
            convert_to_tensor=True,
        )

        # Abstract sentences are encoded as documents.
        corpus_embeddings = self.model.encode_document(
            corpus,
            convert_to_tensor=True,
        )

        hits = semantic_search(
            query_embedding,
            corpus_embeddings,
            top_k=min(top_k, len(passages)),
        )[0]

        retrieved = []

        for hit in hits:
            passage = passages[hit["corpus_id"]]

            retrieved.append(
                RetrievedPassage(
                    paper_id=passage.paper_id,
                    paper_title=passage.paper_title,
                    text=passage.text,
                    similarity=float(hit["score"]),
                )
            )

        return retrieved