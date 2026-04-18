from world.location import Location
from data.config import FUEL_PER_TRAVEL


class SolarSystem:
    def __init__(self):
        self.name = "Sol System"
        self.system_id = 0
        self.locations = []
        self._generate()

    def _generate(self):
        self.locations = [
            Location("Sol", "star", 0, 4, "The dying sun."),
            Location("Hermes", "rocky_planet", 2, 3, "Scorched world."),
            Location("Aphrodite", "rocky_planet", 3, 6, "Thick atmosphere."),
            Location("The Belt", "asteroid_field", 5, 2, "Dense asteroids."),
            Location("Gaia", "rocky_planet", 5, 5, "Ruins of old colony."),
            Location("Outpost 7", "station", 5, 7, "Trading post."),
            Location("Tartarus", "gas_giant", 7, 1, "Massive gas giant."),
            Location("Europa", "ice_moon", 8, 3, "Frozen moon."),
            Location("Kuiper Drift", "asteroid_field", 9, 0, "Edge of system."),
            Location("The Maw", "asteroid_field", 9, 7, "Dangerous debris."),
        ]
        outpost = self.locations[5]
        outpost.explored = True
        outpost.station_type = "trading_post"
        outpost.generate_market()

    def get_location(self, name):
        for loc in self.locations:
            if loc.name == name:
                return loc
        return None

    def travel_cost(self, from_loc, to_loc):
        dist = from_loc.distance_to(to_loc)
        return max(1, dist * FUEL_PER_TRAVEL)
