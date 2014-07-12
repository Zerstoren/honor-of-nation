define('view/elements/map/help', [
    'system/config'
], function (
    config
) {
    return Backbone.View.extend({
        initialize: function(service) {
            this.service = service;
        },

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

        fromPlaceToChunk: function(x, y) {
            var chunk = config.getChunkSize(),
                size = config.getMapSize();

            return parseInt(((y - y % chunk) / chunk * (size / chunk)) + (x - x % chunk) / chunk + 1, 0x0);
        }
    });
});
