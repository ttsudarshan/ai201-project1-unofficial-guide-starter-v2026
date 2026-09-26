"""
Settings for The Unofficial Guide.

Everything you're likely to change lives here, at the top, on purpose.
You'll edit THRESHOLD in Milestone 4 and the chunking numbers in Milestone 3.

Anything you set in your .env file wins over the defaults here.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")


# ─── The corpus you're working with ──────────────────────────────────────────
# Change this to switch corpora, or pass --corpus on the command line.
# Options are the folder names inside corpora/. See corpora/README.md.

CORPUS = os.getenv("AI201_CORPUS", "campus_life")


# ─── Chunking (Milestone 3) ──────────────────────────────────────────────────
# These are deliberately plain, generic numbers. Milestone 3 is where you
# replace them with numbers that fit the documents you actually read.

CHUNK_SIZE = 800        # characters per chunk
CHUNK_OVERLAP = 120     # characters shared between neighbouring chunks

# Used by chunker.py::split_documents (the paragraph-aware chunker), not by the
# fallback above. campus_life posts run 178-554 characters, title included.
MAX_CHUNK_CHARS = 450   # a chunk (title + paragraphs) may not grow past this
MIN_CHUNK_CHARS = 100   # a trailing piece shorter than this merges backwards


# ─── Retrieval (Milestone 4) ─────────────────────────────────────────────────

TOP_K = 5               # how many chunks to pull back per question

# The relevance gate. If the best chunk is further away than this, the system
# refuses to answer instead of handing the model thin material.
#
# LOWER IS BETTER: 0.3 is a close match, 0.9 is unrelated.
#
# 0.6 is a reasonable starting point, not a right answer. Milestone 4 has you
# measure your own two groups of distances and put the cutoff in the gap.
# Most corpora land somewhere between 0.45 and 0.75.
THRESHOLD = 0.7         # was 0.6. In-corpus best <= 0.370 on my 5 questions, out-of-corpus best >= 0.825


# ─── Hybrid search (unit 2 improvement) ──────────────────────────────────────
# Semantic search alone matches on meaning, which is exactly wrong for a corpus
# like this one: there is a near-identical post for every dorm and every
# course, and the only thing telling them apart is a name or a number the
# embedding barely notices. "How many hours a week is HIST 118?" returned the
# PHYS 130 workload post first, because the two read almost identically.
#
# BM25 is a keyword ranker, so "hist", "118" and "laundry" count for a lot.
# Running both and fusing their rankings is the fix. Set this to False to get
# the pure-semantic behaviour back — that is how the before/after was measured.

# AI201_HYBRID=0 turns fusion off without editing this file, which is how the
# "before" half of the unit 2 run log was produced:
#     AI201_HYBRID=0 python run_eval.py --label before
HYBRID_SEARCH = os.getenv("AI201_HYBRID", "1") != "0"

# Reciprocal Rank Fusion. Each ranker contributes 1 / (RRF_K + rank) to every
# chunk, and the two contributions are added. Fusing *ranks* rather than scores
# means a cosine distance and a BM25 score never have to be put on the same
# scale, which they cannot honestly be. 60 is the value from the paper that
# introduced RRF and is not tuned to this corpus.
RRF_K = 60

# How many chunks the semantic side pulls back for fusion to rerank. The
# campus_life index is 91 chunks, so this takes all of them and BM25 sees the
# whole corpus. On a much larger index it caps the work.
HYBRID_POOL = 500


# ─── Models ──────────────────────────────────────────────────────────────────
# Embeddings run on your own machine and cost no API quota.
# Only generation calls out to a service.

# This is the model Chroma bundles, and leaving it alone is the fast path: it
# downloads about 80 MB from Chroma's own CDN and needs nothing else installed.
#
# Setting it to any other name — unit 2's "try a second embedding model"
# stretch option — switches to loading that model from Hugging Face instead,
# which needs `pip install 'sentence-transformers>=3.4,<3.5'` first. store.py
# says so with a real error message rather than a stack trace if you forget.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MODEL = os.getenv("AI201_MODEL", "gemini-3.5-flash-lite")


# ─── Rate limiting and quota guards ──────────────────────────────────────────
# You should not need to touch these. They exist so that a runaway loop costs
# you a warning instead of your whole day's allowance.

# AI201_RPM lowers this without editing the file. The free tier allows 15/min
# for gemini-3.5-flash-lite, so the unit 2 evaluation runs were paced with
#     AI201_RPM=10 python run_eval.py ...
REQUESTS_PER_MINUTE = int(os.getenv("AI201_RPM", "30"))   # outgoing calls allowed per minute
SESSION_REQUEST_BUDGET = 300   # stop and warn rather than draining the daily quota
MAX_RETRIES = 4                # on 429 / resource-exhausted, with backoff

CACHE_ENABLED = os.getenv("AI201_CACHE", "1") != "0"
CACHE_DIR = ROOT / ".cache"


# ─── Paths ───────────────────────────────────────────────────────────────────

CORPORA_DIR = ROOT / "corpora"
CHROMA_DIR = ROOT / "chroma_db"
RESULTS_DIR = ROOT / "results"


def corpus_path(name: str | None = None) -> Path:
    """Folder holding the documents for a corpus."""
    return CORPORA_DIR / (name or CORPUS) / "documents"


def collection_name(name: str | None = None, variant: str = "default") -> str:
    """
    Name of the vector-store collection for a corpus.

    `variant` lets you index the same corpus two different ways and query both
    without deleting anything — you'll want that in unit 2 when you compare
    chunking strategies.

    Chroma is fussy about collection names: 3 to 63 characters, starting and
    ending with a letter or digit, and nothing but letters, digits, underscores
    and hyphens in between. If you bring your own corpus and name the folder
    something Chroma won't accept, this cleans it up rather than failing.
    """
    import re

    raw = f"{name or CORPUS}__{variant}"
    cleaned = re.sub(r"[^A-Za-z0-9_-]", "-", raw)
    cleaned = cleaned.strip("_-")          # must start and end alphanumeric
    if not cleaned or not cleaned[0].isalnum():
        cleaned = f"c{cleaned}"
    if not cleaned[-1].isalnum():
        cleaned = f"{cleaned}0"
    return cleaned[:63].rstrip("_-") or "collection"
