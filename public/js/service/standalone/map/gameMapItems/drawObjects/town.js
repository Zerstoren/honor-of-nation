define('service/standalone/map/gameMapItems/drawObjects/town', [
    'system/template',

    'factory/town',
    'model/town',


    'service/standalone/map'
], function(
    template,

    factoryTown,
    ModelTown,

    mapInstance
) {
    "use strict";

    return AbstractService.extend({
        initialize: function() {

        },

        getTownObject: function(x, y, type) {
            var domain,
                self = this,
                posId = mapInstance.help.fromPlaceToId(x, y);

            domain = factoryTown.searchInPool('pos_id', posId)[0];

            if(domain === undefined) {
                domain = new ModelTown();
                domain.set('pos_id', posId);
                domain.mapLoad(function () {
                    this.drawBuildObject(domain);
                    try {
                        factoryTown.pushToPool(domain);
                    } catch (e) {}
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
                domain.$$container = template('elements/map/objects/town', {
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
