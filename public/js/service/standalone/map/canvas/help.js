define('service/standalone/map/canvas/help', [
    'system/config',
    'view/block/error'
], function (
    config,
    viewBlockError
) {
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

        fromPlaceToChunk: function(x, y) {

            var chunk = config.getChunkSize(),
                size = config.getMapSize();

            return parseInt(((y - y % chunk) / chunk * (size / chunk)) + (x - x % chunk) / chunk + 1, 0x0);
        },

        validateCoordinate: function (coordinate) {
            var x, y,
                coords = coordinate.split(/([0-9]{1,4})([^0-9]{1,})([0-9]{1,4})/);

            if (coords.length != 5) {
                viewBlockError.showErrorBox('Введен неверный формат координат. Используйте такой вид: 100x100');
                return false;
            }

            x = parseInt(coords[1], 10);
            y = parseInt(coords[3], 10);

            if (isNaN(x) || isNaN(y)) {
                viewBlockError.showErrorBox('Введен неверный формаn координат. Используйте такой вид: 100x100');
                return false;
            }

            return [x, y];
        }
    });
});