import random

CONTRACT_TYPES = ["delivery", "mining", "escort", "rescue"]


class Contract:
    def __init__(self, contract_type, destination, reward, description, requirements=None):
        self.contract_type = contract_type
        self.destination = destination
        self.reward = reward
        self.description = description
        self.requirements = requirements or {}
        self.completed = False
        self.failed = False

    def check_completion(self, player_cargo, player_location):
        if self.completed or self.failed:
            return False
        if self.contract_type == "delivery":
            if player_location.name == self.destination:
                for res, amt in self.requirements.items():
                    if player_cargo.get(res, 0) < amt:
                        return False
                return True
        return False


class ContractEngine:
    def __init__(self):
        self.active_contracts = []
        self.available_contracts = []

    def generate_contracts(self, locations, current_location):
        self.available_contracts = []
        for _ in range(random.randint(2, 5)):
            dest = random.choice(
                [l for l in locations if l.name != current_location.name and l.explored]
            )
            ctype = random.choice(CONTRACT_TYPES)
            reward_credits = random.randint(20, 100)
            req = {}
            desc = ""
            if ctype == "delivery":
                res = random.choice(["metal", "electronics", "food", "fuel"])
                amt = random.randint(3, 15)
                req = {res: amt}
                desc = f"Deliver {amt} {res} to {dest.name}"
            elif ctype == "mining":
                desc = f"Mine resources near {dest.name}"
            elif ctype == "escort":
                desc = f"Escort a vessel to {dest.name}"
            elif ctype == "rescue":
                desc = f"Rescue survivors near {dest.name}"
            self.available_contracts.append(
                Contract(ctype, dest.name, {"credits": reward_credits}, desc, req)
            )

    def accept_contract(self, contract):
        if contract in self.available_contracts:
            self.available_contracts.remove(contract)
            self.active_contracts.append(contract)

    def check_all(self, player_cargo, player_location):
        completed = []
        for c in self.active_contracts:
            if c.check_completion(player_cargo, player_location):
                c.completed = True
                completed.append(c)
        for c in completed:
            self.active_contracts.remove(c)
        return completed
