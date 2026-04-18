"""Dead Sun - Game data definitions."""

# Tile types on the ship grid
EMPTY = 0   # vacuum/space
FLOOR = 1   # hull floor (buildable)

# Module definitions: symbol, name, power_use, oxygen_use, crew_slots, build_cost
MODULES = {
    "cockpit":      {"sym": "🎮", "name": "Cockpit",       "pwr": 1, "o2": 1, "crew": 1, "cost": {}},
    "reactor":      {"sym": "⚡", "name": "Reactor",        "pwr": -5, "o2": 0, "crew": 1, "cost": {"metal": 20, "electronics": 5}},
    "engine":       {"sym": "🔧", "name": "Engine",         "pwr": 2, "o2": 0, "crew": 1, "cost": {"metal": 15, "electronics": 10}},
    "life_support": {"sym": "🫁", "name": "Life Support",   "pwr": 2, "o2": -6, "crew": 1, "cost": {"metal": 10, "electronics": 5}},
    "habitat":      {"sym": "🏠", "name": "Habitat",        "pwr": 1, "o2": 2, "crew": 0, "cost": {"metal": 15}},
    "cargo_bay":    {"sym": "📦", "name": "Cargo Bay",      "pwr": 0, "o2": 0, "crew": 0, "cost": {"metal": 10}},
    "mining_drill": {"sym": "⛏️", "name": "Mining Drill",   "pwr": 3, "o2": 1, "crew": 1, "cost": {"metal": 20, "electronics": 10}},
    "refinery":     {"sym": "🔥", "name": "Refinery",       "pwr": 3, "o2": 1, "crew": 1, "cost": {"metal": 25, "electronics": 15}},
    "scanner":      {"sym": "📡", "name": "Scanner",        "pwr": 1, "o2": 0, "crew": 1, "cost": {"metal": 10, "electronics": 20}},
    "shield":       {"sym": "🛡️", "name": "Shield",         "pwr": 4, "o2": 0, "crew": 1, "cost": {"metal": 30, "electronics": 20}},
    "farm":         {"sym": "🌱", "name": "Farm",           "pwr": 2, "o2": -1, "crew": 1, "cost": {"metal": 10, "electronics": 5}},
    "workshop":     {"sym": "🔩", "name": "Workshop",       "pwr": 2, "o2": 1, "crew": 1, "cost": {"metal": 20, "electronics": 15}},
}

HULL_COST = {"metal": 10}

# How much cargo each cargo bay holds
CARGO_PER_BAY = 20

# Refining recipes: {output: {inputs, per_batch}
REFINE_RECIPES = {
    "metal":      {"inputs": {"iron_ore": 3},  "output": 1, "days": 1},
    "electronics": {"inputs": {"copper_ore": 2, "silicon": 1}, "output": 1, "days": 2},
    "fuel":       {"inputs": {"ice": 2},       "output": 3, "days": 1},
    "water":      {"inputs": {"ice": 1},       "output": 2, "days": 1},
}

# Mining yields per location type (resource: (min, max))
LOCATION_YIELDS = {
    "asteroid_field": {"iron_ore": (8, 20), "copper_ore": (3, 10), "silicon": (2, 8), "ice": (1, 5)},
    "rocky_planet":   {"iron_ore": (5, 15), "copper_ore": (2, 8), "silicon": (1, 5), "ice": (0, 3)},
    "gas_giant":      {"fuel": (10, 30), "ice": (5, 15)},
    "ice_moon":       {"ice": (15, 40), "water": (5, 15)},
    "station":        {},
}

# Crew first/last name pools
FIRST_NAMES = ["Chen", "Vasquez", "Okonkwo", "Kim", "Petrov", "Singh", "Müller", "Nakamura", "O'Brien", "Johansson",
               "Patel", "Santos", "Yamamoto", "Williams", "Ivanova", "Hoffman", "Zhao", "Ali", "Larsson", "Costa"]
LAST_NAMES = ["Elara", "James", "Voss", "Reyes", "Kato", "Shaw", "Park", "Fischer", "Okafor", "Lindgren",
              "Torres", "Chandra", "Eriksson", "Osei", "Bakker", "Novak", "Ahmed", "Berg", "Medina", "Sato"]

SKILLS = ["piloting", "engineering", "mining", "science", "medical", "command"]

# Game screens
SCREENS = ["ship", "map", "crew", "cargo", "systems"]

# Colors (curses pair numbers)
CLR_TITLE = 1
CLR_GOOD = 2
CLR_WARN = 3
CLR_BAD = 4
CLR_HIGHLIGHT = 5
CLR_DIM = 6
CLR_MODULE = 7
CLR_CURSOR = 8
CLR_BORDER = 9

# Day ticks
FOOD_PER_CREW_PER_DAY = 1
OXYGEN_PER_CREW_PER_DAY = 1
FUEL_PER_TRAVEL = 5
MINE_DAYS = 1
