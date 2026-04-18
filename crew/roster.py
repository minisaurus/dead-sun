from crew.crew import CrewMember


class CrewRoster:
    def __init__(self):
        self.members = []

    def add(self, member=None):
        if member is None:
            member = CrewMember()
        self.members.append(member)
        return member

    def remove(self, member):
        if member in self.members:
            self.members.remove(member)

    def assigned(self):
        return [m for m in self.members if m.is_assigned()]

    def unassigned(self):
        return [m for m in self.members if not m.is_assigned()]

    def get_assigned_to(self, pos):
        for m in self.members:
            if m.assigned_to == pos:
                return m
        return None

    def total_food_needed(self):
        return len(self.members)

    def tick_all(self):
        for m in self.members:
            m.tick()

    def feed_all(self):
        fed = 0
        for m in self.members:
            if m.hunger > 0:
                m.feed()
                fed += 1
        return fed

    def members_on_ship(self, ship_id):
        return [m for m in self.members if m.ship_id == ship_id]

    def available_for_role(self, role):
        return [m for m in self.members if not m.is_assigned() and m.role == role]

    def best_for_skill(self, skill):
        if not self.members:
            return None
        return max(self.members, key=lambda m: m.skill(skill))

    def total_morale(self):
        if not self.members:
            return 0
        return sum(m.morale for m in self.members) / len(self.members)

    def total_health(self):
        if not self.members:
            return 0
        return sum(m.health for m in self.members) / len(self.members)

    def heal_all(self, amount):
        for m in self.members:
            m.health = min(100, m.health + amount)
