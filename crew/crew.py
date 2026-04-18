import random
from data.config import FIRST_NAMES, LAST_NAMES, SKILLS

ROLES = ["commander", "engineer", "pilot", "miner", "scientist", "medic", "gunner"]


class CrewMember:
    def __init__(self, name=None, role=None):
        if name is None:
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        self.name = name
        self.role = role or random.choice(ROLES)
        self.skills = {}
        for s in SKILLS:
            self.skills[s] = random.randint(1, 3)
        self.skills[self.role] = max(self.skills.get(self.role, 1), random.randint(3, 5))
        self.assigned_to = None
        self.morale = 100
        self.health = 100
        self.hunger = 0
        self.ship_id = None
        self.xp = {}

    def skill(self, skill_name):
        return self.skills.get(skill_name, 1)

    def assign(self, module_pos):
        self.assigned_to = module_pos

    def unassign(self):
        self.assigned_to = None

    def is_assigned(self):
        return self.assigned_to is not None

    def tick(self):
        self.hunger += 1
        if self.hunger > 3:
            self.morale = max(0, self.morale - 5)
            if self.hunger > 7:
                self.health = max(0, self.health - 3)
        if self.morale < 30:
            self.health = max(0, self.health - 1)

    def feed(self):
        self.hunger = 0
        self.morale = min(100, self.morale + 2)

    def efficiency(self):
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

    def add_xp(self, skill, amount):
        if skill not in self.xp:
            self.xp[skill] = 0
        self.xp[skill] += amount
        current_level = self.skills.get(skill, 1)
        new_level = min(current_level + self.xp[skill] // 10, 10)
        if new_level > current_level:
            self.skills[skill] = new_level
            self.xp[skill] = self.xp[skill] % 10

    def specialty(self):
        return max(self.skills, key=self.skills.get)
