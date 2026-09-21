"""Nine harder, paraphrased in-corpus questions (not in questions.py). Reports
gate outcome and rank of the right document. Usage: python probe.py"""
import config, gate, store
TESTS = [("Which dorm is cheapest?","morrow"),("What's the difference between dropping and withdrawing?","withdrawal"),("Do dining dollars carry over to next year?","dining_dollars"),("When does the library close during reading week?","library_hours"),("Which lots sell out first for parking?","parking"),("How many hours a week is CS 340?","cs_340_workload"),("Is Fenwick Court loud?","fenwick_court_noise"),("How long is the walk from Fenwick Court to central campus?","walking"),("What if I miss the registration window?","registration")]
passed = 0
for q, e in TESTS:
    r = store.search(q, top_k=config.TOP_K)
    d = gate.check(r)
    hit = [i + 1 for i, x in enumerate(r) if e in x.source]
    passed += d.passed
    print(f"{r[0].distance:.3f} gate={'pass' if d.passed else 'REFUSE'} rank={hit[0] if hit else 'MISS'} | {q}")
print(f"gate passes {passed}/{len(TESTS)} at cutoff {config.THRESHOLD}")
