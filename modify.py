from typing import Any

from lib.database import Database
from lib.dto import Weapon


def read_input(text: str, default: Any = None, data_type: Any = lambda x: str(x)):
    try:
        data = input(text)
        if data == "" and default is None:
            raise ValueError("Input is empty. Retrying.")
        if data == "" and default is not None:
            return data_type(default)
        return data_type(data)
    except ValueError:
        return read_input(text, default, data_type)


def create():
    db = Database()

    weapon = Weapon()
    weapon.weapon_name = read_input(text="Weapon Name (str): ")
    weapon.variant_id = read_input(text="Variant ID (int): ", data_type=lambda x: int(x))
    weapon.wear_from = read_input(text="Wear from (int) [0]: ", default=0, data_type=lambda x: int(x))
    weapon.wear_to = read_input(text="Wear to (int) [100]: ", default=100, data_type=lambda x: int(x))
    weapon.stat_track = read_input(text="Stat-Track (int) [0]: ", default=100, data_type=lambda x: bool(x))

    db.save_weapon(weapon)


def list_items():
    db = Database()
    wps = db.get_weapons()

    for wp in wps:
        print(f"#{wp.idx} {wp.weapon_name} ({wp.wear_from}% -> {wp.wear_to}%) Stat-Track: {wp.stat_track}")


def remove_item(item_id: int):
    db = Database()
    db.delete_weapon(item_id)
    list_items()
