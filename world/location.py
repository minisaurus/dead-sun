import random
from data.locations import LOCATION_YIELDS, STATION_TYPES
from data.items import RESOURCES, TRADE_PRICES


class Location:
    def __init__(self, name, loc_type, row, col, description="", resources=None):
        self.name = name
        self.loc_type = loc_type
        self.row = row
        self.col = col
        self.description = description
        self.resources = resources or LOCATION_YIELDS.get(loc_type, {}).copy()
        self.explored = loc_type == "station"
        self.station_type = None
        self.danger_level = 0
        self.market = {}
        self.symbol = {
            "star": "☀️", "asteroid_field": "☄️", "rocky_planet": "🌍",
            "gas_giant": "🪐", "ice_moon": "🧊", "station": "🏗️",
            "moon": "🌙", "warp_gate": "🌀",
        }.get(loc_type, "?")

    def is_station(self):
        return self.loc_type == "station"

    def generate_market(self):
        if not self.is_station():
            return
        stype = STATION_TYPES.get(self.station_type, {})
        price_mod = stype.get("price_modifier", 1.0)
        available = stype.get("available_items", [])
        trade_mods = TRADE_PRICES.get(self.station_type, {"buy": 1.0, "sell": 0.8})
        self.market = {}
        for item in available:
            base = RESOURCES.get(item, {}).get("base_price", 10)
            self.market[item] = {
                "buy": int(base * price_mod * trade_mods["buy"]),
                "sell": int(base * price_mod * trade_mods["sell"]),
            }

    def distance_to(self, other):
        return abs(self.row - other.row) + abs(self.col - other.col)

    def mine(self, drill_count=0, miner_skill=1):
        if not self.resources:
            return {}
        results = {}
        for res, (lo, hi) in self.resources.items():
            base = random.randint(lo, hi)
            bonus = int(base * (0.2 * drill_count))
            skill_bonus = int(base * (0.1 * miner_skill))
            total = base + bonus + skill_bonus
            if total > 0:
                results[res] = total
        return results
