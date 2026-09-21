"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def _sentences(paragraph: str) -> list[str]:
    """Split a paragraph after ., ! or ? followed by whitespace."""
    return [s for s in re.split(r"(?<=[.!?])\s+", paragraph) if s]


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Paragraph-aware chunker with the document title repeated on every chunk.

    Why: every campus_life post is a title line followed by one to four short
    paragraphs, and the title is where the subject lives. "Laundry in Aldridge
    Hall" is the only place the building is named -- the body just says
    "Machines take $1.75 wash". A chunk without its title can't be found by
    someone asking about Aldridge Hall.

    Rules:
      1. The first line is the title. It is prepended to every chunk.
      2. Paragraphs are packed together, in order, until adding the next one
         would push the chunk past config.MAX_CHUNK_CHARS. A post that fits
         stays one chunk; paragraphs are never cut in half if they fit alone.
      3. A single paragraph longer than the limit is cut on sentence
         boundaries, and the last sentence of each piece is repeated at the
         start of the next (the overlap), so no sentence is left dangling.
      4. A trailing chunk with fewer than config.MIN_CHUNK_CHARS characters of
         body is merged into the previous one instead of standing alone.
    """
    limit = config.MAX_CHUNK_CHARS
    min_body = config.MIN_CHUNK_CHARS
    chunks: list[Chunk] = []

    for doc in documents:
        blocks = [b.strip() for b in doc.text.split("\n\n") if b.strip()]
        if not blocks:
            continue
        title, paragraphs = blocks[0], blocks[1:]
        if not paragraphs:                      # a document that is only a title line
            paragraphs, title = [title], ""

        head = f"{title}\n\n" if title else ""
        budget = max(limit - len(head), 100)

        # Break oversized paragraphs into sentence groups first.
        units: list[str] = []
        for para in paragraphs:
            if len(para) <= budget:
                units.append(para)
                continue
            group: list[str] = []
            for sent in _sentences(para):
                if group and len(" ".join(group + [sent])) > budget:
                    units.append(" ".join(group))
                    group = [group[-1], sent]       # one-sentence overlap
                else:
                    group.append(sent)
            if group:
                units.append(" ".join(group))

        # Pack units into chunk bodies.
        bodies: list[str] = []
        current = ""
        for unit in units:
            joined = f"{current}\n\n{unit}" if current else unit
            if current and len(joined) > budget:
                bodies.append(current)
                current = unit
            else:
                current = joined
        if current:
            if bodies and len(current) < min_body:
                bodies[-1] = f"{bodies[-1]}\n\n{current}"
            else:
                bodies.append(current)

        for i, body in enumerate(bodies):
            chunks.append(
                Chunk(
                    text=f"{head}{body}",
                    source=doc.source,
                    index=i,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
