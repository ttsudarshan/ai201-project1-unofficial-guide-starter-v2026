# The Unofficial Guide

Sudarshan — corpus: `campus_life`

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

I picked the `campus_life` corpus, which is 88 short posts from students about life at a made-up university: dining halls, dorms, courses, and the admin rules nobody explains (housing lottery, add/drop, pass/fail, parking). You type a question, it finds the closest chunks in a local Chroma index, and a Gemini model answers using only those chunks and names the file it used. If nothing in the index is close enough it just says it doesn't know instead of guessing.

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

When I read the documents, every post was a title line plus one to four short paragraphs, somewhere between 178 and 554 characters. The starter's 800-character chunker never split anything (88 documents, 88 chunks), so it wasn't really chunking at all.

The thing I noticed is that the title is where the subject lives. `housing_aldridge_hall_laundry.txt` starts with "Laundry in Aldridge Hall", but the body only says "Machines take $1.75 wash". Take the title off and nobody asking about Aldridge Hall can find it, and there's a lookalike post for every other building and course. So my chunker (`chunker.py::split_documents`) puts the title at the top of every chunk, and packs whole paragraphs together up to 450 characters. A post that fits stays as one chunk. A longer one, like the Tamsin Court post with its good/bad/laundry/noise paragraphs, splits between paragraphs and never in the middle of one. A leftover piece under 100 characters gets merged back into the previous chunk so there are no tiny fragments.

That gave 91 chunks from 88 documents, so only three posts were long enough to split. I went with 450 because nothing in this corpus needs more room, but I didn't go much smaller because each paragraph is one fact and it needs its neighbours to make sense. I didn't change my mind partway through.

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
The housing lottery is not entirely random in the way most people assume. While rising sophomores get a number drawn at random, juniors and seniors are ordered by accumulated credit hours first, with a random tie-break used only for ties.

Source: admin_housing_lottery.txt
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

**1. The chunker.** I told Claude Code what the assignment was and asked it to write a chunker for my corpus. It read the posts first and pointed out that the title is the only place the building or course is named, so it wrote a version that repeats the title on every chunk. I didn't just trust it. I printed five chunks and read them, and I ran a check that each `expects` phrase in `questions.py` shows up whole inside a single chunk (all 5 did). When it tried to fill in this README it accidentally wiped out the later sections with a bad string replace, so I had it restore the file from git and redo it more carefully.

**2. The cutoff and the prompt.** I didn't want to guess the relevance cutoff, so I had it print the best distance for my five real questions and the five out-of-scope ones. The real ones were 0.370 or lower and the out-of-scope ones were 0.825 or higher, so I kept 0.6 in the middle. It also tightened `GROUNDING_INSTRUCTION` in `generate.py` to warn about lookalike documents and to require a `Source:` line. Once my API key was working I ran all five questions and all of them came back grounded with the right file named (for example Aldridge Hall laundry gave `housing_aldridge_hall_laundry.txt` and "$1.75").

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
