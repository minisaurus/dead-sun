"""Dead Sun - Ship grid, modules, and building."""

from data import EMPTY, FLOOR, MODULES, HULL_COST, CARGO_PER_BAY


class Ship:
    def __init__(self, width=16, height=10):
        self.width = width
        self.height = height
        self.grid = [[EMPTY] * width for _ in range(height)]
        self.modules = {}  # (row, col) -> module_type string

    def in_bounds(self, r, c):
        return 0 <= r < self.height and 0 <= c < self.width

    def get_tile(self, r, c):
        if not self.in_bounds(r, c):
            return None
        return self.grid[r][c]

    def is_buildable(self, r, c):
        """Can we place a floor here? Must be EMPTY and adjacent to existing FLOOR/module."""
        if not self.in_bounds(r, c):
            return False
        if self.grid[r][c] != EMPTY:
            return False
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.grid[nr][nc] != EMPTY:
                return True
        return False

    def can_place_module(self, r, c):
        """Can we place a module here? Must be FLOOR with no module."""
        if not self.in_bounds(r, c):
            return False
        if self.grid[r][c] != FLOOR:
            return False
        return (r, c) not in self.modules

    def build_hull(self, r, c):
        """Extend hull to this tile. Returns True if successful."""
        if not self.is_buildable(r, c):
            return False
        self.grid[r][c] = FLOOR
        return True

    def place_module(self, r, c, module_type):
        """Place a module on a floor tile. Returns True if successful."""
        if not self.can_place_module(r, c):
            return False
        if module_type not in MODULES:
            return False
        self.grid[r][c] = FLOOR
        self.modules[(r, c)] = module_type
        return True

    def remove_module(self, r, c):
        """Remove a module, returning half its build cost."""
        if (r, c) not in self.modules:
            return {}
        mtype = self.modules.pop((r, c))
        cost = MODULES[mtype]["cost"]
        refund = {}
        for res, amt in cost.items():
            refund[res] = max(1, amt // 2)
        self.grid[r][c] = FLOOR
        return refund

    def get_module_at(self, r, c):
        return self.modules.get((r, c))

    def get_module_list(self):
        """Return list of (row, col, module_type) for all modules."""
        return [(r, c, mt) for (r, c), mt in self.modules.items()]

    def count_module(self, module_type):
        return sum(1 for mt in self.modules.values() if mt == module_type)

    def get_power_balance(self):
        """Returns (generated, consumed). Negative pwr means generation."""
        gen = 0
        use = 0
        for mt in self.modules.values():
            p = MODULES[mt]["pwr"]
            if p < 0:
                gen += abs(p)
            else:
                use += p
        return gen, use

    def get_oxygen_balance(self):
        """Returns (generated, consumed). Negative o2 means generation."""
        gen = 0
        use = 0
        for mt in self.modules.values():
            o = MODULES[mt]["o2"]
            if o < 0:
                gen += abs(o)
            else:
                use += o
        return gen, use

    def get_max_crew(self):
        return self.count_module("habitat") * 2 + 2

    def get_cargo_capacity(self):
        return 20 + self.count_module("cargo_bay") * CARGO_PER_BAY

    def get_total_cargo(self, cargo):
        return sum(cargo.values())

    def get_connected_modules(self, module_type):
        """Count modules that have a path to other modules (connectivity check)."""
        if not self.modules:
            return set()
        module_positions = set(self.modules.keys())
        visited = set()
        start = next(iter(module_positions))
        queue = [start]
        while queue:
            r, c = queue.pop(0)
            if (r, c) in visited:
                continue
            visited.add((r, c))
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in module_positions and (nr, nc) not in visited:
                    queue.append((nr, nc))
        return visited

    def apply_starter_layout(self):
        """Set up the initial ship layout."""
        # 6x3 block in the center-ish area
        center_r = self.height // 2 - 1
        center_c = self.width // 2 - 3
        for r in range(center_r, center_r + 3):
            for c in range(center_c, center_c + 6):
                self.grid[r][c] = FLOOR
        # Place starter modules
        self.modules[(center_r, center_c)] = "cockpit"
        self.modules[(center_r, center_c + 2)] = "reactor"
        self.modules[(center_r, center_c + 4)] = "engine"
        self.modules[(center_r + 1, center_c)] = "life_support"
        self.modules[(center_r + 1, center_c + 2)] = "farm"
        self.modules[(center_r + 1, center_c + 4)] = "cargo_bay"
        self.modules[(center_r + 2, center_c)] = "habitat"
        self.modules[(center_r + 2, center_c + 1)] = "habitat"
        self.modules[(center_r + 2, center_c + 4)] = "cargo_bay"
