import os
import sqlite3
import time
from typing import List

from lib.price_resolver import ResolvedPrice


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


class Database:
    def __init__(self):
        database_name = os.getenv('DATABASE_NAME', 'sv.db')
        self.connection = sqlite3.connect(database_name)
        self.connection.isolation_level = None
        self.connection.row_factory = sqlite3.Row
        print("DB: ", database_name)
        self.create_table()

    def create_table(self):
        self.connection.execute(
            'CREATE TABLE IF NOT EXISTS weapons (weapon_name VARCHAR, variant_id INT, wear_from FLOAT, wear_to FLOAT, stat_track NUMERIC)')
        self.connection.execute(
            'CREATE TABLE IF NOT EXISTS prices (weapon_name VARCHAR, lowest_price FLOAT, highest_price FLOAT, date_from NUMERIC, market VARCHAR)')

    def get_weapons(self) -> List[Weapon]:
        data = self.connection.execute('SELECT rowid, * FROM weapons')
        result = []

        for item in data.fetchall():
            wp = Weapon()
            wp.idx = item["rowid"]
            wp.wear_from = item["wear_from"]
            wp.wear_to = item["wear_to"]
            wp.variant_id = item["variant_id"]
            wp.weapon_name = item["weapon_name"]
            wp.stat_track = bool(item["stat_track"])

            result.append(wp)

        return result

    def save_weapon(self, weapon: Weapon):
        data = self.connection.execute('SELECT rowid, * FROM weapons WHERE weapon_name = ?', (weapon.weapon_name,))
        fetched_data = data.fetchall()

        if len(fetched_data) > 0:
            print(f"[Updating {weapon.weapon_name}]")
            rowid = fetched_data[0]["rowid"]

            self.connection.execute(
                'UPDATE weapons SET weapon_name = ?, variant_id = ?, wear_from = ?, wear_to = ? WHERE rowid = ?',
                (weapon.weapon_name, weapon.variant_id, weapon.wear_from, weapon.wear_to, rowid))
        else:
            print(f"[Creating {weapon.weapon_name}]")
            self.connection.execute(
                'INSERT INTO weapons (weapon_name, variant_id, wear_from, wear_to) VALUES (?, ?, ?, ?)',
                (weapon.weapon_name, weapon.variant_id, weapon.wear_from, weapon.wear_to))

    def get_resolved_prices(self, weapon_name) -> List[PriceHistory]:
        data = self.connection.execute('SELECT rowid, * FROM prices WHERE weapon_name = ? ORDER BY date_from',
                                       (weapon_name,))
        result = []

        for item in data.fetchall():
            rp = PriceHistory()
            rp.date = item["date_from"]
            rp.lowest_price = item["lowest_price"]
            rp.highest_price = item["highest_price"]
            rp.market = item["market"]
            rp.weapon_name = item["weapon_name"]

            result.append(rp)

        return result

    def save_resolved_price(self, price_history: PriceHistory):
        self.connection.execute('INSERT INTO prices VALUES(?, ?, ?, ?, ?)',
                                (price_history.weapon_name, price_history.lowest_price, price_history.highest_price,
                                 price_history.date, price_history.market))
