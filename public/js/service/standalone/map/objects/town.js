define('service/standalone/map/objects/town', [
    'service/standalone/map/objects/abstract',
    'system/template',

    'factory/town',
    'model/town',

    'service/standalone/map',
    'system/imageLoader',

    'view/elements/ractive-helper'
], function(
    AbstractObjects,
    template,

    factoryTown,
    ModelTown,

    mapInstance,
    imageLoader,

    viewElementsRactiveHelper
) {
    "use strict";

    return AbstractObjects.extend({
        initialize: function () {
            this.shift = new LibCanvas.Point(6, 12);
        },

        getDetail: function (x, y) {
            var posId = mapInstance.help.fromPlaceToId(x, y);
            return factoryTown.searchInPool('pos_id', posId)[0];
        },

        getTownObject: function(x, y) {
            var domain,
                self = this,
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
                        typeName,
                        type = domain.get('type');

                    switch(type) {
                        case 0:
                            townImage = imageLoader.get('city-village');
                            typeName = 'Село';
                            break;
                        case 1:
                            townImage = imageLoader.get('city-town');
                            typeName = 'Город';
                            break;
                        case 2:
                            townImage = imageLoader.get('city-castle');
                            typeName = 'Замок';
                            break;
                    }

                    ctx.drawImage({
                        image: townImage,
                        from: [point.x + self.shift.x, point.y + self.shift.y]
                    });

                    self.setStyleForBox(ctx);
                    self.drawBox(
                        domain.get('name') + '\n' + typeName + '. Населения ' +
                            viewElementsRactiveHelper.transformNumberToView(domain.get('population')),
                        point,
                        ctx
                    );
                };
            }
        }
    });
});
