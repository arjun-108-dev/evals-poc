import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

rows = [
    # id, prompt, expected_tool, expected_args, category, difficulty
    ("e01", "What's the weather like in Tokyo right now?", "get_weather", {"location": "Tokyo"}, "should_call", "easy"),
    ("e02", "Set a timer for 10 minutes to take the pizza out of the oven.", "set_timer", {"duration_minutes": 10, "label": "take the pizza out of the oven"}, "multi_arg", "easy"),
    ("e03", "Text my mom and tell her I'll be home late.", "send_message", {"recipient": "mom", "message": "I'll be home late"}, "multi_arg", "medium"),
    ("e04", "Can you find contacts named Sarah in my address book?", "search_contacts", {"query": "Sarah"}, "should_call", "easy"),
    ("e05", "How are you today?", "none", None, "should_not_call", "easy"),
    ("e06", "Tell me a joke about cats.", "none", None, "should_not_call", "easy"),
    ("e07", "Remind me in 25 minutes to stretch.", "set_timer", {"duration_minutes": 25, "label": "stretch"}, "multi_arg", "easy"),
    ("e08", "Message David: are we still on for lunch tomorrow?", "send_message", {"recipient": "David", "message": "are we still on for lunch tomorrow?"}, "multi_arg", "medium"),
    ("e09", "What is the capital of France?", "none", None, "should_not_call", "easy"),
    ("e10", "Look up anyone called Ahmed in my contacts.", "search_contacts", {"query": "Ahmed"}, "should_call", "easy"),
    ("e11", "Is it raining in London?", "get_weather", {"location": "London"}, "should_call", "easy"),
    ("e12", "Set a 5 minute timer labeled 'tea'.", "set_timer", {"duration_minutes": 5, "label": "tea"}, "multi_arg", "easy"),
    ("e13", "Send a message to my boss saying I'm sick today.", "send_message", {"recipient": "boss", "message": "I'm sick today"}, "multi_arg", "medium"),
    ("e14", "Who won the world cup in 2018?", "none", None, "should_not_call", "medium"),
    ("e15", "Can you check the weather for New York City?", "get_weather", {"location": "New York City"}, "should_call", "easy"),
    ("e16", "Find my friend Michael in contacts.", "search_contacts", {"query": "Michael"}, "should_call", "easy"),
    ("e17", "Set timer 15 minutes for workout.", "set_timer", {"duration_minutes": 15, "label": "workout"}, "multi_arg", "easy"),
    ("e18", "Please message Emma that the meeting is moved to 3pm.", "send_message", {"recipient": "Emma", "message": "the meeting is moved to 3pm"}, "multi_arg", "medium"),
    ("e19", "Explain the theory of relativity in simple terms.", "none", None, "should_not_call", "medium"),
    ("e20", "What's the forecast for Sydney?", "get_weather", {"location": "Sydney"}, "should_call", "easy"),
    ("e21", "Search contacts for 'John'.", "search_contacts", {"query": "John"}, "should_call", "easy"),
    ("e22", "Timer for 45 minutes, label 'laundry'.", "set_timer", {"duration_minutes": 45, "label": "laundry"}, "multi_arg", "easy"),
    ("e23", "Send a text to Alex: 'Bring the documents please'.", "send_message", {"recipient": "Alex", "message": "Bring the documents please"}, "multi_arg", "medium"),
    ("e24", "Can you write me a poem about the ocean?", "none", None, "should_not_call", "easy"),
    ("e25", "Do I need an umbrella in Berlin?", "get_weather", {"location": "Berlin"}, "should_call", "easy"),
    ("e26", "Set a timer for two minutes to brush my teeth.", "set_timer", {"duration_minutes": 2, "label": "brush my teeth"}, "edge_case", "medium"),
    ("e27", "Message grandma happy birthday.", "send_message", {"recipient": "grandma", "message": "happy birthday"}, "edge_case", "medium"),
    ("e28", "Hello there, how's it going?", "none", None, "should_not_call", "easy"),
    ("e29", "Find contact Tom.", "search_contacts", {"query": "Tom"}, "should_call", "easy"),
    ("e30", "What is 2 plus 2?", "none", None, "should_not_call", "easy"),
    ("e31", "Thanks so much for your help!", "none", None, "should_not_call", "easy"),
    ("e32", "What time is it?", "none", None, "should_not_call", "easy"),
    ("e33", "Can you summarize that article I sent earlier?", "none", None, "should_not_call", "medium"),
    ("e34", "Good morning!", "none", None, "should_not_call", "easy"),
]

out = []
for r in rows:
    out.append({
        "id": r[0],
        "prompt": r[1],
        "expected_tool": r[2],
        "expected_args": r[3],
        "category": r[4],
        "difficulty": r[5],
    })

path = os.path.join(BASE, "data", "eval_dataset.jsonl")
with open(path, "w", encoding="utf-8") as f:
    for o in out:
        f.write(json.dumps(o, ensure_ascii=False) + "\n")

snc = sum(1 for o in out if o["category"] == "should_not_call")
print(f"wrote {len(out)} examples to {path}; should_not_call = {snc}")
