# Evaluation Failures & Notable Cases

Generated automatically by `evaluator/analyze.py`. All results below are from **real** model runs via Ollama (no synthetic data).

## Model ranking (by overall score)

| Rank | Model | Size | Call Acc | Arg Acc | Abstain | FPR | Overall | Avg ms |
|------|-------|------|---------:|--------:|--------:|----:|--------:|--------:|
| 1 | Qwen3 0.6B | 0.6B | 100% | 95% | 100% | 0% | 0.989 | 5149 |
| 2 | Qwen2.5 1.5B | 1.5B | 100% | 86% | 92% | 8% | 0.949 | 3632 |
| 3 | Qwen2.5 0.5B | 0.5B | 95% | 82% | 25% | 75% | 0.784 | 6558 |
| 4 | Gemma 3 1B | 1B | 73% | 23% | 17% | 83% | 0.517 | 4711 |
| 5 | FunctionGemma 270M | 270M | 5% | 5% | 92% | 8% | 0.315 | 15184 |

## Qwen3 0.6B (0.6B)
_Qwen3 instruction-tuned tiny model._

- Tool accuracy: **100%** (34/34)
- Argument accuracy: **95%** (21/22)
- False positive rate: **0%** (0/12)
- Accuracy by category: unknown=100% (n=34)

### Right tool, wrong args (1)
- **e02** `set_timer`: expected {"duration_minutes": 10, "label": "take the pizza out of the oven"} → got {"duration_minutes": 10, "label": "take pizza out"}


## Qwen2.5 1.5B (1.5B)
_Largest model in the suite; useful upper-bound reference._

- Tool accuracy: **97%** (33/34)
- Argument accuracy: **86%** (19/22)
- False positive rate: **8%** (1/12)
- Accuracy by category: unknown=97% (n=34)

### False positives (1) - called a tool when none was needed
- **e09** (What is the capital of France?) → called `search_contacts` args={"query": "capital of France"}

### Right tool, wrong args (3)
- **e02** `set_timer`: expected {"duration_minutes": 10, "label": "take the pizza out of the oven"} → got {"duration_minutes": 10, "label": "Take Pizza Out"}
- **e13** `send_message`: expected {"recipient": "boss", "message": "I'm sick today"} → got {"recipient": "boss", "message": "I'm feeling sick today and won't be able to work."}
- **e26** `set_timer`: expected {"duration_minutes": 2, "label": "brush my teeth"} → got {"duration_minutes": 2, "label": "Brushing Teeth Timer"}


## Qwen2.5 0.5B (0.5B)
_Smallest Qwen2.5 variant; stress test for very low capacity._

- Tool accuracy: **71%** (24/34)
- Argument accuracy: **82%** (18/22)
- False positive rate: **75%** (9/12)
- Accuracy by category: unknown=71% (n=34)

### False positives (9) - called a tool when none was needed
- **e05** (How are you today?) → called `search_contacts` args={"query": "today"}
- **e06** (Tell me a joke about cats.) → called `send_message` args={"recipient": "cat", "message": "Why don't cats like Mondays? Because they're always late for work."}
- **e09** (What is the capital of France?) → called `search_contacts` args={"query": "France"}
- **e14** (Who won the world cup in 2018?) → called `search_contacts` args={"query": "World Cup 2018 winner"}
- **e28** (Hello there, how's it going?) → called `search_contacts` args={"query": "hello"}
- **e30** (What is 2 plus 2?) → called `get_weather` args={"location": "Paris"}
- **e32** (What time is it?) → called `get_weather` args={"location": "Paris"}
- **e33** (Can you summarize that article I sent earlier?) → called `send_message` args={"recipient": "user@example.com", "message": "I sent an article to you. Here it is: [insert article text here]"}
- **e34** (Good morning!) → called `send_message` args={"recipient": "John Doe", "message": "Good morning! How can I assist you today?"}

### Wrong / missing tool (1)
- **e25** expected `get_weather` → got `search_contacts` (prompt: Do I need an umbrella in Berlin?)

### Right tool, wrong args (3)
- **e02** `set_timer`: expected {"duration_minutes": 10, "label": "take the pizza out of the oven"} → got {"duration_minutes": 10, "label": "Pizzas out of the oven"}
- **e12** `set_timer`: expected {"duration_minutes": 5, "label": "tea"} → got {"duration_minutes": 30, "label": "tea"}
- **e26** `set_timer`: expected {"duration_minutes": 2, "label": "brush my teeth"} → got {"duration_minutes": 2, "label": "Brush teeth"}


## Gemma 3 1B (1B)
_General-purpose tiny multimodal model. Not specifically trained for tool use._

- Tool accuracy: **53%** (18/34)
- Argument accuracy: **23%** (5/22)
- False positive rate: **83%** (10/12)
- Accuracy by category: unknown=53% (n=34)

### False positives (10) - called a tool when none was needed
- **e05** (How are you today?) → called `get_weather` args={"location": "London"}
- **e09** (What is the capital of France?) → called `get_weather` args={"location": "Paris"}
- **e14** (Who won the world cup in 2018?) → called `get_weather` args={"location": "Brazil"}
- **e19** (Explain the theory of relativity in simple terms.) → called `get_weather` args={"location": "London"}
- **e24** (Can you write me a poem about the ocean?) → called `Ocean's Whisper` args={"search_contacts": null}
- **e28** (Hello there, how's it going?) → called `get_weather` args={"location": "London"}
- **e30** (What is 2 plus 2?) → called `get_weather` args={"location": "London"}
- **e32** (What time is it?) → called `get_weather` args={"location": "London"}
- **e33** (Can you summarize that article I sent earlier?) → called `get_weather` args={"location": "London"}
- **e34** (Good morning!) → called `get_weather` args={"location": "London"}

### Wrong / missing tool (6)
- **e02** expected `set_timer` → got `get_timer` (prompt: Set a timer for 10 minutes to take the pizza out o)
- **e10** expected `search_contacts` → got `Ahmed` (prompt: Look up anyone called Ahmed in my contacts.)
- **e12** expected `set_timer` → got `get_timer` (prompt: Set a 5 minute timer labeled 'tea'.)
- **e17** expected `set_timer` → got `get_timer` (prompt: Set timer 15 minutes for workout.)
- **e22** expected `set_timer` → got `get_timer` (prompt: Timer for 45 minutes, label 'laundry'.)
- **e26** expected `set_timer` → got `get_timer` (prompt: Set a timer for two minutes to brush my teeth.)

### Right tool, wrong args (11)
- **e03** `send_message`: expected {"recipient": "mom", "message": "I'll be home late"} → got {"to": "Mom", "message": "I'll be home late."}
- **e04** `search_contacts`: expected {"query": "Sarah"} → got {"contact_type": "Sarah"}
- **e07** `set_timer`: expected {"duration_minutes": 25, "label": "stretch"} → got {"time": "25 minutes"}
- **e08** `send_message`: expected {"recipient": "David", "message": "are we still on for lunch tomorrow?"} → got {"to": "David", "message": "Are we still on for lunch tomorrow?"}
- **e13** `send_message`: expected {"recipient": "boss", "message": "I'm sick today"} → got {"to": "boss", "message": "I'm sick today."}
- **e16** `search_contacts`: expected {"query": "Michael"} → got {"contact": "Michael"}
- **e18** `send_message`: expected {"recipient": "Emma", "message": "the meeting is moved to 3pm"} → got {"to": "Emma", "message": "The meeting is moved to 3pm."}
- **e21** `search_contacts`: expected {"query": "John"} → got {"contact": "John"}
- **e23** `send_message`: expected {"recipient": "Alex", "message": "Bring the documents please"} → got {"to": "Alex"}
- **e27** `send_message`: expected {"recipient": "grandma", "message": "happy birthday"} → got {"to": "grandma", "message": "Happy birthday!"}
- **e29** `search_contacts`: expected {"query": "Tom"} → got {"contact_name": "Tom"}


## FunctionGemma 270M (270M)
_Purpose-built function-calling model from Google. Smallest model in the suite._

- Tool accuracy: **35%** (12/34)
- Argument accuracy: **5%** (1/22)
- False positive rate: **8%** (1/12)
- Accuracy by category: unknown=35% (n=34)

### False positives (1) - called a tool when none was needed
- **e09** (What is the capital of France?) → called `get_weather` args={"location": "Paris"}

### Wrong / missing tool (21)
- **e01** expected `get_weather` → got `(none)` (prompt: What's the weather like in Tokyo right now?)
- **e02** expected `set_timer` → got `(none)` (prompt: Set a timer for 10 minutes to take the pizza out o)
- **e03** expected `send_message` → got `(none)` (prompt: Text my mom and tell her I'll be home late.)
- **e04** expected `search_contacts` → got `get_weather` (prompt: Can you find contacts named Sarah in my address bo)
- **e07** expected `set_timer` → got `(none)` (prompt: Remind me in 25 minutes to stretch.)
- **e08** expected `send_message` → got `(none)` (prompt: Message David: are we still on for lunch tomorrow?)
- **e10** expected `search_contacts` → got `get_weather` (prompt: Look up anyone called Ahmed in my contacts.)
- **e11** expected `get_weather` → got `(none)` (prompt: Is it raining in London?)
- **e12** expected `set_timer` → got `(none)` (prompt: Set a 5 minute timer labeled 'tea'.)
- **e13** expected `send_message` → got `(none)` (prompt: Send a message to my boss saying I'm sick today.)
- **e16** expected `search_contacts` → got `(none)` (prompt: Find my friend Michael in contacts.)
- **e17** expected `set_timer` → got `(none)` (prompt: Set timer 15 minutes for workout.)
- ...and 9 more.

