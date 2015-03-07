from . import Common

MOVE = {
    'infantry': {
        'byroad': {
            Common.LAND_VALLEY: 10,
            Common.LAND_STEPPE: 13,
            Common.LAND_SWAMP: 16,
            Common.LAND_FOREST: 13,
            Common.LAND_JUNGLE: 20,
            Common.LAND_MOUNTAINS: 19
        },

        'road': {
            Common.LAND_VALLEY: 5,
            Common.LAND_STEPPE: 5,
            Common.LAND_SWAMP: 12,
            Common.LAND_FOREST: 8,
            Common.LAND_JUNGLE: 12,
            Common.LAND_MOUNTAINS: 14
        }
    }
}