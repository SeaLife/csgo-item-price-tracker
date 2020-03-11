# Counter-Strike Global Offensive Price Tracker
import logging
from lib.database import Database, PriceHistory
from lib.price_resolver import SteamResolver, SkinBaronResolver

log = logging.getLogger('process')

db = Database()

weapons = db.get_weapons()

for weapon in weapons:
    log.info("Processing %s with a wear-rate of %s -> %s", weapon.weapon_name, weapon.wear_from, weapon.wear_to)

    steam_price = SteamResolver.resolve_price(weapon)
    if steam_price is not None:
        db.save_resolved_price(PriceHistory('STEAM', steam_price))
        log.error("Steam reported a Price of %s€ and a volume of %s for the %s", steam_price.lowest_price,
                  steam_price.volume, weapon.weapon_name)

    sb_price = SkinBaronResolver.resolve_price(weapon)
    if sb_price is not None:
        db.save_resolved_price(PriceHistory('SKINBARON', sb_price))
        log.error("SkinBaron reported a Price of %s€ and a volume of %s for the %s", sb_price.lowest_price,
                  sb_price.volume, weapon.weapon_name)
