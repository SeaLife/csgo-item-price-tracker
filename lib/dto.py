import time
import logging


class ResolvedPrice:
    weapon_name = ""
    lowest_price = 0.0
    highest_price = 0.0
    volume = 0


class PriceHistory:
    weapon_name = ""
    lowest_price = 0.0
    highest_price = 0.0
    market = ""
    date = 0

    def __init__(self, market: str = None, resolved_price: ResolvedPrice = None, synced_time: float = time.time()):
        if resolved_price is not None:
            self.weapon_name = resolved_price.weapon_name
            self.lowest_price = resolved_price.lowest_price
            self.highest_price = resolved_price.highest_price
        if market is not None:
            self.market = market

        self.date = int(synced_time)

    def __str__(self):
        return f'PriceHistory(name={self.weapon_name},lowest={self.lowest_price},highest={self.highest_price},market={self.market},from={self.date})'

    def to_resolved_price(self) -> ResolvedPrice:
        result = ResolvedPrice()
        result.weapon_name = self.weapon_name
        result.highest_price = self.highest_price
        result.lowest_price = self.lowest_price

        return result


class Weapon:
    idx = 0
    weapon_name = ""
    variant_id = 0
    wear_from = 0
    wear_to = 0
    stat_track = False

    def __init__(self, idx=None, name="", variant_id=0, wear_from=0, wear_to=100, stat_track=False):
        self.idx = idx
        self.weapon_name = name
        self.variant_id = variant_id
        self.wear_from = wear_from
        self.wear_to = wear_to
        self.stat_track = stat_track
