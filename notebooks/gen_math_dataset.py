import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

rows = [
    # arithmetic
    ("a01", "What is 17 + 29?", "46", "arithmetic", "easy"),
    ("a02", "What is 148 - 63?", "85", "arithmetic", "easy"),
    ("a03", "What is 12 * 15?", "180", "arithmetic", "easy"),
    ("a04", "What is 156 / 4?", "39", "arithmetic", "easy"),
    ("a05", "What is 25 + 33 - 17?", "41", "arithmetic", "easy"),
    ("a06", "What is 7 * 8 + 4?", "60", "arithmetic", "easy"),
    ("a07", "What is 3^4?", "81", "arithmetic", "easy"),
    ("a08", "What is 1024 - 256?", "768", "arithmetic", "easy"),
    # word problems
    ("w01", "A train travels at 60 miles per hour for 2.5 hours. How far does it travel in miles?", "150", "word_problem", "medium"),
    ("w02", "If one dozen eggs costs $3, how much do 4 dozen eggs cost in dollars?", "12", "word_problem", "easy"),
    ("w03", "A rectangle is 12 meters long and 8 meters wide. What is its perimeter in meters?", "40", "word_problem", "medium"),
    ("w04", "A pizza is cut into 8 slices. If 5 slices are eaten, how many slices are left?", "3", "word_problem", "easy"),
    ("w05", "John has 15 apples. He gives 4 to Mary and eats 3. How many apples does he have left?", "8", "word_problem", "medium"),
    ("w06", "A car uses 6 liters of fuel per 100 km. How many liters does it use to drive 250 km?", "15", "word_problem", "hard"),
    ("w07", "A store sells a shirt for $45 after a 25% discount. What was the original price in dollars?", "60", "word_problem", "hard"),
    ("w08", "You run 3 laps of a 400-meter track. How many meters do you run in total?", "1200", "word_problem", "easy"),
    ("w09", "A book has 240 pages. You read 15 pages a day. How many days does it take to finish?", "16", "word_problem", "medium"),
    ("w10", "A bag has 3 red, 5 blue, and 2 green marbles. How many marbles are in the bag in total?", "10", "word_problem", "easy"),
    ("w11", "The sum of two numbers is 100. One of them is 37. What is the other number?", "63", "word_problem", "medium"),
    ("w12", "A recipe needs 1.5 cups of flour per batch. How many cups are needed for 3 batches?", "4.5", "word_problem", "medium"),
    # fractions / percent
    ("f01", "What is 25% of 200?", "50", "fraction_percent", "easy"),
    ("f02", "What is 1/4 of 100?", "25", "fraction_percent", "easy"),
    ("f03", "What is 50% of 78?", "39", "fraction_percent", "easy"),
    ("f04", "What is 2/3 of 60?", "40", "fraction_percent", "medium"),
    ("f05", "What is 3/4 + 1/4?", "1", "fraction_percent", "easy"),
    ("f06", "What is 10% of 350?", "35", "fraction_percent", "easy"),
    ("f07", "A shirt costs $80. It goes on sale for 30% off. How much is the discount in dollars?", "24", "fraction_percent", "medium"),
    ("f08", "What is 15% of 200?", "30", "fraction_percent", "easy"),
    ("f09", "If 40% of a number is 20, what is the number?", "50", "fraction_percent", "hard"),
    # algebra
    ("al01", "If x + 7 = 15, what is x?", "8", "algebra", "medium"),
    ("al02", "If 3x = 24, what is x?", "8", "algebra", "easy"),
    ("al03", "If 2x - 5 = 9, what is x?", "7", "algebra", "medium"),
    ("al04", "If x / 4 = 6, what is x?", "24", "algebra", "easy"),
    ("al05", "If x + 2x = 18, what is x?", "6", "algebra", "medium"),
    ("al06", "If 5x + 3 = 28, what is x?", "5", "algebra", "medium"),
    ("al07", "If 2(x + 3) = 14, what is x?", "4", "algebra", "hard"),
    ("al08", "If x^2 = 81, what is the positive value of x?", "9", "algebra", "medium"),
]

out = []
for r in rows:
    out.append({
        "id": r[0],
        "question": r[1],
        "answer": r[2],
        "category": r[3],
        "difficulty": r[4],
    })

path = os.path.join(BASE, "data", "math_dataset.jsonl")
with open(path, "w", encoding="utf-8") as f:
    for o in out:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")

by_cat = {}
for o in out:
    by_cat[o["category"]] = by_cat.get(o["category"], 0) + 1
print(f"wrote {len(out)} examples to {path}")
for c, n in sorted(by_cat.items()):
    print(f"  {c}: {n}")
