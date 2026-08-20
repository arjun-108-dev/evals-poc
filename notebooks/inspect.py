import csv, os

RAW = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "raw")
for mid in ["functiongemma-270m", "qwen2.5-0.5b", "gemma3-1b", "qwen3-0.6b", "qwen2.5-1.5b"]:
    print("==", mid, "==")
    with open(os.path.join(RAW, mid + ".csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["expected_tool"] != "none":
                print(f"  {r['id']}: exp={r['expected_tool']:<13} got={r['parsed_tool']:<14} TC={r['tool_correct']} AC={r['args_correct']} FP={r['false_positive']}")
