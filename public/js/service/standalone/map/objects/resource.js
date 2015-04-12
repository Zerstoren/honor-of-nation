define('service/standalone/map/objects/resource', [
    'system/template',
    'factory/mapResources',
    'model/mapResources',
    'service/standalone/map',
    'system/imageLoader'
], function(
    template,
    factoryMapResources,
    ModelMapResources,
    mapInstance,
    imageLoader
) {
    "use strict";

    return AbstractService.extend({
        getDetail: function (x, y) {
            var posId = mapInstance.help.fromPlaceToId(x, y);
            return factoryMapResources.searchInPool('pos_id', posId)[0];
        },

        getResourceObject: function(x, y) {
            var domain,
                posId = mapInstance.help.fromPlaceToId(x, y);

            domain = factoryMapResources.searchInPool('pos_id', posId)[0];

            if(domain === undefined) {
                domain = new ModelMapResources();
                domain.set('pos_id', posId);
                domain.mapLoad(function () {
                    try {
                        factoryMapResources.pushToPool(domain);
                    } catch (e) {}
                    mapInstance.draw();
                }.bind(this));

                return false;
            } else {
                return function (point, ctx) {
                    var resourceImage,
                        type = domain.get('type');

                    resourceImage = imageLoader.get('resource-' + type);

                    ctx.drawImage({
                        image: resourceImage,
                        from: [point.x + 6, point.y + 24]
                    });
                };
            }
        }
    });
});
