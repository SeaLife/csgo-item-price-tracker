import requests
import json


class Resolver:
    @staticmethod
    def resolve_price(weapon):
        pass


class ResolvedPrice:
    weapon_name = ""
    lowest_price = 0.0
    highest_price = 0.0
    volume = 0


class SteamResolver(Resolver):
    @staticmethod
    def resolve_price(weapon):
        data = requests.get(
            f'https://steamcommunity.com/market/priceoverview/?appid=730&currency=3&market_hash_name={weapon.weapon_name}'
        )

        if data.status_code == 200:
            market_info = json.loads(data.content)

            price = float(market_info["lowest_price"][:-1].replace(" ", "").replace(",", "."))
            volume = int(market_info["volume"])

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

            result = ResolvedPrice()
            result.lowest_price = lowest_price
            result.highest_price = highest_price
            result.volume = len(market_info["aggregatedMetaOffers"])
            result.weapon_name = weapon.weapon_name
            return result
