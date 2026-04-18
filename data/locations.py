LOCATION_YIELDS = {
    "asteroid_field": {
        "iron_ore": (8, 20),
        "copper_ore": (3, 10),
        "silicon": (2, 8),
        "ice": (1, 5),
    },
    "rocky_planet": {
        "iron_ore": (5, 15),
        "copper_ore": (2, 8),
        "silicon": (1, 5),
        "ice": (0, 3),
    },
    "gas_giant": {
        "fuel": (10, 30),
        "ice": (5, 15),
    },
    "ice_moon": {
        "ice": (15, 40),
        "water": (5, 15),
    },
    "station": {},
}

STATION_TYPES = {
    "trading_post": {
        "name": "Trading Post",
        "description": "General goods and supplies at standard rates.",
        "price_modifier": 1.0,
        "available_items": [
            "metal", "electronics", "fuel", "water", "food",
            "iron_ore", "copper_ore", "silicon", "ice",
        ],
    },
    "shipyard": {
        "name": "Shipyard",
        "description": "Ship modules, hull repairs, and upgrades.",
        "price_modifier": 1.2,
        "available_items": ["metal", "electronics", "rare_minerals"],
    },
    "mining_outpost": {
        "name": "Mining Outpost",
        "description": "Raw materials at bargain prices.",
        "price_modifier": 0.8,
        "available_items": [
            "iron_ore", "copper_ore", "silicon", "ice", "rare_minerals",
        ],
    },
    "black_market": {
        "name": "Black Market",
        "description": "Rare goods, no questions asked.",
        "price_modifier": 1.5,
        "available_items": [
            "antimatter", "rare_minerals", "electronics", "fuel",
        ],
    },
}
