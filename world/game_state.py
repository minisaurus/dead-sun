from world.galaxy import Galaxy
from ship import Ship, Fleet
from crew import CrewMember, CrewRoster
from data.modules import REFINE_RECIPES


class GameState:
    def __init__(self):
        self.fleet = Fleet()
        starter = Ship(16, 10)
        starter.apply_starter_layout()
        self.fleet.add_ship(starter)
        self.ship = self.fleet.active_ship
        self.roster = CrewRoster()
        self.cargo = {
            "metal": 10, "electronics": 3, "fuel": 20, "food": 15, "ice": 0,
            "iron_ore": 0, "copper_ore": 0, "silicon": 0, "water": 5,
        }
        self.galaxy = Galaxy()
        self.system = self.galaxy.systems[0]
        self.current_system = self.galaxy.systems[0]
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
        self.credits = 100
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
        food_needed = self.roster.total_food_needed()
        if self.cargo.get("food", 0) >= food_needed:
            self.cargo["food"] -= food_needed
            self.roster.feed_all()
        else:
            self.log_event("Not enough food! Crew is starving!")
        _, o2_use = self.ship.get_oxygen_balance()
        o2_gen, _ = self.ship.get_oxygen_balance()
        if o2_gen < o2_use:
            self.log_event("Oxygen shortage! Crew health declining!")
            for m in self.roster.members:
                m.health = max(0, m.health - 5)
        if self.message_timer > 0:
            self.message_timer -= 1

    def do_mine(self):
        if self.current_location.resources is None or len(self.current_location.resources) == 0:
            self.show_message("Nothing to mine here.")
            return
        drill_count = self.ship.count_module("mining_drill")
        miner_skill = 1
        for m in self.roster.members:
            if m.assigned_to:
                mt = self.ship.get_module_at(*m.assigned_to)
                if mt == "mining_drill":
                    miner_skill = max(miner_skill, m.skill("mining"))
        if drill_count == 0:
            drill_count = 0.5
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
        self.log_event(f"Refined: {inputs_str} -> {recipe['output']} {recipe_name}")
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

    def do_ftl_travel(self, target_system):
        if target_system.name == self.current_system.name:
            self.show_message("Already in this system.")
            return
        if self.ship.count_module("ftl_drive") == 0:
            self.show_message("No FTL drive installed!")
            return
        cost = self.galaxy.ftl_cost(self.current_system, target_system)
        if self.cargo.get("fuel", 0) < cost:
            self.show_message(f"Need {cost} fuel for FTL jump.")
            return
        self.cargo["fuel"] -= cost
        self.current_system = target_system
        self.system = target_system
        arrival = None
        for loc in target_system.locations:
            if loc.is_station():
                arrival = loc
                break
        if arrival is None:
            arrival = target_system.locations[0]
        self.current_location = arrival
        if not arrival.explored:
            arrival.explored = True
            self.log_event(f"Discovered: {arrival.name} - {arrival.description}")
        for _ in range(3):
            self.advance_day()
        self.log_event(f"FTL jump to {target_system.name}. Arrived at {arrival.name}.")
        self.show_message(f"Jumped to {target_system.name}")

    def do_trade(self, resource, amount, is_buying):
        if not self.current_location.is_station():
            self.show_message("No market here.")
            return
        market = self.current_location.market
        if resource not in market:
            self.show_message(f"{resource} not available here.")
            return
        prices = market[resource]
        if is_buying:
            total_cost = prices["buy"] * amount
            if self.credits < total_cost:
                self.show_message(f"Need {total_cost} credits.")
                return
            if not self.has_cargo_space(amount):
                self.show_message("Cargo full!")
                return
            self.credits -= total_cost
            self.receive({resource: amount})
            self.log_event(f"Bought {amount} {resource} for {total_cost} credits")
            self.show_message(f"Bought {amount} {resource}")
        else:
            if self.cargo.get(resource, 0) < amount:
                self.show_message(f"Not enough {resource}.")
                return
            total_value = prices["sell"] * amount
            self.cargo[resource] -= amount
            self.credits += total_value
            self.log_event(f"Sold {amount} {resource} for {total_value} credits")
            self.show_message(f"Sold {amount} {resource}")
