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
        rubinsShift: new LibCanvas.Point(36, 24),
        steelShift:  new LibCanvas.Point(0, 0),
        eatShift:    new LibCanvas.Point(0, 0),
        stoneShift:  new LibCanvas.Point(0, 0),
        woodShift:   new LibCanvas.Point(0, 0),

        getDetail: function (x, y) {
            var posId = mapInstance.help.fromPlaceToId(x, y);
            return factoryMapResources.searchInPool('pos_id', posId)[0];
        },

        getResourceObject: function(x, y) {
            var self = this,
                domain,
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
                    var resourceImage, resourceShift,
                        type = domain.get('type');

                    resourceImage = imageLoader.get('resource-' + type);
                    resourceShift = self[type + 'Shift'];

                    ctx.drawImage({
                        image: resourceImage,
                        from: [point.x + resourceShift.x, point.y + resourceShift.y]
                    });
                };
            }
        }
    });
});
