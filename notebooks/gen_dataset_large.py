#!/usr/bin/env python3
"""
gen_dataset_large.py
Deterministic generator for the 150-example pass^k tool-calling eval dataset.

Design targets (see project notes):
  - 150 examples total
  - category distribution: should_call ~40, multi_arg ~40, should_not_call ~35, edge_case ~35
  - difficulty distribution: easy ~45, medium ~55, hard ~50
  - single-shot accuracy in the 75-90% band for 0.3-1.5B models, so that pass^8 visibly
    degrades even though per-item accuracy looks fine.

No randomness is used -- every item is hand-authored below so the dataset is fully
reproducible (re-running this script always emits byte-identical output). This is
intentional: combinatorial random generation tends to produce shallow, repetitive
"hard" examples; the genuinely hard items here (entity distractors, unit conversion,
tool-choice near-synonyms, verbatim quoting) needed to be authored, not sampled.

Usage:
    python notebooks/gen_dataset_large.py > data/eval_dataset_large.jsonl
"""

import json
import sys

# Each entry: (id_suffix, prompt, expected_tool, expected_args, category, difficulty)
ITEMS = []


def add(prompt, tool, args, category, difficulty):
    ITEMS.append((prompt, tool, args, category, difficulty))


# ---------------------------------------------------------------------------
# SHOULD_CALL / get_weather (20: easy 11, medium 7, hard 2)
# ---------------------------------------------------------------------------
_easy_weather = [
    ("weather in Lagos please", "Lagos"),
    ("give me the current weather for Oslo", "Oslo"),
    ("how's the weather in Cape Town", "Cape Town"),
    ("check the weather in Toronto for me", "Toronto"),
    ("what's it like outside in Denver", "Denver"),
    ("I need the weather report for Dublin", "Dublin"),
    ("tell me the weather in Seoul", "Seoul"),
    ("weather check for Manila", "Manila"),
    ("current weather in Vienna?", "Vienna"),
    ("what's the temperature in Cairo right now", "Cairo"),
    ("give me a weather update for Lima", "Lima"),
]
for p, loc in _easy_weather:
    add(p, "get_weather", {"location": loc}, "should_call", "easy")

_medium_weather = [
    ("should I wear a coat in Chicago today", "Chicago"),
    ("is it sunny in Barcelona", "Barcelona"),
    ("will it snow in Helsinki this weekend", "Helsinki"),
    ("packing for a trip to Bangkok, what's it like there", "Bangkok"),
    ("is it cold in Reykjavik right now", "Reykjavik"),
    ("heading out in Nairobi, need to know the weather", "Nairobi"),
    ("how hot is it in Phoenix today", "Phoenix"),
]
for p, loc in _medium_weather:
    add(p, "get_weather", {"location": loc}, "should_call", "medium")

_hard_weather = [
    ("I'm comparing Paris and Rome for my trip but right now just tell me the weather in Rome", "Rome"),
    ("not sure if I should bike to work in Seattle, my cousin says it's nice in Miami but what's it doing in Seattle", "Seattle"),
]
for p, loc in _hard_weather:
    add(p, "get_weather", {"location": loc}, "should_call", "hard")

# ---------------------------------------------------------------------------
# SHOULD_CALL / search_contacts (20: easy 11, medium 7, hard 2)
# ---------------------------------------------------------------------------
_easy_contacts = [
    ("pull up Priya in my contacts", "Priya"),
    ("look for Wei in my address book", "Wei"),
    ("find Fatima in contacts", "Fatima"),
    ("search my contacts for Noah", "Noah"),
    ("do I have a contact named Elena", "Elena"),
    ("check contacts for Hiro", "Hiro"),
    ("look up Zainab please", "Zainab"),
    ("find someone named Carlos in my phone", "Carlos"),
    ("search for Aisha in contacts", "Aisha"),
    ("who is Mateo in my contacts", "Mateo"),
    ("pull up contact info for Lucia", "Lucia"),
]
for p, q in _easy_contacts:
    add(p, "search_contacts", {"query": q}, "should_call", "easy")

_medium_contacts = [
    ("is there a Jordan saved in my contacts", "Jordan"),
    ("can you dig through my contacts for someone called Renata", "Renata"),
    ("I'm trying to find Devon's contact card", "Devon"),
    ("check if Priyanka is in my address book", "Priyanka"),
    ("search my phone contacts for the name Omar", "Omar"),
    ("find contact details for Ingrid", "Ingrid"),
    ("look through contacts for anyone named Kwame", "Kwame"),
]
for p, q in _medium_contacts:
    add(p, "search_contacts", {"query": q}, "should_call", "medium")

_hard_contacts = [
    ("my brother Sam mentioned a coworker named Petra, can you find Petra in my contacts", "Petra"),
    ("I need Diego's number, not Marco's, look Diego up in contacts", "Diego"),
]
for p, q in _hard_contacts:
    add(p, "search_contacts", {"query": q}, "should_call", "hard")

# ---------------------------------------------------------------------------
# MULTI_ARG / set_timer (20: easy 5, medium 10, hard 5)
# ---------------------------------------------------------------------------
_easy_timer = [
    ("set a timer for 20 minutes labeled 'nap'", 20, "nap"),
    ("start an 8 minute timer for eggs", 8, "eggs"),
    ("timer for 3 minutes, label 'steep tea'", 3, "steep tea"),
    ("set a 12 minute timer for 'cookies'", 12, "cookies"),
    ("please set a timer for 30 minutes to water the plants", 30, "water the plants"),
]
for p, d, l in _easy_timer:
    add(p, "set_timer", {"duration_minutes": d, "label": l}, "multi_arg", "easy")

_medium_timer = [
    ("can you time 10 minutes for me while I meditate", 10, "meditate"),
    ("set a timer so I remember to check the oven in 40 minutes", 40, "check the oven"),
    ("I need a 7 minute timer for my run cooldown", 7, "run cooldown"),
    ("start a timer, 18 minutes, for charging my phone", 18, "charging my phone"),
    ("set one for 50 minutes labeled study session", 50, "study session"),
    ("can you set a countdown for 6 minutes to boil the pasta", 6, "boil the pasta"),
    ("give me a timer for twenty two minutes for laundry", 22, "laundry"),
    ("set a timer, call it 'break', for 15 minutes", 15, "break"),
    ("I want a timer for 9 minutes so I don't overcook the rice", 9, "don't overcook the rice"),
    ("set a reminder timer for 55 minutes for the roast", 55, "the roast"),
]
for p, d, l in _medium_timer:
    add(p, "set_timer", {"duration_minutes": d, "label": l}, "multi_arg", "medium")

_hard_timer = [
    ("set a timer for a quarter of an hour to check the mail", 15, "check the mail"),
    ("start a timer for ten minutes, not the five minute one I mentioned earlier, for pizza", 10, "pizza"),
    ("set a timer for two and a half minutes for the soft boiled egg", 2.5, "the soft boiled egg"),
    ("give me a timer for half an hour labeled 'yoga'", 30, "yoga"),
    ("set a timer for 90 seconds to steep the green tea", 1.5, "steep the green tea"),
]
for p, d, l in _hard_timer:
    add(p, "set_timer", {"duration_minutes": d, "label": l}, "multi_arg", "hard")

# ---------------------------------------------------------------------------
# MULTI_ARG / send_message (20: easy 5, medium 10, hard 5)
# ---------------------------------------------------------------------------
_easy_msg = [
    ("message Priya and say I'm running 10 minutes late", "Priya", "I'm running 10 minutes late"),
    ("send Tom a text saying happy anniversary", "Tom", "happy anniversary"),
    ("text Grace: see you at 7", "Grace", "see you at 7"),
    ("send a message to Noah saying good luck today", "Noah", "good luck today"),
    ("message Aunt Rita that dinner's ready", "Aunt Rita", "dinner's ready"),
]
for p, r, m in _easy_msg:
    add(p, "send_message", {"recipient": r, "message": m}, "multi_arg", "easy")

_medium_msg = [
    ("let Marcus know the flight got delayed", "Marcus", "the flight got delayed"),
    ("send a text to Dad: can you pick me up at 6", "Dad", "can you pick me up at 6"),
    ("tell Elena I'll call her after work", "Elena", "I'll call her after work"),
    ("send message to Yuki, tell her the package arrived", "Yuki", "the package arrived"),
    ("text Ben and let him know I'm on my way", "Ben", "I'm on my way"),
    ("message the landlord that the sink is leaking again", "landlord", "the sink is leaking again"),
    ("can you tell Priya the report is done", "Priya", "the report is done"),
    ("send a quick text to Owen saying thanks for today", "Owen", "thanks for today"),
    ("message Sophie: running 5 minutes behind schedule", "Sophie", "running 5 minutes behind schedule"),
    ("let coach know I can't make practice tonight", "coach", "I can't make practice tonight"),
]
for p, r, m in _medium_msg:
    add(p, "send_message", {"recipient": r, "message": m}, "multi_arg", "medium")

_hard_msg = [
    ("text Marco exactly this: 'don't forget the tickets, they're in the drawer'", "Marco",
     "don't forget the tickets, they're in the drawer"),
    ("I was going to message Liam but actually send this to Noah instead: the venue changed to the downtown location",
     "Noah", "the venue changed to the downtown location"),
    ("message my brother-in-law Karim and say 'congrats on the new job!!'", "Karim", "congrats on the new job!!"),
    ("send Priyanka a message that just says ok", "Priyanka", "ok"),
    ("text both... actually just Diego for now: meeting moved to Friday", "Diego", "meeting moved to Friday"),
]
for p, r, m in _hard_msg:
    add(p, "send_message", {"recipient": r, "message": m}, "multi_arg", "hard")

# ---------------------------------------------------------------------------
# SHOULD_NOT_CALL (35: easy 10, medium 15, hard 10)
# ---------------------------------------------------------------------------
_easy_none = [
    "what's up",
    "tell me a fun fact about octopuses",
    "how do you spell necessary",
    "what's 15 times 4",
    "goodnight",
    "who wrote Romeo and Juliet",
    "can you recommend a good book",
    "you're the best, thank you",
    "what day is it",
    "tell me a riddle",
]
for p in _easy_none:
    add(p, "none", None, "should_not_call", "easy")

_medium_none = [
    "what's the difference between a crocodile and an alligator",
    "can you help me brainstorm names for my new puppy",
    "explain how photosynthesis works",
    "summarize the plot of Romeo and Juliet for me",
    "what's a good recipe for banana bread",
    "how many ounces are in a gallon",
    "give me some tips for staying focused while studying",
    "what's the meaning of the word ephemeral",
    "can you help me write a birthday toast for my dad",
    "what year did the Berlin Wall fall",
    "explain the rules of chess to me",
    "give me a workout routine for beginners",
    "what's a synonym for happy",
    "can you proofread this sentence: 'me and him went to the store'",
    "what's the square root of 144",
]
for p in _medium_none:
    add(p, "none", None, "should_not_call", "medium")

_hard_none = [
    "how do I add a new contact named Priya to my phone",
    "cancel the timer I set for the eggs",
    "delete the last message I sent to Marcus",
    "who is the president of Portugal",
    "remind me tomorrow morning to call the dentist",
    "read me my last message from Sophie",
    "snooze my alarm for ten minutes",
    "call Priya on the phone",
    "check my calendar for tomorrow",
    "turn off the timer",
]
for p in _hard_none:
    add(p, "none", None, "should_not_call", "hard")

# ---------------------------------------------------------------------------
# EDGE_CASE (35: easy 3, medium 6, hard 26)
# ---------------------------------------------------------------------------
add("set a timer for 1 minute labeled 'quick check'", "set_timer",
    {"duration_minutes": 1, "label": "quick check"}, "edge_case", "easy")
add("message Theo and just say 'k'", "send_message",
    {"recipient": "Theo", "message": "k"}, "edge_case", "easy")
add("find Al in my contacts", "search_contacts", {"query": "Al"}, "edge_case", "easy")

_medium_edge = [
    ("can you check contacts real quick, I'm looking for someone named Lee",
     "search_contacts", {"query": "Lee"}),
    ("set a timer, 25 minutes, don't forget the label this time: 'bread'",
     "set_timer", {"duration_minutes": 25, "label": "bread"}),
    ("message Nora, quote: 'see you soon'",
     "send_message", {"recipient": "Nora", "message": "see you soon"}),
    ("weather-wise, how's Jakarta looking",
     "get_weather", {"location": "Jakarta"}),
    ("is Priti in my contact list or not",
     "search_contacts", {"query": "Priti"}),
    ("set a fifteen minute timer, label it 'call mom'",
     "set_timer", {"duration_minutes": 15, "label": "call mom"}),
]
for p, tool, args in _medium_edge:
    add(p, tool, args, "edge_case", "medium")

_hard_edge = [
    # near-synonym tool-choice confusion
    ("find out how the weather's doing in Prague", "get_weather", {"location": "Prague"}),
    ("look up the weather for Warsaw", "get_weather", {"location": "Warsaw"}),
    ("search for the current conditions in Vancouver", "get_weather", {"location": "Vancouver"}),
    ("can you check if Marco is around, look him up in my contacts", "search_contacts", {"query": "Marco"}),
    ("text Priya... actually no, just set a timer for 20 minutes labeled gym",
     "set_timer", {"duration_minutes": 20, "label": "gym"}),
    ("call it a 'break' and set the timer for 12 minutes",
     "set_timer", {"duration_minutes": 12, "label": "break"}),
    ("search contacts... wait, just message Elif that I'm outside",
     "send_message", {"recipient": "Elif", "message": "I'm outside"}),
    # multiple entities / wrong entity pick
    ("text Sam, no wait, text Sara instead: I'm almost there",
     "send_message", {"recipient": "Sara", "message": "I'm almost there"}),
    ("weather in Rio de Janeiro, not Sao Paulo, please", "get_weather", {"location": "Rio de Janeiro"}),
    ("find Ana in contacts, she's not the same Ana from work, the one from college",
     "search_contacts", {"query": "Ana"}),
    ("set a timer for the cookies, 12 minutes, not the 20 minute one for the bread",
     "set_timer", {"duration_minutes": 12, "label": "cookies"}),
    ("message Grandpa Joe, I mean my actual grandfather not my uncle who everyone calls Grandpa Joe: dinner's at 6",
     "send_message", {"recipient": "Grandpa Joe", "message": "dinner's at 6"}),
    ("search my contacts for Kim — I think there's more than one but just find Kim",
     "search_contacts", {"query": "Kim"}),
    # number-word / unit conversions
    ("set a timer for a minute and a half to steam the dumplings",
     "set_timer", {"duration_minutes": 1.5, "label": "steam the dumplings"}),
    ("give me a two hour timer labeled 'slow cook'",
     "set_timer", {"duration_minutes": 120, "label": "slow cook"}),
    ("set a timer for forty five minutes for the marinade",
     "set_timer", {"duration_minutes": 45, "label": "the marinade"}),
    ("start a timer for 1 hour and 15 minutes labeled 'roast turkey'",
     "set_timer", {"duration_minutes": 75, "label": "roast turkey"}),
    ("set a timer for thirty seconds labeled 'quick check'",
     "set_timer", {"duration_minutes": 0.5, "label": "quick check"}),
    # verbatim quote / punctuation preservation
    ("text Layla exactly: \"don't wait up, I'll be late — traffic is insane!!\"",
     "send_message", {"recipient": "Layla", "message": "don't wait up, I'll be late — traffic is insane!!"}),
    ("message Farid word for word: 'meeting's at 9, bring the slides.'",
     "send_message", {"recipient": "Farid", "message": "meeting's at 9, bring the slides."}),
    ("send this exact message to Priti — 'ok, see you then :)'",
     "send_message", {"recipient": "Priti", "message": "ok, see you then :)"}),
    # extra irrelevant detail
    ("so I was at the gym earlier and totally forgot, but can you check the weather in Montreal for me",
     "get_weather", {"location": "Montreal"}),
    ("my phone's been acting up all day but anyway, find Yusuf in my contacts",
     "search_contacts", {"query": "Yusuf"}),
    ("ugh long day, can you set a 10 minute timer for a power nap",
     "set_timer", {"duration_minutes": 10, "label": "power nap"}),
    ("quick one before I forget, message Tariq that I'll send the invoice tomorrow",
     "send_message", {"recipient": "Tariq", "message": "I'll send the invoice tomorrow"}),
    # tool-choice vs. should_not_call trap
    ("find out what time it is in Berlin", "none", None),
]
for entry in _hard_edge:
    p, tool, args = entry
    add(p, tool, args, "edge_case", "hard")


def main():
    lines = []
    for i, (prompt, tool, args, category, difficulty) in enumerate(ITEMS, start=1):
        obj = {
            "id": f"n{i:03d}",
            "prompt": prompt,
            "expected_tool": tool,
            "expected_args": args,
            "category": category,
            "difficulty": difficulty,
        }
        lines.append(json.dumps(obj, ensure_ascii=False))
    sys.stdout.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
