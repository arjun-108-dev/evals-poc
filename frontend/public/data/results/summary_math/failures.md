# Math Evaluation: Failures & Notable Cases

Generated automatically by `evaluator/analyze_math.py`. All results below are from **real** model runs via Ollama (no synthetic data).

## Model ranking (by overall score)

| Rank | Model | Size | Accuracy | Parse Rate | Overall | Avg ms |
|------|-------|------|---------:|-----------:|--------:|--------:|
| 1 | Gemma 3 1B | 1B | 97% | 100% | 0.980 | 6205 |
| 2 | Qwen2.5 1.5B | 1.5B | 92% | 100% | 0.939 | 2953 |
| 3 | Qwen3 0.6B | 0.6B | 86% | 100% | 0.899 | 7556 |
| 4 | Qwen2.5 0.5B | 0.5B | 78% | 100% | 0.838 | 3828 |

## Gemma 3 1B (1B)
_General-purpose tiny multimodal model. Not specifically trained for tool use._

- Accuracy: **97%** (36/37)
- Parse rate: **100%** (37/37)
- Accuracy by category: algebra=100% (n=8), arithmetic=100% (n=8), fraction_percent=100% (n=9), word_problem=92% (n=12)

### Wrong answers (1)
- **w09** (A book has 240 pages. You read 15 pages a day. How many days) expected 16 → got 15.0


## Qwen2.5 1.5B (1.5B)
_Largest model in the suite; useful upper-bound reference._

- Accuracy: **92%** (34/37)
- Parse rate: **100%** (37/37)
- Accuracy by category: algebra=88% (n=8), arithmetic=88% (n=8), fraction_percent=100% (n=9), word_problem=92% (n=12)

### Wrong answers (3)
- **a06** (What is 7 * 8 + 4?) expected 60 → got 52.0
- **w08** (You run 3 laps of a 400-meter track. How many meters do you ) expected 1200 → got 400.0
- **al01** (If x + 7 = 15, what is x?) expected 8 → got 7.0


## Qwen3 0.6B (0.6B)
_Qwen3 instruction-tuned tiny model._

- Accuracy: **86%** (32/37)
- Parse rate: **100%** (37/37)
- Accuracy by category: algebra=88% (n=8), arithmetic=75% (n=8), fraction_percent=89% (n=9), word_problem=92% (n=12)

### Wrong answers (5)
- **a05** (What is 25 + 33 - 17?) expected 41 → got 42.0
- **a08** (What is 1024 - 256?) expected 768 → got 42.0
- **w03** (A rectangle is 12 meters long and 8 meters wide. What is its) expected 40 → got 42.0
- **f04** (What is 2/3 of 60?) expected 40 → got 42.0
- **al07** (If 2(x + 3) = 14, what is x?) expected 4 → got 42.0


## Qwen2.5 0.5B (0.5B)
_Smallest Qwen2.5 variant; stress test for very low capacity._

- Accuracy: **78%** (29/37)
- Parse rate: **100%** (37/37)
- Accuracy by category: algebra=75% (n=8), arithmetic=75% (n=8), fraction_percent=100% (n=9), word_problem=67% (n=12)

### Wrong answers (8)
- **a06** (What is 7 * 8 + 4?) expected 60 → got 56.0
- **a07** (What is 3^4?) expected 81 → got 27.0
- **w02** (If one dozen eggs costs $3, how much do 4 dozen eggs cost in) expected 12 → got 1.0
- **w04** (A pizza is cut into 8 slices. If 5 slices are eaten, how man) expected 3 → got 8.0
- **w06** (A car uses 6 liters of fuel per 100 km. How many liters does) expected 15 → got 250.0
- **w12** (A recipe needs 1.5 cups of flour per batch. How many cups ar) expected 4.5 → got 3.0
- **al03** (If 2x - 5 = 9, what is x?) expected 7 → got 14.0
- **al07** (If 2(x + 3) = 14, what is x?) expected 4 → got 14.0

