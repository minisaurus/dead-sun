from world.system import SolarSystem
from world.location import Location


class Galaxy:
    def __init__(self):
        self.systems = []
        self._generate()

    def _generate(self):
        home = SolarSystem()
        home.name = "Sol System"
        home.system_id = 0
        self.systems.append(home)

        alpha = SolarSystem()
        alpha.name = "Alpha Centauri"
        alpha.system_id = 1
        alpha.locations = [
            Location("Proxima", "rocky_planet", 1, 3, "A harsh red-drenched world."),
            Location("Centauri Belt", "asteroid_field", 3, 1, "Rich asteroid deposits."),
            Location("New Haven", "station", 4, 5, "A bustling trading hub."),
            Location("Rigel Station", "station", 6, 2, "Shipyard and repair facility."),
        ]
        new_haven = alpha.get_location("New Haven")
        new_haven.station_type = "trading_post"
        new_haven.generate_market()
        rigel = alpha.get_location("Rigel Station")
        rigel.station_type = "shipyard"
        rigel.generate_market()
        self.systems.append(alpha)

        sirius = SolarSystem()
        sirius.name = "Sirius"
        sirius.system_id = 2
        sirius.locations = [
            Location("Sirius Prime", "gas_giant", 0, 4, "Brilliant blue giant."),
            Location("The Shards", "asteroid_field", 3, 2, "Shattered crystalline debris."),
            Location("Deep Ice", "ice_moon", 5, 6, "Frozen wastes at the edge."),
            Location("Outpost Zero", "station", 7, 3, "Rough mining settlement."),
        ]
        outpost_zero = sirius.get_location("Outpost Zero")
        outpost_zero.station_type = "mining_outpost"
        outpost_zero.generate_market()
        self.systems.append(sirius)

    def get_system(self, name):
        for s in self.systems:
            if s.name == name:
                return s
        return None

    def ftl_cost(self, from_system, to_system):
        return 50
