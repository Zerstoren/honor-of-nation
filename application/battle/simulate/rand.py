import random


def chance(chanceInt):
    chanceInt = round(chanceInt * 10)
    randInt = random.randint(0, 1000)
    return chanceInt <= randInt

def randint(start, complete):
    return random.randint(start, complete)