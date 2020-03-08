# Counter-Strike Global Offensive Price Tracker (Chart Generator)
from datetime import datetime

from lib import mail
from lib.database import Database
# noinspection PyUnresolvedReferences
from matplotlib import pyplot as plt
import os

from datetime import datetime
from lib.mail import Mail

mail = Mail(f'Counter-Strike Global Offensive - Item Prices (at {datetime.now().strftime("%d.%m.%Y %H:%M")})')

db = Database()
weapons = db.get_weapons()

charts = []
weapon_prices = []

body = "You'r Items are currently worth:<br><br>"
for wp in weapons:
    body += f'<br><img src="cid:chart_{wp.idx}">'
mail.add_text(body)

for weapon in weapons:
    prices = db.get_resolved_prices(weapon.weapon_name)

    steamX = []
    skinbaronX = []
    steamY = []
    skinbaronY = []

    for price in prices:
        date = datetime.fromtimestamp(price.date)

        if price.market == 'STEAM':
            steamX.append(date)
            steamY.append(price.lowest_price)
        if price.market == 'SKINBARON':
            skinbaronX.append(date)
            skinbaronY.append(price.lowest_price)

    plt.style.use('seaborn')
    plt.title(weapon.weapon_name)
    plt.plot(steamX, steamY)
    plt.plot(skinbaronX, skinbaronY)
    plt.legend(["STEAM", "SKINBARON"])
    plt.gcf().autofmt_xdate()
    plt.grid(True)
    plt.ylabel('Price in €')
    plt.savefig('chart.png')
    plt.clf()

    mail.add_image('chart.png', f'chart_{weapon.idx}')

mail.send()
