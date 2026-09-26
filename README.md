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

<!-- Milestone 1. -->

Semantic-only retrieval, the system exactly as I submitted it in unit 1.
Produced by `run_eval.py::main`, three runs per question, caching off, log
committed at `results/run_2026-09-26_0327_before.md`. Reproduce with:

```
AI201_HYBRID=0 AI201_RPM=10 python run_eval.py --label before
```

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. `expects` phrase whole inside one chunk | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Named source contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

Criteria 3 and 4 are single deterministic passes — the gate is a comparison
against a fixed number and the chunk check is a string search — so one
measurement goes in all three columns. Criteria 1, 2 and 5 were scored from the
three separate generated answers in the committed log.

### Real output

**Criterion 1 and 2** — `store.py::search` then `generate.py::answer_from_chunks`,
called by `run_eval.py::run_once`:

```
### How much does a wash cost in the Aldridge Hall laundry? — run 1

- Best distance: 0.2262 (passed the gate)
- Sources retrieved: housing_aldridge_hall.txt, housing_aldridge_hall_laundry.txt,
  housing_innisfree_hall.txt, housing_innisfree_hall_laundry.txt, housing_old_brewhouse.txt

A wash in the Aldridge Hall laundry costs $1.75.

Source: housing_aldridge_hall_laundry.txt
```

**Criterion 3** — `run_eval.py::check_out_of_scope` and `gate.py::check`, cutoff 0.7:

```
| Out-of-scope question                                       | Best distance | Gate    |
| What is the capital of Mongolia?                            | 0.825         | refused |
| How do I change the oil in a diesel engine?                 | 0.934         | refused |
| Who won the 1994 World Cup?                                 | 0.886         | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.844         | refused |
| How do I write a for loop in Rust?                          | 0.896         | refused |
-> gate refused 5 of 5
```

**Criterion 4** — string search over every chunk from `chunker.py::split_documents`:

```
yes ['admin_graduation_requirements.txt#0', 'admin_housing_lottery.txt#0', 'advising_registration.txt#0'] | credit hours
yes ['admin_pass_fail_option.txt#0', 'course_cs_340.txt#0', 'course_cs_340_exams.txt#0']                  | week eight
yes ['dining_kestrel_commons.txt#0', 'dining_kestrel_commons_followup.txt#0']                             | 20 to 25 minutes
yes ['housing_aldridge_hall.txt#0', 'housing_aldridge_hall_laundry.txt#0', 'housing_calder_annexe.txt#0',
     'housing_calder_annexe_laundry.txt#0', 'housing_fenwick_court.txt#0', 'housing_fenwick_court_laundry.txt#0',
     'housing_innisfree_hall.txt#1', 'housing_innisfree_hall_laundry.txt#0']                              | $1.75
yes ['course_biol_160.txt#0', 'course_cs_210.txt#0', 'course_cs_210_exams.txt#0', 'course_cs_340.txt#0',
     'course_econ_101.txt#0', 'course_math_220.txt#0', 'course_math_220_exams.txt#0', 'course_phys_130.txt#0'] | lecture
-> C4 = 5/5
```

Look at the last two rows. That is criterion 4 passing, and it is also the
first thing that went wrong in this unit — see **Diagnoses**.

**Criterion 5** — the `Source:` lines parsed out of all 15 committed answers:

```
run 1:  C2 names a source 5/5   |  C5 as written 5/5   |  C5 strict (exact right file) 5/5
run 2:  C2 names a source 5/5   |  C5 as written 5/5   |  C5 strict (exact right file) 5/5
run 3:  C2 names a source 5/5   |  C5 as written 5/5   |  C5 strict (exact right file) 5/5
wrong-neighbour citations: none
```

## Verdicts

<!-- Milestone 2. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Retrieved chunks contain the answer | 4 of 5 | MET | 5 of 5 in all three runs, and the right file was rank 1 every time, so it clears the target with a run to spare. |
| 2 | Every answer names a source | 5 of 5 | MET | All 15 answers ended in a `Source:` line. Target is every answer, and every answer had one. |
| 3 | Gate stops out-of-corpus questions | 4 of 5 | MET | 5 of 5 refused. The closest out-of-scope question (Mongolia, 0.825) is still 0.125 clear of the 0.7 cutoff, so this is not a near miss. |
| 4 | `expects` phrase whole inside one chunk | 5 of 5 | MET (but the check is hollow — revised) | 5 of 5 by string search. I am calling it MET because that is what the criterion as written says, but it passes for the wrong reason and I revised it in `criteria.md`. |
| 5 | Named source contains the answer | 4 of 5 | MET (and still MET under a stricter check) | 5 of 5 as written. I also scored a strict version — is the cited file the *right* file — and that is 5 of 5 too, so the verdict does not depend on the loose wording. |

Nothing here was close, so no verdict came down to a judgement call. The honest
difficulty in this unit was not deciding met-or-missed; it was noticing that two
of the five criteria were not measuring what I thought they were.

## Diagnoses

<!-- Milestone 3. -->

**I missed nothing. All five criteria were met on every run, before and after.**

Under the rules that means I owe an honest answer about whether the targets were
set low. They were, and in two cases the problem is worse than a low target:
the criterion could not have failed at all.

### The pattern: my `expects` phrases are not distinctive

This is one problem, not two, and it is behind both weak criteria.

`questions.py` stores an `expects` phrase per question, and I wrote those
phrases by copying them out of the corpus. So they are guaranteed to exist in
the corpus. Any criterion that asks "does this phrase appear somewhere" is
therefore asking a question whose answer is already known to be yes.

The numbers make it concrete. `$1.75` appears in **8 chunks across 4 different
buildings**. `lecture` appears in **8 course chunks**. `credit hours` in 3.

- **Criterion 4** ("the phrase appears whole inside a single chunk") searches
  *every* chunk in the index. It cannot fail. It told me nothing about whether
  the answer to *that question* survived chunking. **Stage: none — this is a
  measurement defect, not a pipeline failure.**
- **Criterion 5** ("the file the answer names contains the phrase") is worse,
  because it fails to catch the exact thing I wrote it to catch. In
  `criteria.md` I justified it by saying a citation of Fenwick Court's laundry
  post for an Aldridge Hall question would mislead a student. It would — and it
  would also **pass criterion 5**, because `housing_fenwick_court_laundry.txt`
  contains the string `$1.75`:

```
Laundry in Aldridge Hall
Machines take $1.75 wash, $1.50 dry, card only.

Laundry in Fenwick Court
Machines take $2.00 wash, $1.75 dry, app-based.
```

  Aldridge's `$1.75` is the **wash** price. Fenwick's `$1.75` is the **dry**
  price. Same string, different fact, wrong building. Both revisions are
  written under the originals in `criteria.md`.

### The real failure, found by probing harder

Because the five criteria were all at ceiling, I went looking for a failure with
questions that are *not* my criteria questions, so this is diagnosis and not a
quiet reset of the test. I generated 32 sibling questions — one per dorm for
laundry and noise, one per course for exams and workload — and asked only
whether retrieval put the right document first.

| Group | Before (semantic only) |
|---|---|
| Dorm laundry, right file at rank 1 | 4 of 7 |
| Dorm noise, right file at rank 1 | 7 of 7 |
| Course exams, right file at rank 1 | 6 of 9 |
| Course workload, right file at rank 1 | 8 of 9 |
| **Right file at rank 1, overall** | **25 of 32 (78%)** |
| **Right *building or course* at rank 1** | **31 of 32 (97%)** |

Those last two rows matter and I nearly reported only the first. Three of the
seven "misses" are the Innisfree, Morrow and Old Brewhouse laundry questions
returning the *parent* dorm post instead of the dedicated laundry post — and
the parent post for those three buildings repeats the laundry fact verbatim:

```
Morrow House — what it's actually like
...
Laundry costs $1.50 wash, $1.25 dry, coin or card. On noise: loud until about 1am on weekends.
```

That is the right building with the right price, so it is not a wrong answer at
all; my scoring was too strict. Once I scored by *entity* instead of by
filename, the before system was already 31 of 32, not 25.

**That leaves exactly one true failure, and it is a real one:**

```
WRONG ENTITY  got=course_phys_130_workload.txt   want=course_hist_118_*   | How many hours a week is HIST 118?
```

**Stage: retrieval.** **Mechanism:** the workload posts are written to a
template, so `course_hist_118_workload.txt` and `course_phys_130_workload.txt`
are near-identical prose. Nearly all the embedding's 384 dimensions are spent
on "this is a post about weekly workload for a course", which both share, and
the only thing separating them is the token `hist` / `118` versus `phys` /
`130` — which a sentence embedding compresses almost to nothing.

There is a second reason this particular pair collides, and I only found it by
opening both files:

```
Workload for HIST 118 Modern World History
People keep asking so: a lot of reading, about 120 pages a week, but no problem sets.

Workload for PHYS 130 Mechanics
People keep asking so: 7 hours a week, plus 3 on lab weeks.
```

HIST 118's workload is given in **pages**, not hours. PHYS 130's is the only
one of the two that says "hours a week" — which is the phrase in my question.
So semantic search was not malfunctioning; it was matching the question's
wording to the only post that shares it. The question has no answer in the
corpus at all.

**How much did this actually cost me?** Less than I first wrote down. I checked
the end-to-end answer, and the before system refuses this question correctly:

```
$ AI201_HYBRID=0 python app.py ask "How many hours a week is HIST 118?"
  (best distance 0.448, cutoff 0.7)
I don't have enough information about that.
Sources retrieved: course_econ_101_workload.txt, course_hist_118.txt,
course_hist_118_workload.txt, course_phys_130_workload.txt, course_stat_150_workload.txt
```

The wrong post was at rank 1, but `GROUNDING_INSTRUCTION` in `generate.py`
already tells the model to use only a document whose title names exactly what
the question asks about, and it did. So this is a real ranking defect sitting
behind a prompt that happens to mask it — worth fixing, because the prompt is
the weaker of the two layers and I would rather not depend on it, but not a
wrong answer any student ever saw.

### Which criteria I would tighten

Criteria 1 and 5 each allowed one miss in five and I never used it, so both go
to 5 of 5. Criterion 3's allowance of one miss was also unnecessary given a
0.455-wide gap between the two distance groups. But tightening the numbers is
the smaller half — criteria 4 and 5 needed their *measurement* fixed, which is
what the revisions in `criteria.md` do.

## The Improvement

<!-- Milestone 4. -->

**What I changed:** hybrid search. `store.py::search` now runs a BM25 keyword
ranking alongside the existing semantic ranking and fuses the two with
Reciprocal Rank Fusion (`store.py::_rrf`, `store.py::_bm25_for`). The new
settings are `HYBRID_SEARCH`, `RRF_K` and `HYBRID_POOL` in `config.py`.
`rank-bm25` was already in `requirements.txt`, so nothing new was installed.

**Why I picked it, in one sentence:** my one true failure was HIST 118 losing
to PHYS 130 because the embedding compresses away the course code, and BM25
scores `hist` and `118` as ordinary terms, so the token the embedding throws
away is exactly the token keyword search keeps.

Two design decisions worth stating, because both could have quietly broken
something:

- **Ranks are fused, not scores.** A cosine distance and a BM25 score have no
  common scale and normalising them would have been invented precision. RRF
  adds `1 / (60 + rank)` from each ranker instead.
- **Every result keeps its real cosine distance.** Fusion decides *which*
  chunks come back and in what order; it never invents a distance. That matters
  because `gate.py::check` compares distance against the 0.7 cutoff I
  calibrated in unit 1, and I did not want the improvement to silently
  recalibrate the gate.

### Run Log — After

Hybrid retrieval. Log committed at `results/run_2026-09-26_0331_after.md`.
Reproduce with:

```
AI201_HYBRID=1 AI201_RPM=10 python run_eval.py --label after
```

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict | vs before |
|---|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET | no change |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET | no change |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET | no change |
| 4. `expects` phrase whole inside one chunk | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET | no change |
| 5. Named source contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET | no change |

Under the revised wording of criteria 4 and 5 the answer is the same: revised
criterion 4 (phrase inside the rank-1 chunk) is 5 of 5 before and after;
revised criterion 5 (cited file is the right file) is 5 of 5 before and after.

### Did it help?

**On my five criteria: no. Not at all. Every cell is identical.** That is not a
disappointment I am dressing up — it is the predictable result of testing a
change against five questions that were already scoring 100% before the change.
There was no headroom for it to win.

**On the failure it was built to fix: yes, and measurably.** Same 32 sibling
questions, same script, hybrid the only difference:

| Group | Before | After |
|---|---|---|
| Dorm laundry, right file at rank 1 | 4 of 7 | 4 of 7 |
| Dorm noise, right file at rank 1 | 7 of 7 | **6 of 7** |
| Course exams, right file at rank 1 | 6 of 9 | **9 of 9** |
| Course workload, right file at rank 1 | 8 of 9 | **9 of 9** |
| Right file at rank 1, overall | 25 of 32 (78%) | **28 of 32 (88%)** |
| Right building or course at rank 1 | 31 of 32 (97%) | **32 of 32 (100%)** |

The HIST 118 failure is fixed at the ranking level — it now returns
`course_hist_118_workload.txt` at rank 1 — and the three course-exam questions
that were returning the parent course post now return the exams post. **It also
caused one regression:** "Is Morrow House noisy at night?" fell from rank 1 to
rank 2, because the parent Morrow post contains both `morrow` and `noise` and
BM25 rewards it for the repetition. Net is plus three, minus one.

**On the answers a user actually sees: I could not find a single case where it
made a difference.** I ran the HIST 118 question end to end both ways and got
the same refusal from each, because the grounding instruction was already
rejecting the wrong-course post that retrieval had put first. So every
improvement I measured is an improvement in what the model is *shown*, not in
what it *says*.

I want to be careful about how much I claim. The 78% → 88% figure is the one
that looks impressive and the one I trust least: it counts parent-post results
as failures when they contain the correct answer, and it measures ranking
rather than output. The honest summary is three sentences. **Hybrid search
improved retrieval ranking on a 32-question probe set, decisively on the
course-exam questions. It cost me one rank-1 position on Morrow House noise. It
changed no answer I was able to observe, and none of my five criteria — which
means I have improved a stage of the pipeline without yet showing that the
improvement reaches the user.**

One side effect I did not anticipate: `search` no longer returns results
strictly nearest-first, because fused order is not distance order. That is
deliberate — reranking is the whole point — but it means
`tools/smoke_test.py`'s "results are ordered nearest first" check now fails
when hybrid is on. The smoke test passes in full with `AI201_HYBRID=0`. I left
the test alone rather than editing it to agree with me.

The gate's reported best distance also shifted slightly on out-of-scope
questions (Mongolia 0.825 → 0.869), because that number is now the minimum over
the fused top-5 rather than over the five nearest chunks. All five are still
refused by a wide margin, but it is a real change in what that number means.

## What's Still Broken

<!-- Milestone 5. -->

**1. My test is too easy to tell me much.** This is the big one. Five
questions, written by me, each with one clean answer in one post, all scoring
5 of 5 before and after. A test that cannot distinguish the system before my
change from the system after it is not measuring the system. What I would do:
promote the 32-question sibling set into the real test and score it
automatically, so criterion 1 runs against 32 questions instead of 5. I did not
do it in this unit because swapping in a different set of questions
mid-evaluation would have made the before and after incomparable, which is the
one thing the unit asks me not to do.

**2. Three laundry questions still return the parent dorm post.** Innisfree,
Morrow and Old Brewhouse. Not wrong — those posts carry the right price for the
right building — but the dedicated post is the better source and it loses.
The cause is in **loading**, not retrieval: the corpus stores the same fact in
two places, so there is no ranking fix that makes this clean. I would deal with
it at ingest by noticing duplicated facts, and I stopped because it is a corpus
problem I would be papering over from the retrieval end.

**3. The Morrow House noise regression.** A direct cost of my change, above. A
tuned weighting between the two rankers instead of plain RRF would likely
recover it, but tuning a weight on 32 questions I wrote myself would be fitting
to my own test set, which is how you get a number that improves and a system
that does not.

**4. The gate is untested near its boundary.** Every in-corpus question is at
0.370 or better and every out-of-corpus one at 0.825 or worse. I have no
evidence about anything in between — a question my corpus half-covers. 5 of 5
on a gap that wide is not a hard test.

**5. The improvement does not demonstrably reach the user.** Hybrid search
moved retrieval ranking and moved nothing downstream of it that I could
observe. I would want to find a question where the wrong-neighbour post is the
*only* plausible source, so the grounding instruction cannot quietly rescue it,
and check whether the answer changes. Until I have that, "it helped" is a claim
about a stage, not about the system.

**6. The refusal line is not exact, and criterion 2 would not notice.**
`GROUNDING_INSTRUCTION` says to reply exactly "I don't have enough information
about that." The HIST 118 refusal came back as that sentence *plus* a `Source:`
line naming three files it did not use:

```
I don't have enough information about that.

Source: course_hist_118.txt, course_hist_118_exams.txt, course_hist_118_workload.txt
```

Harmless here, but criterion 2 counts an answer as passing when it names a
source, so a refusal that cites its way out would score as a pass. None of my
five questions refuse, so this never affected a number — it is a third example
of the same lesson the other two criteria taught me.

**7. Fusion can only rerank what the semantic pool returned.** With 91 chunks
the pool is the whole corpus, so it does not bite here. On a larger index a
chunk BM25 loves but the embedding never surfaced would be dropped, because I
would not hold a real cosine distance for it and the gate needs one. It is
documented in `store.py::search` rather than fixed.

## What I'd Do Differently

<!-- Milestone 5. -->

**Criterion 4 is the one I would rewrite, and not by moving the number.** It was
5 of 5 and it was worthless, which is a combination I did not know was possible
before this unit. The flaw is that it searches the whole index for a phrase I
copied out of that index. I would tie it to the chunk retrieval actually
returns — which is the revision now in `criteria.md`, and which stays at 5 of 5,
so the revision costs me nothing and the original bought me nothing.

**Criterion 5 is the one that taught me the most,** because I had already
written down the exact failure it misses. My own justification in `criteria.md`
used Fenwick Court's laundry post as the example of a citation that would
mislead — and that post contains `$1.75`, so it would have sailed through. The
lesson is that "the answer contains X" and "the answer is right" only coincide
when X is unique, and I never checked that mine were.

**The general thing I would change:** I set every target as a count out of five
and then wrote five questions I already knew the answers to. Next time I would
write the questions from the *document titles* without reading the bodies, so I
cannot smuggle the answer into the `expects` phrase, and I would set at least
one criterion against a question set large enough that a real change moves it.

## How I Used AI — Unit 2

<!-- Milestone 5 — added to the unit 1 section above, continuing its numbering. -->

**3. Finding the hollow criteria (unit 2).** I had all five criteria passing and
asked Claude Code to argue the opposite verdict as hard as it could. It went
after the measurement rather than the numbers: it printed how many chunks
contain each `expects` phrase and showed `$1.75` in 8 chunks across 4
buildings, then found that `housing_fenwick_court_laundry.txt` contains `$1.75`
as its dry price — the counter-example to the justification I had written for
criterion 5 in unit 1. I checked both by opening the files myself before
writing the revisions, because this is the finding the whole unit rests on.

**4. The improvement, and the numbers I nearly overclaimed.** I asked for a
diagnosis I could connect to a fix in one sentence, and the 32-question sibling
probe came out of that. Its first result was "78% → 88%", which I was ready to
put in the README. Re-scoring by building/course instead of by filename showed
the before system was already at 97%, because the parent dorm posts I was
counting as misses contain the right answer. The improvement is real but much
smaller than the first number suggested, and both are in the table above. I
also had it explain why hybrid search might *not* work before I built it; the
regression it predicted — a parent post that repeats a child post's keywords
winning on BM25 — is exactly the Morrow House noise case.

**5. A mistake worth recording.** Running `python tools/smoke_test.py` rebuilds
the `campus_life` index with fake embeddings (`AI201_FAKE_EMBEDDINGS=1`, line
23), so every measurement I took immediately afterwards was garbage — the
housing lottery question was returning a dining hall post. I only caught it
because the number was absurd rather than merely bad. `python app.py index`
puts it back. My before and after eval runs were taken before that happened and
are unaffected, but it is a good argument for re-reading a result that looks
surprising instead of writing it down.
