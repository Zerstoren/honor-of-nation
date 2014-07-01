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

        fromPlaceToChank: function(x, y) {
            var chank = config.getChankSize(),
                size = config.getMapSize();

            return parseInt(((y - y % chank) / chank * (size / chank)) + (x - x % chank) / chank + 1, 0x0);
        }
    });
});
