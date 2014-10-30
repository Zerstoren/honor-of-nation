import config

import helpers.math

from . import Data

import copy


def getBuildPrice(buildKey, level, drop=1):
    price = Data.builds[buildKey]['price']

    percent = int(config.get('rate.build_up'))

    for i in range(1, level):
        price['wood'] += helpers.math.percent(price['wood'], percent)
        price['rubins'] += helpers.math.percent(price['rubins'], percent)
        price['stone'] += helpers.math.percent(price['stone'], percent)
        price['steel'] += helpers.math.percent(price['steel'], percent)
        price['time'] += helpers.math.percent(price['time'], percent)

    return {
        'wood': int(helpers.math.rate(price['wood']) * drop),
        'rubins': int(helpers.math.rate(price['rubins']) * drop),
        'stone': int(helpers.math.rate(price['stone']) * drop),
        'steel': int(helpers.math.rate(price['steel']) * drop),
        'time': int(helpers.math.rate(price['time']) * drop),
        'eat': 0
    }
