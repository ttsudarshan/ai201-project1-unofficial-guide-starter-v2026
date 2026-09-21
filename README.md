# The Unofficial Guide

Sudarshan (ttsudarshan) — corpus: `campus_life`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

The Unofficial Guide answers questions about student life at a fictional university using the `campus_life` corpus: 88 short posts from students on dining halls, dorms (laundry, noise), courses (exams, workload), and the administrative rules nobody explains, such as the housing lottery, add/drop, pass/fail and parking. It retrieves the closest chunks from a local Chroma index, refuses in code if nothing is close enough, and otherwise has a Gemini model answer from those chunks only, naming the source file. Ask it things like "Is the housing lottery random?" or "How much does a wash cost in Aldridge Hall?"; ask it about Mongolia and it says it doesn't know.

## Chunking Strategy

**Chunk size:** at most 450 characters (`MAX_CHUNK_CHARS`), title included. Actual: 91 chunks, 307 characters on average, shortest 159, longest 430.
**Overlap:** none between paragraph chunks; the document title is repeated at the top of every chunk instead. Only when a single paragraph is too long to fit is it cut on sentence boundaries, with one sentence repeated between neighbours.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

What I saw in Milestone 1: every post is a title line plus one to four short paragraphs, 178 to 554 characters, and the starter's 800-character window never cut anything (88 documents, 88 chunks). What shaped my design is that the title carries the subject: `housing_aldridge_hall_laundry.txt` opens "Laundry in Aldridge Hall" and the body says only "Machines take $1.75 wash", so a chunk without its title can't be found by someone asking about Aldridge Hall, and there is a near-identical sibling post for every other building and course. So `chunker.py::split_documents` (1) keeps the title on every chunk, (2) packs whole paragraphs up to 450 characters, so a post that fits stays one chunk and a longer multi-topic post (e.g. Tamsin Court's good/bad/laundry/noise paragraphs) splits between paragraphs rather than inside them, and (3) merges a trailing piece under 100 characters backwards instead of leaving a fragment. Result: 88 documents became 91 chunks; only three posts were long enough to split. I chose 450 rather than 800 because nothing here needs more room, and not much smaller because one paragraph is one fact and the answer needs its neighbours. I did not change my mind partway through.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt` — produced by: `chunker.py::split_documents`

```
======================================================================
On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

**Chunk 2** — source: `course_biol_160_exams.txt` — produced by: `chunker.py::split_documents`

```
======================================================================
BIOL 160 Cell Biology — assessment

Four unit tests and a cumulative final. Not curved.

The unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.
```

**Chunk 3** — source: `course_math_220_exams.txt` — produced by: `chunker.py::split_documents`

```
======================================================================
MATH 220 Linear Algebra — assessment

Two midterms and a cumulative final. Curved to a b- median.

The problem sets are the course; the lectures make sense afterwards rather than during.
```

**Chunk 4** — source: `dining_the_ridgeway_cafe.txt` — produced by: `chunker.py::split_documents`

```
======================================================================
The Ridgeway Café

Second-year here. Wait times: 10 to 15 minutes at 12:30, none after 2:00. The thing worth going for is the only place on campus with real espresso. The thing to know is that seating is tight; about 40 seats for a building of 900.

Hours are 7:00am to 4:00pm weekdays only. Costs declining balance only, no meal swipes.
```

**Chunk 5** — source: `housing_morrow_house.txt` — produced by: `chunker.py::split_documents`

```
======================================================================
Morrow House — what it's actually like

Just finished a year in this building. Built 1954, partially renovated 2008. Rooms are singles and doubles, hall bathrooms.

The good: cheapest housing tier by about $900 a year, and the singles are real singles.

The bad: known damp problem on the ground floor; two rooms were taken offline in 2024.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Is the housing lottery random?

**Answer:**

```
PENDING - needs a real GEMINI_API_KEY in .env. Run:
  python app.py ask "Is the housing lottery random?"
and paste the full output here, with the Source line visible. Retrieval for
this question is already verified: best chunk admin_housing_lottery.txt at
distance 0.254, under the 0.6 cutoff.
```

**My relevance cutoff:** 0.6 (`THRESHOLD` in `config.py`). The two groups were far apart: every question the corpus covers had a best distance of 0.370 or lower, and every out-of-scope question had a best distance of 0.825 or higher. 0.6 sits in the middle of that 0.455-wide gap. Too low (say 0.3) would have refused my CS 210 question at 0.370; too high (say 0.9) would have let Mongolia, the World Cup and Rust through. Retrieval is top-k = 5, unchanged from the starter, since the right chunk was ranked first for all five questions.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---|
| Is the housing lottery random? | yes | 0.254 |
| How late in the term can I declare a course pass/fail? | yes | 0.215 |
| How long is the wait at Kestrel Commons during the lunch rush? | yes | 0.198 |
| How much does a wash cost in the Aldridge Hall laundry? | yes | 0.226 |
| Where do the CS 210 exam questions come from? | yes | 0.370 |
| What is the capital of Mongolia? | no | 0.825 |
| How do I change the oil in a diesel engine? | no | 0.934 |
| Who won the 1994 World Cup? | no | 0.886 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.844 |
| How do I write a for loop in Rust? | no | 0.896 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I gave Claude Code the full project brief and asked it to build the Unit 1 pieces. For the chunker it read the corpus first, noticed that a post's title is the only place the building or course is named, and wrote `chunker.py::split_documents` to repeat the title on every chunk and pack paragraphs up to 450 characters. I did not accept "it looks right": I had it print five chunks, and checked with a script that every `expects` phrase in `questions.py` appears whole inside one chunk (5 of 5 did). Its first attempt at filling in this README overwrote the later sections (Sample Answer, cutoff table) with a bad string splice; the diff showed it, so I had the file restored from git and redone with targeted replacements.

**2.** For the cutoff I asked Claude to measure rather than pick: it ran all five test questions and all five `OUT_OF_SCOPE` questions through `store.search` and printed the best distance for each. That produced the two groups in the table above (at most 0.370 vs at least 0.825), and it kept the starter's 0.6, which lands mid-gap. It also rewrote `GROUNDING_INSTRUCTION` in `generate.py` to add a rule about lookalike documents (one post per building, per course) and a required `Source:` line. I still need to confirm with a real key that the model follows it; the Sample Answer above is pending that.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
