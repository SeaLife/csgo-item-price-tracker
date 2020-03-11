import requests
import json

from lib.dto import ResolvedPrice


class Resolver:
    @staticmethod
    def resolve_price(weapon):
        pass


class SteamResolver(Resolver):
    @staticmethod
    def resolve_price(weapon):
        data = requests.get(
            f'https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name={weapon.weapon_name}'
        )

        if data.status_code == 200:
            market_info = json.loads(data.content)
            price = 0

            if 'lowest_price' in market_info:
                price = float(market_info["lowest_price"][:-1].replace(" ", "").replace(",", ".").replace("-", "0"))
            elif 'median_price' in market_info:
                price = float(market_info["median_price"][:-1].replace(" ", "").replace(",", ".").replace("-", "0"))

            try:
                volume = int(market_info["volume"])
            except KeyError:
                volume = 0

            if price > 0:
                result = ResolvedPrice()
                result.highest_price = price
                result.lowest_price = price
                result.volume = volume
                result.weapon_name = weapon.weapon_name

                return result

        return None


class SkinBaronResolver(Resolver):
    @staticmethod
    def resolve_price(weapon):
        data = requests.get(
            f'https://skinbaron.de/api/v2/Browsing/FilterOffers' +
            f'?appId=730&variantId={weapon.variant_id}&sort=BP&wlb={weapon.wear_from}&wub={weapon.wear_to}'
        )

        if data.status_code < 300:
            market_info = json.loads(data.content)

            highest_price = 0
            lowest_price = 0

            for item in market_info["aggregatedMetaOffers"]:
                single_offer = item["singleOffer"]

                if (weapon.stat_track is True and 'statTrakString' in single_offer) or (
                        weapon.stat_track is False and 'statTrakString' not in single_offer):
                    if lowest_price == 0:
                        lowest_price = single_offer["itemPrice"]
                    if lowest_price > single_offer["itemPrice"]:
                        lowest_price = single_offer["itemPrice"]
                    if highest_price < single_offer["itemPrice"]:
                        highest_price = single_offer["itemPrice"]

            if lowest_price > 0:
                result = ResolvedPrice()
                result.lowest_price = lowest_price
                result.highest_price = highest_price
                result.volume = len(market_info["aggregatedMetaOffers"])
                result.weapon_name = weapon.weapon_name
                return result

        return None
