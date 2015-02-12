define('service/standalone/map/gameMapItems/drawObjects/army', [
    'system/template',
    'factory/army',
    'model/army',
    'service/standalone/map'
], function(
    template,
    factoryArmy,
    ModelArmy,
    mapInstance
) {
    "use strict";

    return AbstractService.extend({
        initialize: function () {
            this.armyMap = {};
        },

        addArmy: function (domain) {
            if (!this.armyMap[domain.get('location')]) {
                this.armyMap[domain.get('location')] = [];
            }

            this.armyMap[domain.get('location')].push(domain);
        },

        getArmyObject: function(x, y, armyLocation) {
            var domain,
                army = this.armyMap[armyLocation],
                domCell = mapInstance.getDomCell(x, y);

            for (var i = 0; i < army.length; i++) {
                domain = this.armyMap[armyLocation][i];
                if (domain.$$domCell === domCell) {
                    return false;
                }

                if (!domain.$$domCell) {
                    domain.$$container = template('elements/map/objects/army', {
                        data: domain.toJSON()
                    });
                }

                if (domCell) {
                    domain.$$domCell = domCell;
                    domCell.find('.cont').append(domain.$$container);
                }
            }

            return true;
        }
    });
});
