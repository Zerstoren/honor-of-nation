from . import Common

import helpers.const
const = helpers.const.Const(
    SWORD=Common.TYPE_SWORD,
    BLUNT=Common.TYPE_BLUNT,
    SPEAR=Common.TYPE_SPEAR,
    BOW=Common.TYPE_BOW,

    SWORD_DAMAGE_MIN=10,
    SWORD_DAMAGE_BASE=40,
    SWORD_SPEED_MIN=20,
    SWORD_SPEED_BASE=20,  # Кол-во ударов в 300 секунд
    SWORD_CRITICAL_CHANCE_MIN=1,
    SWORD_CRITICAL_CHANCE_BASE=1,
    SWORD_CRITICAL_CHANCE_MAX=20,
    SWORD_CRITICAL_DAMAGE_MIN=1.4,
    SWORD_CRITICAL_DAMAGE_BASE=1.4,
    SWORD_CRITICAL_DAMAGE_MAX=3.0,

    BLUNT_DAMAGE_MIN=30,
    BLUNT_DAMAGE_BASE=60,
    BLUNT_SPEED_MIN=15,
    BLUNT_SPEED_BASE=15,
    BLUNT_CRITICAL_CHANCE_MIN=1,
    BLUNT_CRITICAL_CHANCE_BASE=1,
    BLUNT_CRITICAL_CHANCE_MAX=15,
    BLUNT_CRITICAL_DAMAGE_MIN=1.7,
    BLUNT_CRITICAL_DAMAGE_BASE=1.7,
    BLUNT_CRITICAL_DAMAGE_MAX=3.8,

    SPEAR_DAMAGE_MIN=20,
    SPEAR_DAMAGE_BASE=45,
    SPEAR_SPEED_MIN=12,
    SPEAR_SPEED_BASE=12,
    SPEAR_CRITICAL_CHANCE_MIN=2,
    SPEAR_CRITICAL_CHANCE_BASE=2,
    SPEAR_CRITICAL_CHANCE_MAX=25,
    SPEAR_CRITICAL_DAMAGE_MIN=1.2,
    SPEAR_CRITICAL_DAMAGE_BASE=1.2,
    SPEAR_CRITICAL_DAMAGE_MAX=2.8,

    BOW_DAMAGE_MIN=85,
    BOW_DAMAGE_BASE=85,
    BOW_SPEED_MIN=3,
    BOW_SPEED_BASE=3,
    BOW_CRITICAL_CHANCE_MIN=1,
    BOW_CRITICAL_CHANCE_BASE=1,
    BOW_CRITICAL_CHANCE_MAX=10,
    BOW_CRITICAL_DAMAGE_MIN=1.5,
    BOW_CRITICAL_DAMAGE_BASE=1.5,
    BOW_CRITICAL_DAMAGE_MAX=4.0,
)

weapon = {
    'damage': {
        const.SWORD: {
            'rubins': 340,
            'eat': 80,
            'steel': 200,
            'wood': 10,
            'time': 0.1,
            'level': 0.019,
            'base': const.SWORD_DAMAGE_BASE,
            'min': const.SWORD_DAMAGE_MIN
        },

        const.BLUNT: {
            'rubins': 200,
            'eat': 50,
            'steel': 120,
            'wood': 4,
            'time': 0.07,
            'level': 0.014,
            'base': const.BLUNT_DAMAGE_BASE,
            'min': const.BLUNT_DAMAGE_MIN
        },

        const.SPEAR: {
            'rubins': 350,
            'eat': 85,
            'steel': 210,
            'wood': 13,
            'time': 0.11,
            'level': 0.021,
            'base': const.SPEAR_DAMAGE_BASE,
            'min': const.SPEAR_DAMAGE_MIN
        },

        const.BOW: {
            'rubins': 110,
            'eat': 30,
            'steel': 90,
            'wood': 35,
            'time': 0.03,
            'level': 0.009,
            'base': const.BOW_DAMAGE_BASE,
            'min': const.BOW_DAMAGE_MIN
        }
    },

    'speed': {
        const.SWORD: {
            'rubins': 4300,
            'eat': 800,
            'steel': 1500,
            'wood': 300,
            'time': 1,
            'level': 0.3,
            'base': const.SWORD_SPEED_BASE,
            'min': const.SWORD_SPEED_MIN
        },

        const.BLUNT: {
            'rubins': 4500,
            'eat': 1000,
            'steel': 1800,
            'wood': 400,
            'time': 1.2,
            'level': 0.3,
            'base': const.BLUNT_SPEED_BASE,
            'min': const.BLUNT_SPEED_MIN
        },

        const.SPEAR: {
            'rubins': 4900,
            'eat': 950,
            'steel': 1700,
            'wood': 450,
            'time': 1.1,
            'level': 0.4,
            'base': const.SPEAR_SPEED_BASE,
            'min': const.SPEAR_SPEED_MIN
        },

        const.BOW: {
            'rubins': 9000,
            'eat': 1800,
            'steel': 800,
            'wood': 1900,
            'time': 3,
            'level': 0.9,
            'base': const.BOW_SPEED_BASE,
            'min': const.BOW_SPEED_MIN
        }
    },

    'critical_chance': {
        const.SWORD: {
            'rubins': 6000,
            'eat': 1000,
            'steel': 2000,
            'wood': 600,
            'time': 2,
            'level': 0.5,
            'base': const.SWORD_CRITICAL_CHANCE_BASE,
            'min': const.SWORD_CRITICAL_CHANCE_MIN,
            'max': const.SWORD_CRITICAL_CHANCE_MAX

        },

        const.BLUNT: {
            'rubins': 9000,
            'eat': 1800,
            'steel': 2900,
            'wood': 800,
            'time': 2.6,
            'level': 0.7,
            'base': const.BLUNT_CRITICAL_CHANCE_BASE,
            'min': const.BLUNT_CRITICAL_CHANCE_MIN,
            'max': const.BLUNT_CRITICAL_CHANCE_MAX
        },

        const.SPEAR: {
            'rubins': 4500,
            'eat': 800,
            'steel': 1600,
            'wood': 450,
            'time': 1.8,
            'level': 0.4,
            'base': const.SPEAR_CRITICAL_CHANCE_BASE,
            'min': const.SPEAR_CRITICAL_CHANCE_MIN,
            'max': const.SPEAR_CRITICAL_CHANCE_MAX
        },

        const.BOW: {
            'rubins': 12000,
            'eat': 1600,
            'steel': 800,
            'wood': 3500,
            'time': 4,
            'level': 0.7,
            'base': const.BOW_CRITICAL_CHANCE_BASE,
            'min': const.BOW_CRITICAL_CHANCE_MIN,
            'nax': const.BOW_CRITICAL_CHANCE_MAX
        }
    },

    'critical_damage': {
        const.SWORD: {
            'rubins': 200000,
            'eat': 50000,
            'steel': 100000,
            'wood': 10000,
            'time': 80,
            'level': 10,
            'base': const.SWORD_CRITICAL_DAMAGE_BASE,
            'min': const.SWORD_CRITICAL_DAMAGE_MIN,
            'max': const.SWORD_CRITICAL_DAMAGE_MAX
        },

        const.BLUNT: {
            'rubins': 180000,
            'eat': 46000,
            'steel': 94000,
            'wood': 9600,
            'time': 72,
            'level': 9.2,
            'base': const.BLUNT_CRITICAL_DAMAGE_BASE,
            'min': const.BLUNT_CRITICAL_DAMAGE_MIN,
            'max': const.BLUNT_CRITICAL_DAMAGE_MAX
        },

        const.SPEAR: {
            'rubins': 230000,
            'eat': 53000,
            'steel': 110000,
            'wood': 11000,
            'time': 95,
            'level': 11,
            'base': const.SPEAR_CRITICAL_DAMAGE_BASE,
            'min': const.SPEAR_CRITICAL_DAMAGE_MIN,
            'max': const.SPEAR_CRITICAL_DAMAGE_MAX
        },

        const.BOW: {
            'rubins': 170000,
            'eat': 45000,
            'steel': 10000,
            'wood': 90000,
            'time': 70,
            'level': 9,
            'base': const.BOW_CRITICAL_DAMAGE_BASE,
            'min': const.BOW_CRITICAL_DAMAGE_MIN,
            'max': const.BOW_CRITICAL_DAMAGE_MAX
        }
    },
}
