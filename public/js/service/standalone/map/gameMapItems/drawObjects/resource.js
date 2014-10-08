define('service/standalone/map/gameMapItems/drawObjects/resource', [
    'system/template',
    'factory/mapResources',
    'model/mapResources',
    'service/standalone/map/gameMapItems/init'
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

        getResourceObject: function(x, y, type) {
            var domain,
                self = this,
                posId = mapInstance.help.fromPlaceToId(x, y);

            domain = factoryMapResources.getFromPool(posId);

            if(domain === undefined) {
                domain = new ModelMapResources();
                domain.set('pos_id', posId);
                domain.mapLoad(function () {
                    this.drawBuildObject(domain);
                }.bind(this));
            } else {
                this.drawBuildObject(domain);
            }
        },

        drawBuildObject: function(domain) {
            var result = mapInstance.help.fromIdToPlace(parseInt(domain.get('pos_id'), 10));
            var domCell = mapInstance.getDomCell(result.x, result.y);

            if(domain.$$domCell === domCell) {
                return false;
            }

            if(!domain.$$domCell) {
                domain.$$container = template('elements/map/objects/resource', {
                    data: domain.toJSON()
                });
            }

            if(domCell) {
                domain.$$domCell = domCell;
                domCell.find('.cont').append(domain.$$container);
            }

            return true;
        }
    });
});
