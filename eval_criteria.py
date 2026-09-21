"""Scores the five criteria in criteria.md, three runs each. Usage: python eval_criteria.py"""
import re, sys, time
import config, gate, questions as qs
from store import search
from generate import answer_from_chunks
from ingest import load_documents
from chunker import split_documents

chunks = split_documents(load_documents())
docs = {d.source: d.text.lower() for d in load_documents()}
QS = qs.answered()
RUNS = 3

def named_sources(answer):
    return re.findall(r"[\w.]+\.(?:txt|md)", answer)

c1, c2, c5, extra = [], [], [], []
for run in range(RUNS):
    a1 = a2 = a5 = ex = 0
    if run: time.sleep(45)
    for q in QS:
        results = search(q["question"], top_k=config.TOP_K)
        exp = q["expects"].lower()
        if any(exp in r.text.lower() for r in results):
            a1 += 1
        ans = answer_from_chunks(q["question"], results, cache=False)
        srcs = named_sources(ans)
        if srcs:
            a2 += 1
        if any(exp in docs.get(s, "") for s in srcs):
            a5 += 1
        ex += sum(1 for s in srcs if exp not in docs.get(s, ""))
        print(f"run {run+1} | {q['question'][:45]:45} | sources={srcs}")
    extra.append(ex); c1.append(a1); c2.append(a2); c5.append(a5)

c3 = sum(1 for q in qs.OUT_OF_SCOPE if not gate.check(search(q, top_k=config.TOP_K)).passed)
c4 = sum(1 for q in QS if any(q["expects"].lower() in c.text.lower() for c in chunks))
n = len(QS)
print("\nC1 retrieved contains answer :", [f"{x}/{n}" for x in c1])
print("C2 names a source            :", [f"{x}/{n}" for x in c2])
print(f"C3 gate stops out-of-scope   : {c3}/{len(qs.OUT_OF_SCOPE)} (deterministic)")
print(f"C4 expects whole in a chunk  : {c4}/{n} (deterministic)")
print("C5 named source has answer   :", [f"{x}/{n}" for x in c5])
print("Cited files without the answer:", extra, "| top_k =", config.TOP_K)
