define('service/standalone/map/gameMapItems/Help', [
    'system/config'
], function (config) {
    return AbstractService.extend({
        fromPlaceToId: function(x, y) {
            return (y * config.getMapSize()) + x;
        },

        fromIdToPlace: function(id) {
            var x = id % config.getMapSize(),
                y = (id - x) / config.getMapSize();

            return {
                x: x,
                y: y
            };
        },

        fromPlaceToChank: function(x, y) {

            var chank = config.getChunkSize(),
                size = config.getMapSize();

            return parseInt(((y - y % chank) / chank * (size / chank)) + (x - x % chank) / chank + 1, 0x0);
        }
    });
});