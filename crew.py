"""Dead Sun - Crew management."""

import random
from data import FIRST_NAMES, LAST_NAMES, SKILLS


class CrewMember:
    def __init__(self, name=None, role=None):
        if name is None:
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        self.name = name
        self.role = role or random.choice(["commander", "engineer", "miner", "pilot", "scientist", "medic"])
        self.skills = {}
        for s in SKILLS:
            self.skills[s] = random.randint(1, 3)
        self.skills[self.role] = max(self.skills.get(self.role, 1), random.randint(3, 5))
        self.assigned_to = None  # (row, col) of module
        self.morale = 100
        self.health = 100
        self.hunger = 0

    def skill(self, skill_name):
        return self.skills.get(skill_name, 1)

    def assign(self, module_pos):
        self.assigned_to = module_pos

    def unassign(self):
        self.assigned_to = None

    def is_assigned(self):
        return self.assigned_to is not None

    def tick(self):
        """Daily crew update."""
        self.hunger += 1
        if self.hunger > 3:
            self.morale = max(0, self.morale - 5)
            if self.hunger > 7:
                self.health = max(0, self.health - 3)
        if self.morale < 30:
            self.health = max(0, self.health - 1)

    def feed(self):
        """Reset hunger."""
        self.hunger = 0
        self.morale = min(100, self.morale + 2)

    def efficiency(self):
        """Work efficiency 0.0 - 1.0 based on morale and health."""
        return (self.morale / 100) * (self.health / 100)

    def status_text(self):
        if self.health < 30:
            return "critical"
        if self.morale < 30:
            return "unhappy"
        if self.hunger > 3:
            return "hungry"
        if self.health < 70:
            return "injured"
        return "ok"


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
