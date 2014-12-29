import config

RATE = int(config.get('rate.base_rate'))


def percent(value, percent):
    return int(float(value) / 100 * float(percent))


def rate(value):
    return int(value * RATE / 100)
