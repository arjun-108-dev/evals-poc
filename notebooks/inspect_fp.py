import csv, os
RAW = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "raw")

for mid in ["qwen2.5-0.5b", "gemma3-1b", "functiongemma-270m"]:
    print("########", mid, "########")
    with open(os.path.join(RAW, mid + ".csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["expected_tool"] == "none":
                fp = "FP" if r["false_positive"] == "True" else "  "
                print(f"  [{fp}] {r['id']} prompt={r['prompt'][:40]!r}")
                print(f"        got={r['parsed_tool']!r} args={r['parsed_args'][:60]!r}")
                print(f"        raw={r['model_output'][:90]!r}")
    print()
