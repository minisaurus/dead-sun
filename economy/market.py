from data.items import RESOURCES
from data.locations import STATION_TYPES
import random


class Market:
    def __init__(self, station_type="trading_post"):
        self.station_type = station_type
        self.inventory = {}
        self.prices = {}
        self._generate_inventory()

    def _generate_inventory(self):
        station_info = STATION_TYPES.get(self.station_type, {})
        price_mod = station_info.get("price_modifier", 1.0)
        available = station_info.get("available_items", [])
        for item_key in available:
            if item_key in RESOURCES:
                base_price = RESOURCES[item_key]["base_price"]
                self.prices[item_key] = {
                    "buy": int(base_price * price_mod * 1.2),
                    "sell": int(base_price * price_mod * 0.8),
                }
                self.inventory[item_key] = random.randint(5, 50)

    def buy_price(self, resource):
        return self.prices.get(resource, {}).get("buy", 999)

    def sell_price(self, resource):
        return self.prices.get(resource, {}).get("sell", 0)

    def can_buy(self, resource, amount=1):
        return self.inventory.get(resource, 0) >= amount

    def buy(self, resource, amount=1):
        if not self.can_buy(resource, amount):
            return False
        self.inventory[resource] -= amount
        return self.buy_price(resource) * amount

    def sell(self, resource, amount=1):
        return self.sell_price(resource) * amount

    def get_available_items(self):
        return {k: v for k, v in self.inventory.items() if v > 0}
