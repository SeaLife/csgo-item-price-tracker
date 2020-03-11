# Counter-Strike Global Offensive Price Tracker (Chart Generator)
import logging
import os
import time
from functools import lru_cache

from typing import Dict, List
from lib.database import Database
from lib.dto import Weapon, ResolvedPrice, PriceHistory
from lib.mail import Mail
from datetime import datetime
from datetime import time as dtime
from matplotlib import pyplot as plt
from datetime import datetime

send_mail = Mail(f'Counter-Strike Global Offensive - Item Prices (at {datetime.now().strftime("%d.%m.%Y %H:%M")})')

db = Database()
log = logging.getLogger('chart')


class PriceInfo:
    skin_baron: List[PriceHistory]
    steam: List[PriceHistory]

    def __init__(self):
        self.steam = []
        self.skin_baron = []

    @lru_cache(maxsize=10)
    def avg_steam(self):
        p = 0
        for s in self.steam:
            p += s.lowest_price
        avg = p / (len(self.steam))
        log.debug("Average price for steam is %s€ (%s prices)", avg, len(self.steam))
        return avg

    @lru_cache(maxsize=10)
    def avg_skin_baron(self):
        p = 0
        for s in self.skin_baron:
            p += s.lowest_price
        avg = p / len(self.skin_baron)
        log.debug("Average price for skin baron is %s€ (%s prices)", avg, len(self.skin_baron))
        return avg


def prices_from_dates(wp: Weapon, date_format='%Y-%m-%d %H:%M:%S', predicate=lambda t: True):
    prices = db.get_resolved_prices(wp.weapon_name)

    daily_prices: Dict[str, PriceInfo] = {}

    for p in prices:
        if predicate(p.date) is True:
            date = time.strftime(date_format, time.localtime(p.date))
            log.debug("Added PriceInfo from %s from market %s with the price of %s to the storage.", date, p.market,
                      p.lowest_price)

            if date not in daily_prices:
                daily_prices[date] = PriceInfo()

            if p.market == 'STEAM':
                daily_prices[date].steam.append(p)
            if p.market == 'SKINBARON':
                daily_prices[date].skin_baron.append(p)

    return daily_prices


def generate_charts_for(wp: Weapon, prices: Dict[str, PriceInfo], file_name='chart.png'):
    x_axis = []
    y_axis_steam = []
    y_axis_skinbaron = []

    date_format = '%Y-%m-%d %H:%M:%S'

    for d, price_info in prices.items():
        x_axis.append(datetime.strptime(d, date_format))
        log.debug("%s got entry for %s", file_name, d)
        if price_info.avg_steam() > 0:
            y_axis_steam.append(price_info.avg_steam())
        if price_info.avg_skin_baron() > 0:
            y_axis_skinbaron.append(price_info.avg_skin_baron())

    plt.clf()
    plt.suptitle(weapon.weapon_name)
    plt.title(f'(variant_id={weapon.variant_id})')
    plt.plot(x_axis, y_axis_steam)
    plt.plot(x_axis, y_axis_skinbaron)
    plt.legend(['STEAM', 'SKINBARON'])
    plt.gcf().autofmt_xdate()
    plt.grid(True)
    plt.ylabel('Preis in €')
    plt.savefig(file_name)
    plt.clf()

    log.info(f"Rendered {file_name} with {len(x_axis)} x values.")


def predicate_today():
    date_format = '%Y-%m-%d %H:%M:%S'
    start_of_day = datetime.strptime(time.strftime('%Y-%m-%d 00:00:00', time.localtime(time.time())), date_format)
    end_of_day = datetime.strptime(time.strftime('%Y-%m-%d 23:59:59', time.localtime(time.time())), date_format)
    return lambda t: start_of_day <= datetime.fromtimestamp(t) <= end_of_day


def predicate_this_month():
    date_format = '%Y-%m-%d %H:%M:%S'
    start_of_day = datetime.strptime(time.strftime('%Y-%m-01 00:00:00', time.localtime(time.time())), date_format)
    end_of_day = datetime.strptime(time.strftime('%Y-%m-28 23:59:59', time.localtime(time.time())), date_format)
    return lambda t: start_of_day <= datetime.fromtimestamp(t) <= end_of_day


def predicate_this_year():
    date_format = '%Y-%m-%d %H:%M:%S'
    start_of_day = datetime.strptime(time.strftime('%Y-01-01 00:00:00', time.localtime(time.time())), date_format)
    end_of_day = datetime.strptime(time.strftime('%Y-12-31 23:59:59', time.localtime(time.time())), date_format)
    return lambda t: start_of_day <= datetime.fromtimestamp(t) <= end_of_day


body = '<h2>Price Summary</h2><br><br>You\'r price summary is:<br><br>'

for weapon in db.get_weapons():
    # daily
    generate_charts_for(
        wp=weapon,
        prices=prices_from_dates(weapon, '%Y-%m-%d 12:00:00'),
        file_name=f'rendered/daily{weapon.idx}.png')
    # monthly
    generate_charts_for(
        wp=weapon,
        prices=prices_from_dates(weapon, '%Y-%m-01 12:00:00'),
        file_name=f'rendered/monthly{weapon.idx}.png')
    # today
    generate_charts_for(
        wp=weapon,
        prices=prices_from_dates(weapon, predicate=predicate_today()),
        file_name=f'rendered/today{weapon.idx}.png')
    # this month
    generate_charts_for(
        wp=weapon,
        prices=prices_from_dates(weapon, predicate=predicate_this_month()),
        file_name=f'rendered/this_month{weapon.idx}.png')
    # this year
    generate_charts_for(
        wp=weapon,
        prices=prices_from_dates(weapon, predicate=predicate_this_year()),
        file_name=f'rendered/this_year{weapon.idx}.png')

    body += f'<h3>{weapon.weapon_name}</h3>'
    body += f'Rate: {weapon.wear_from}% -> {weapon.wear_to}%<br>'
    body += f'Variant ID: {weapon.variant_id}<br><br>'

    body += f'<b>Charts:</b><br>'
    body += f'<img src="cid:today{weapon.idx}"/>'
    body += f'<img src="cid:this_month{weapon.idx}"/>'
    body += f'<img src="cid:this_year{weapon.idx}"/>'
    body += f'<img src="cid:monthly{weapon.idx}"/>'
    body += f'<img src="cid:daily{weapon.idx}"/>'

send_mail.add_text(body);

for wp in db.get_weapons():
    send_mail.add_image(f'rendered/today{wp.idx}.png', f'today{wp.idx}')
    send_mail.add_image(f'rendered/this_month{wp.idx}.png', f'this_month{wp.idx}')
    send_mail.add_image(f'rendered/this_year{wp.idx}.png', f'this_month{wp.idx}')
    send_mail.add_image(f'rendered/daily{wp.idx}.png', f'daily{wp.idx}')
    send_mail.add_image(f'rendered/monthly{wp.idx}.png', f'monthly{wp.idx}')

send_mail.send()
