"""Dead Sun - Solar system, locations, and travel."""

import random
from data import LOCATION_YIELDS, FUEL_PER_TRAVEL
from crew import CrewMember


class Location:
    def __init__(self, name, loc_type, row, col, description="", resources=None):
        self.name = name
        self.loc_type = loc_type
        self.row = row
        self.col = col
        self.description = description
        self.resources = resources or LOCATION_YIELDS.get(loc_type, {}).copy()
        self.explored = loc_type == "station"
        self.symbol = {
            "star": "☀️",
            "asteroid_field": "☄️",
            "rocky_planet": "🌍",
            "gas_giant": "🪐",
            "ice_moon": "🧊",
            "station": "🏗️",
            "moon": "🌙",
            "warp_gate": "🌀",
        }.get(loc_type, "?")

    def distance_to(self, other):
        return abs(self.row - other.row) + abs(self.col - other.col)

    def mine(self, drill_count=0, miner_skill=1):
        """Mine resources. Returns dict of resources gathered."""
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


class SolarSystem:
    def __init__(self):
        self.locations = []
        self._generate()

    def _generate(self):
        self.locations = [
            Location("Sol",        "star",           0,  4, "The dying sun. A red giant on its last breath."),
            Location("Hermes",     "rocky_planet",    2,  3, "A scorched world rich in iron and copper."),
            Location("Aphrodite",  "rocky_planet",    3,  6, "Thick atmosphere. Trace minerals on the surface."),
            Location("The Belt",   "asteroid_field",  5,  2, "A dense field of asteroids. Mining paradise."),
            Location("Gaia",       "rocky_planet",    5,  5, "Once habitable. Ruins of an old colony."),
            Location("Outpost 7",  "station",         5,  7, "A trading post. Last stop before the outer system."),
            Location("Tartarus",   "gas_giant",       7,  1, "A massive gas giant. Fuel harvesting possible."),
            Location("Europa",     "ice_moon",        8,  3, "Frozen moon. Rich in ice and water."),
            Location("Kuiper Drift", "asteroid_field", 9,  0, "The edge of the system. Rare minerals."),
            Location("The Maw",    "asteroid_field",  9,  7, "Dangerous debris field. High reward, high risk."),
        ]
        self.locations[5].explored = True  # station

    def get_location(self, name):
        for loc in self.locations:
            if loc.name == name:
                return loc
        return None

    def travel_cost(self, from_loc, to_loc):
        dist = from_loc.distance_to(to_loc)
        return max(1, dist * FUEL_PER_TRAVEL)


class GameState:
    def __init__(self):
        from ship import Ship
        from crew import CrewRoster

        self.ship = Ship(16, 10)
        self.ship.apply_starter_layout()
        self.roster = CrewRoster()
        self.cargo = {"metal": 10, "electronics": 3, "fuel": 20, "food": 15, "ice": 0,
                       "iron_ore": 0, "copper_ore": 0, "silicon": 0, "water": 5}
        self.system = SolarSystem()
        self.current_location = self.system.get_location("Outpost 7")
        self.day = 1
        self.log = []
        self.screen = "ship"
        self.cursor_r = 4
        self.cursor_c = 6
        self.selected_crew = 0
        self.selected_location = 0
        self.selected_recipe = 0
        self.build_menu_open = False
        self.build_choice = 0
        self.running = True
        self.message = ""
        self.message_timer = 0

        starter_crew = [
            CrewMember("Chen Vasquez", "commander"),
            CrewMember("Kim Okonkwo", "engineer"),
            CrewMember("Singh Müller", "miner"),
        ]
        for c in starter_crew:
            self.roster.add(c)

        self.log_event("Dead Sun initialized. You awaken at Outpost 7.")
        self.log_event("Your ship is damaged. Explore, mine, and rebuild.")

    def log_event(self, text):
        self.log.append(f"Day {self.day}: {text}")
        if len(self.log) > 100:
            self.log = self.log[-100:]

    def show_message(self, text, duration=3):
        self.message = text
        self.message_timer = duration

    def can_afford(self, cost):
        for res, amt in cost.items():
            if self.cargo.get(res, 0) < amt:
                return False
        return True

    def spend(self, cost):
        for res, amt in cost.items():
            self.cargo[res] -= amt

    def receive(self, resources):
        for res, amt in resources.items():
            self.cargo[res] = self.cargo.get(res, 0) + amt

    def has_cargo_space(self, amount):
        return self.ship.get_total_cargo(self.cargo) + amount <= self.ship.get_cargo_capacity()

    def advance_day(self):
        self.day += 1
        self.roster.tick_all()
        # Consume food
        food_needed = self.roster.total_food_needed()
        if self.cargo.get("food", 0) >= food_needed:
            self.cargo["food"] -= food_needed
            self.roster.feed_all()
        else:
            self.log_event("⚠ Not enough food! Crew is starving!")
        # Oxygen check
        _, o2_use = self.ship.get_oxygen_balance()
        o2_gen, _ = self.ship.get_oxygen_balance()
        if o2_gen < o2_use:
            self.log_event("⚠ Oxygen shortage! Crew health declining!")
            for m in self.roster.members:
                m.health = max(0, m.health - 5)
        # Message timer
        if self.message_timer > 0:
            self.message_timer -= 1

    def do_mine(self):
        if self.current_location.resources is None or len(self.current_location.resources) == 0:
            self.show_message("Nothing to mine here.")
            return
        drill_count = self.ship.count_module("mining_drill")
        # Find best miner
        miner_skill = 1
        for m in self.roster.members:
            if m.assigned_to:
                mt = self.ship.get_module_at(*m.assigned_to)
                if mt == "mining_drill":
                    miner_skill = max(miner_skill, m.skill("mining"))
        if drill_count == 0:
            drill_count = 0.5  # bare hands, very slow
        results = self.current_location.mine(drill_count, miner_skill)
        total = sum(results.values())
        if not self.has_cargo_space(total):
            self.show_message("Cargo full! Can't mine.")
            return
        self.receive(results)
        self.advance_day()
        parts = ", ".join(f"{v} {k}" for k, v in results.items())
        self.log_event(f"Mined: {parts}")
        self.show_message(f"Mined: {parts}")

    def do_refine(self, recipe_name):
        from data import REFINE_RECIPES
        if recipe_name not in REFINE_RECIPES:
            return
        recipe = REFINE_RECIPES[recipe_name]
        if not self.can_afford(recipe["inputs"]):
            self.show_message("Not enough materials to refine.")
            return
        if self.ship.count_module("refinery") == 0:
            self.show_message("No refinery on ship!")
            return
        self.spend(recipe["inputs"])
        self.receive({recipe_name: recipe["output"]})
        self.advance_day()
        inputs_str = ", ".join(f"{v} {k}" for k, v in recipe["inputs"].items())
        self.log_event(f"Refined: {inputs_str} → {recipe['output']} {recipe_name}")
        self.show_message(f"Refined {recipe['output']} {recipe_name}")

    def do_travel(self, destination):
        if destination.name == self.current_location.name:
            self.show_message("Already here.")
            return
        cost = self.system.travel_cost(self.current_location, destination)
        if self.cargo.get("fuel", 0) < cost:
            self.show_message(f"Need {cost} fuel to travel there.")
            return
        engine_count = self.ship.count_module("engine")
        if engine_count == 0:
            self.show_message("No engines! Can't travel.")
            return
        self.cargo["fuel"] -= cost
        travel_days = max(1, destination.distance_to(self.current_location) - engine_count)
        for _ in range(travel_days):
            self.advance_day()
        self.current_location = destination
        if not destination.explored:
            destination.explored = True
            self.log_event(f"Discovered: {destination.name} - {destination.description}")
        self.log_event(f"Arrived at {destination.name} (used {cost} fuel, {travel_days} days)")
        self.show_message(f"Arrived at {destination.name}")
