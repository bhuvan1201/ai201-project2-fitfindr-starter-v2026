"""Unit 4 baseline: five trials per criterion, fixed before model results."""

TEE = "vintage graphic tee under $30"
EMPTY = "designer ballgown size XXS under $5"
JACKET = "90s track jacket size M"

SCENARIOS = [
    {"name": "Matching query completes all tools", "criterion": 1, "target": "4 of 5",
     "query": TEE, "wardrobe": "example"},
    {"name": "Impossible query stops before outfit tool", "criterion": 2, "target": "5 of 5",
     "query": EMPTY, "wardrobe": "example"},
    {"name": "Each request keeps its own state", "criterion": 3, "target": "5 of 5",
     "sequence": [
         {"query": TEE, "wardrobe": "example"},
         {"query": EMPTY, "wardrobe": "example"},
         {"query": JACKET, "wardrobe": "example"},
     ]},
    {"name": "Fit card reports listing facts", "criterion": 4, "target": "4 of 5",
     "variants": [
         {"query": TEE, "wardrobe": "example"},
         {"query": JACKET, "wardrobe": "example"},
         {"query": "corduroy wide leg pants under $35", "wardrobe": "example"},
         {"query": "platform sneakers size 8", "wardrobe": "example"},
         {"query": "denim jacket under $50", "wardrobe": "example"},
     ]},
    {"name": "Outfit advice does not invent ownership", "criterion": 5, "target": "5 of 5",
     "variants": [
         {"query": JACKET, "wardrobe": "example"},
         {"query": JACKET, "wardrobe": "example"},
         {"query": JACKET, "wardrobe": "single"},
         {"query": JACKET, "wardrobe": "single"},
         {"query": JACKET, "wardrobe": "empty"},
     ]},
]

WARDROBES = ("example", "single", "empty")


def requests_for_try(scenario, attempt):
    """A state trial is three requests; a variant trial uses its fixed input."""
    if "sequence" in scenario:
        return scenario["sequence"]
    if "variants" in scenario:
        return [scenario["variants"][(attempt - 1) % len(scenario["variants"])]]
    return [scenario]


def validate():
    problems = []
    for scenario in SCENARIOS:
        if len(scenario.get("variants", [None] * 5)) != 5:
            problems.append(f"{scenario['name']}: expected five variants")
        for request in scenario.get("sequence", scenario.get("variants", [scenario])):
            if not request.get("query", "").strip():
                problems.append(f"{scenario['name']}: missing query")
            if request.get("wardrobe") not in WARDROBES:
                problems.append(f"{scenario['name']}: unknown wardrobe")
    if sorted(s["criterion"] for s in SCENARIOS) != [1, 2, 3, 4, 5]:
        problems.append("Expected exactly one scenario per criterion, 1–5")
    return problems
