import helpers.const


const = helpers.const.Const(
    LEATHER_HEALTH_MIN=0,
    LEATHER_HEALTH_BASE=30,
    LEATHER_AGILITY_MIN=0,
    LEATHER_AGILITY_BASE=10,
    LEATHER_ABSORPTION_MIN=-10,
    LEATHER_ABSORPTION_BASE=-10,

    MAIL_HEALTH_MIN=0,
    MAIL_HEALTH_BASE=200,
    MAIL_AGILITY_MIN=-10,
    MAIL_AGILITY_BASE=0,
    MAIL_ABSORPTION_MIN=-10,
    MAIL_ABSORPTION_BASE=0,

    PLATE_HEALTH_MIN=0,
    PLATE_HEALTH_BASE=450,
    PLATE_AGILITY_MIN=-10,
    PLATE_AGILITY_BASE=-10,
    PLATE_ABSORPTION_MIN=0,
    PLATE_ABSORPTION_BASE=10,

    WOOD_SHIELD_BLOCKING_BASE=20,
    WOOD_SHIELD_BLOCKING_MIN=20,
    WOOD_SHIELD_BLOCKING_MAX=70,
    WOOD_SHIELD_DURABILITY_BASE=150,
    WOOD_SHIELD_DURABILITY_MIN=100,

    STEEL_SHIELD_BLOCKING_BASE=50,
    STEEL_SHIELD_BLOCKING_MIN=50,
    STEEL_SHIELD_BLOCKING_MAX=95,
    STEEL_SHIELD_DURABILITY_BASE=500,
    STEEL_SHIELD_DURABILITY_MIN=300,

    HORSE_HEALTH_BASE=400,
    HORSE_HEALTH_MIN=400,
    HORSE_SLOPE_BASE=10,
    HORSE_SLOPE_MIN=10,
    HORSE_SLOPE_MAX=50,

    ARMOR_LEATHER='leather',
    ARMOR_MAIL='mail',
    ARMOR_PLATE='plate',

    SHIELD_WOOD='wood',
    SHIELD_STEEL='steel',
)

armor = {
    'health': {
        const.ARMOR_LEATHER: {
            'rubins': 90,
            'eat': 20,
            'steel': 1,
            'wood': 10,
            'time': 0.15,
            'level': 0.00425,
            'base': const.LEATHER_HEALTH_BASE,
            'min': const.LEATHER_HEALTH_MIN
        },

        const.ARMOR_MAIL: {
            'rubins': 21,
            'eat': 5.5,
            'steel': 8,
            'wood': 2,
            'time': 0.036,
            'level': 0.00102,
            'base': const.MAIL_HEALTH_BASE,
            'min': const.MAIL_HEALTH_MIN
        },

        const.ARMOR_PLATE: {
            'rubins': 0.6,
            'eat': 0.17,
            'steel': 0.24,
            'wood': 0.06,
            'time': 0.001,
            'level': 0.000028,
            'base': const.PLATE_HEALTH_BASE,
            'min': const.PLATE_HEALTH_MIN
        }
    },

    'agility': {
        const.ARMOR_LEATHER: {
            'rubins': 825,
            'eat': 150,
            'steel': 0,
            'wood': 150,
            'time': 1,
            'level': 0.04,
            'base': const.LEATHER_AGILITY_BASE,
            'min': const.LEATHER_AGILITY_MIN
        },

        const.ARMOR_MAIL: {
            'rubins': 2500,
            'eat': 500,
            'steel': 0,
            'wood': 250,
            'time': 3,
            'level': 0.125,
            'base': const.MAIL_AGILITY_BASE,
            'min': const.MAIL_AGILITY_MIN
        },

        const.ARMOR_PLATE: {
            'rubins': 5000,
            'eat': 1000,
            'steel': 100,
            'wood': 2000,
            'time': 5,
            'level': 0.25,
            'base': const.PLATE_AGILITY_BASE,
            'min': const.PLATE_AGILITY_MIN
        }
    },

    'absorption': {
        const.ARMOR_LEATHER: {
            'rubins': 5000,
            'eat': 1000,
            'steel': 2000,
            'wood': 100,
            'time': 5,
            'level': 0.25,
            'base': const.LEATHER_ABSORPTION_BASE,
            'min': const.LEATHER_ABSORPTION_MIN
        },

        const.ARMOR_MAIL: {
            'rubins': 2500,
            'eat': 500,
            'steel': 250,
            'wood': 0,
            'time': 3,
            'level': 0.125,
            'base': const.MAIL_ABSORPTION_BASE,
            'min': const.MAIL_ABSORPTION_MIN
        },

        const.ARMOR_PLATE: {
            'rubins': 825,
            'eat': 150,
            'steel': 200,
            'wood': 0,
            'time': 1,
            'level': 0.04,
            'base': const.PLATE_ABSORPTION_BASE,
            'min': const.PLATE_ABSORPTION_MIN
        }
    },

    'shield_durability': {
        const.SHIELD_WOOD: {
            'rubins': 25,
            'eat': 7.5,
            'steel': 0.5,
            'wood': 15,
            'time': 0.05,
            'level': 0.0021,
            'base': const.WOOD_SHIELD_DURABILITY_BASE,
            'min': const.WOOD_SHIELD_DURABILITY_MIN
        },

        const.SHIELD_STEEL: {
            'rubins': 1,
            'eat': 0.35,
            'steel': 0.25,
            'wood': 0,
            'time': 0.002,
            'level': 0.00008,
            'base': const.STEEL_SHIELD_DURABILITY_BASE,
            'min': const.STEEL_SHIELD_DURABILITY_MIN
        }
    },

    'shield_blocking': {
        const.SHIELD_WOOD: {
            'rubins': 1000,
            'eat': 150,
            'steel': 80,
            'wood': 380,
            'time': 0.5,
            'level': 0.02,
            'base': const.WOOD_SHIELD_BLOCKING_BASE,
            'min': const.WOOD_SHIELD_BLOCKING_MIN,
            'max': const.WOOD_SHIELD_BLOCKING_MAX
        },

        const.SHIELD_STEEL: {
            'rubins': 1500,
            'eat': 200,
            'steel': 400,
            'wood': 50,
            'time': 1,
            'level': 0.05,
            'base': const.STEEL_SHIELD_BLOCKING_BASE,
            'min': const.STEEL_SHIELD_BLOCKING_MIN,
            'max': const.STEEL_SHIELD_BLOCKING_MAX
        }
    },

    'horse_health': {
        'rubins': 25,
        'eat': 20,
        'steel': 2.5,
        'wood': 10,
        'time': 0.017,
        'level': 0,
        'min': const.HORSE_HEALTH_MIN,
        'base': const.HORSE_HEALTH_BASE
    },

    'horse_slope': {
        'rubins': 4500,
        'eat': 600,
        'steel': 1200,
        'wood': 150,
        'time': 3,
        'level': 0,
        'min': const.HORSE_SLOPE_MIN,
        'max': const.HORSE_SLOPE_MAX,
        'base': const.HORSE_SLOPE_BASE
    }
}