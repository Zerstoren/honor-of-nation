define('service/standalone/map/objects/resource', [
    'system/template',
    'factory/mapResources',
    'model/mapResources',
    'service/standalone/map'
], function(
    template,
    factoryMapResources,
    ModelMapResources,
    mapInstance
) {
    "use strict";

    return AbstractService.extend({
        initialize: function() {

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
                    } catch(e) {}
                    this.drawResourceObject(domain);
                    mapInstance.update();
                }.bind(this));
            } else {
                this.drawResourceObject(domain);
            }
        },

        drawResourceObject: function(domain) {
            var result = mapInstance.help.fromIdToPlace(parseInt(domain.get('pos_id'), 10));
            var domCell = mapInstance.getDomCell(result.x, result.y);

            if(domain.$$domCell === domCell) {
                return false;
            }

            if(!domain.$$domCell) {
                domain.$$container = jQuery(
                    template('elements/map/objects/resource', {
                        data: domain.toJSON()
                    })
                );
            }

            if(domCell) {
                domain.$$domCell = domCell;
                domCell.find('.cont').append(domain.$$container);
            }

            return true;
        }
    });
});
