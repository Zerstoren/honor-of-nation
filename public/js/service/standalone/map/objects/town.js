define('service/standalone/map/objects/town', [
    'system/template',

    'factory/town',
    'model/town',

    'service/standalone/map',
    'system/imageLoader'
], function(
    template,

    factoryTown,
    ModelTown,

    mapInstance,
    imageLoader
) {
    "use strict";

    return AbstractService.extend({
        getDetail: function (x, y) {
            var posId = mapInstance.help.fromPlaceToId(x, y);
            return factoryTown.searchInPool('pos_id', posId)[0];
        },

        getTownObject: function(x, y) {
            var domain,
                posId = mapInstance.help.fromPlaceToId(x, y);

            domain = factoryTown.searchInPool('pos_id', posId)[0];

            if(domain === undefined) {
                domain = new ModelTown();
                domain.set('pos_id', posId);
                domain.mapLoad(function () {
                    try {
                        factoryTown.pushToPool(domain);
                    } catch (e) {}
                    mapInstance.draw();
                }.bind(this));

                return false;
            } else {
                return function (point, ctx) {
                    var townImage,
                        type = domain.get('type');

                    switch(type) {
                        case 0: townImage = imageLoader.get('city-village'); break;
                        case 1: townImage = imageLoader.get('city-town'); break;
                        case 2: townImage = imageLoader.get('city-castle'); break;
                    }

                    ctx.drawImage({
                        image: townImage,
                        from: [point.x + 6, point.y + 12]
                    });
                };
            }
        }
    });
});
