# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
I picked 4 of 5, not 5 of 5, because two of my questions ask about a specific
building or course (Aldridge Hall laundry, CS 210 exams) and the corpus has
near-identical sibling documents for every other building and course, so one
wrong-neighbour retrieval is a realistic miss. I didn't go looser because the
other three topics each live in a single, clearly-titled document and a miss
there would mean retrieval is actually broken, not merely unlucky.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
All five and not four, because the source name isn't something the model has to
discover: `generate.build_prompt` labels every chunk `[from filename]` and the
grounding instruction tells it to cite one. A missing citation is therefore a
prompt or instruction failure I should be able to fix, not noise I should
tolerate. It would have to go wrong through the model ignoring the instruction.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
Written before I measured any distances. My expectation is a gap, since the five
out-of-scope questions (Mongolia, diesel engines, the World Cup, ibuprofen,
Rust) share no vocabulary with campus life. I allowed one miss in five because
short one-line questions embed loosely and one could still land near a generic
chunk; requiring 5 of 5 would make the target depend on a single unlucky
question.

---

## 4. Something about your chunks

For each of my 5 test questions, the `expects` phrase appears whole inside a
single chunk of the index (checked by searching every chunk's text), so no
answer is cut across a chunk boundary: 5 of 5.

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->



**Why this target:**
The starter's fixed 800-character window can slice through the middle of a
sentence, and the answers here are single facts ("$1.75", "week eight"), so a
cut through one is the exact way chunking would lose an answer. It is 5 of 5
because it is a deterministic string check with no judgement in it: any split
answer is a chunking bug, and I can see it immediately.

> **Revised in unit 2:** For each of my 5 test questions, the `expects` phrase
> appears whole inside the chunk that retrieval actually returns at rank 1 for
> that question: 5 of 5.
>
> **Why revised:** The original measured the wrong thing. It searches *every*
> chunk in the index for the phrase, and my phrases are not distinctive.
> `$1.75` appears in 8 chunks spanning 4 different buildings, and `lecture`
> appears in 8 course chunks. So the check passes as long as the phrase exists
> somewhere in the corpus — which it always will, because I copied the phrases
> out of the corpus when I wrote `questions.py`. It cannot fail, and a check
> that cannot fail measures nothing. Tying it to the chunk retrieval actually
> hands the model makes it a real test of whether the answer survived chunking
> *for that question*. The target stays at 5 of 5; only what is counted changed.

---

## 5. Your choice

Source attribution is correct, not merely present: for at least 4 of my 5 test
questions, the file the answer names is a file whose text contains that
question's `expects` phrase.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->



**Why this target:**
Criterion 2 only checks that a source is named; a confident answer that cites
the wrong file (say, Fenwick Court's laundry post for an Aldridge Hall
question) would pass it and still mislead a student. My corpus is full of
sibling documents that read almost the same, so wrong-neighbour citations are
the failure I care most about. 4 of 5 matches criterion 1: if retrieval can
miss once, attribution can too.

> **Revised in unit 2:** For at least 4 of my 5 test questions, every file the
> answer names is one of the files that actually answers that question — the
> post about the right building or the right course.
>
> **Why revised:** The original does not catch the failure I wrote it to catch,
> and I can show it with the exact example I used to justify it. I said a
> citation of Fenwick Court's laundry post for an Aldridge Hall question
> "would pass criterion 2 and still mislead a student". It would also pass
> criterion 5 as originally written, because
> `housing_fenwick_court_laundry.txt` contains the string `$1.75` — as the
> **dry** price, where Aldridge's `$1.75` is the **wash** price. Checking that
> a cited file contains the phrase somewhere is not the same as checking it is
> the right file, and on a corpus of near-identical siblings the two come
> apart. The revision names the acceptable files per question instead. The
> target stays at 4 of 5.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
