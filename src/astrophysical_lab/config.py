# Astrophysical population definition
MIN_GIANT_MASS_JUPITER = 0.3
MAX_GIANT_MASS_JUPITER = 13.0
SHORT_PERIOD_DAYS = 10.0

# Statistical analysis
SIGNIFICANCE_LEVEL = 0.05

# Literature retrieval
RETRIEVAL_MODEL = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
DEFAULT_MAX_PAPERS = 20
DEFAULT_TOP_K = 5

ARXIV_QUERY = (
    'cat:astro-ph.EP AND (all:"giant planet" OR all:"hot Jupiter") AND all:metallicity'
)

# NLI
NLI_MODEL = "cross-encoder/nli-MiniLM2-L6-H768"
NLI_MIN_CONFIDENCE = 0.70
