import csv, os
RAW = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "raw")
with open(os.path.join(RAW, "functiongemma-270m.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["id"] in ("e01", "e02", "e15", "e04"):
            print("ID:", r["id"], "| err:", r["error"])
            print("  OUT:", repr(r["model_output"])[:400])
            print("  parsed_tool:", repr(r["parsed_tool"]), "args:", repr(r["parsed_args"]))
            print()
