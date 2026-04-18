class Fleet:
    def __init__(self):
        self.ships = []
        self.active_ship_idx = 0

    @property
    def active_ship(self):
        if not self.ships:
            return None
        return self.ships[self.active_ship_idx]

    def add_ship(self, ship):
        self.ships.append(ship)

    def remove_ship(self, ship):
        if ship in self.ships:
            self.ships.remove(ship)

    def switch_ship(self, idx):
        if 0 <= idx < len(self.ships):
            self.active_ship_idx = idx

    def total_cargo_capacity(self):
        return sum(s.get_cargo_capacity() for s in self.ships)

    def total_power_balance(self):
        gen = sum(s.get_power_balance()[0] for s in self.ships)
        use = sum(s.get_power_balance()[1] for s in self.ships)
        return gen, use

    def total_oxygen_balance(self):
        gen = sum(s.get_oxygen_balance()[0] for s in self.ships)
        use = sum(s.get_oxygen_balance()[1] for s in self.ships)
        return gen, use

    def total_max_crew(self):
        return sum(s.get_max_crew() for s in self.ships)

    def all_modules(self):
        result = {}
        for ship in self.ships:
            for pos, mt in ship.modules.items():
                result[(id(ship), pos)] = mt
        return result
