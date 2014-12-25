import helpers.const

const = helpers.const.Const(
    UNIT_TROOP_SIZE=0,
    UNIT_HEALTH=50,
    UNIT_STRENGTH=40,
    UNIT_AGILITY=0,
    UNIT_ABSORPTION=0,
    UNIT_STAMINA=10
)

unit = {
    'troop_size': {
        'rubins': 15,
        'eat': 5,
        'steel': 2,
        'wood': 2,
        'time': 0.1,
        'min': const.UNIT_TROOP_SIZE,
        'base': const.UNIT_TROOP_SIZE
    },

    'health': {
        'rubins': 100,
        'eat': 22,
        'steel': 5,
        'wood': 10,
        'time': 0.2,
        'min': const.UNIT_HEALTH,
        'base': const.UNIT_HEALTH
    },

    'strength': {
        'rubins': 2400,
        'eat': 550,
        'steel': 250,
        'wood': 250,
        'time': 2.5,
        'min': const.UNIT_STRENGTH,
        'base': const.UNIT_STRENGTH

    },

    'agility': {
        'rubins': 5300,
        'eat': 1100,
        'steel': 500,
        'wood': 500,
        'time': 5,
        'min': const.UNIT_AGILITY,
        'base': const.UNIT_AGILITY

    },

    'absorption': {
        'rubins': 5300,
        'eat': 1100,
        'steel': 500,
        'wood': 500,
        'time': 5,
        'min': const.UNIT_ABSORPTION,
        'base': const.UNIT_ABSORPTION
    },

    'stamina': {
        'rubins': 50,
        'eat': 10,
        'steel': 5,
        'wood': 4,
        'time': 0.01,
        'min': const.UNIT_STAMINA,
        'base': const.UNIT_STAMINA

    },

    # 'cavalery_level': {
    #     'rubins': 12000,
    #     'eat': 5000,
    #     'steel': 2000,
    #     'wood': 2000,
    #     'time': 1.8,
    #     'level': 0,
    #     'base': 0,
    #     'min': 0
    # },

    'armor': {
        'rubins': 1000,
        'eat': 300,
        'steel': 100,
        'wood': 100,
        'time': 0.5,
        'base': 0,
        'min': 0
    },

    'weapon': {
        'rubins': 1000,
        'eat': 300,
        'steel': 100,
        'wood': 100,
        'time': 0.5,
        'base': 0,
        'min': 0
    },

    'weapon_second': {
        'rubins': 2000,
        'eat': 600,
        'steel': 200,
        'wood': 200,
        'time': 1,
        'base': 0,
        'min': 0
    }
}
