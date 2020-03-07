# Counter-Strike Global Offensive Price Tracker (Chart Generator)
from datetime import datetime

from database import Database
from matplotlib import pyplot as plt
import os
import mail

WEAPON_NAME = os.getenv('WEAPON_NAME', 'AWP | The Prince (Field-Tested)')
WEAPON_NAME = WEAPON_NAME.replace("_", " ")
WEAPON_NAME = WEAPON_NAME.replace("#", "|")

db = Database()
prices = db.get_resolved_prices(WEAPON_NAME)

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

plt.title(WEAPON_NAME)
plt.plot(steamX, steamY)
plt.plot(skinbaronX, skinbaronY)
plt.legend(['STEAM', 'SKINBARON'])
plt.ylabel('Price in €')
plt.savefig('chart.png')

mail.send_mail()