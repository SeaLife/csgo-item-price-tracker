# Counter-Strike Global Offensive Price Tracker

from lib.database import Database, PriceHistory
from lib.price_resolver import SteamResolver, SkinBaronResolver

db = Database()

weapons = db.get_weapons()

for weapon in weapons:
    print(f'>> {weapon.weapon_name} ({weapon.wear_from}% -> {weapon.wear_to}%)')

    steam_price = SteamResolver.resolve_price(weapon)
    db.save_resolved_price(PriceHistory('STEAM', steam_price))
    sb_price = SkinBaronResolver.resolve_price(weapon)
    db.save_resolved_price(PriceHistory('SKINBARON', sb_price))

    print(f'STEAM      {steam_price.lowest_price}€ (lowest) - {steam_price.volume} in Market.')
    print(f'SKIN BARON {sb_price.lowest_price}€ (lowest) - {sb_price.volume} in Market.')
    print(f'SKIN BARON {sb_price.highest_price}€ (highest) - {sb_price.volume} in Market.')
    print("")
