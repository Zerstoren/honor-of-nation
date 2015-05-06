define('service/standalone/map/objects/army', [
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
            mapInstance.on('calculate', this.onUpdate, this);
        },

        addArmy: function (domain) {
            var location = domain.get('location'),
                armyItem = mapInstance.createUnitLayerControl();

            armyItem.setDomain(domain);
            domain.setLayerObject(armyItem);

            if (!this.armyMap[location]) {
                this.armyMap[location] = [];
            }

            this.armyMap[location].push(armyItem);

            domain.on('change:location', this.onUnitMove, this);
        },

        searchByPosition: function (x, y) {
            var location = mapInstance.help.fromPlaceToId(x, y);
            if (this.armyMap[location] && this.armyMap[location].length) {
                return this.armyMap[location];
            } else {
                return null;
            }
        },

        onUnitMove: function (domain, value) {
            var oldLocation = domain.previous('location'),
                location = domain.get('location'),
                armyItem = domain.getLayerObject();

            this.armyMap[oldLocation].splice(
                this.armyMap[oldLocation].indexOf(armyItem),
                1
            );

            if (!this.armyMap[location]) {
                this.armyMap[location] = [];
            }

            this.armyMap[location].push(armyItem);
        },

        onUpdate: function () {
            _.map(this.armyMap, function (item) {
                _.map(item, function (unit) {
                    unit.update();
                })
            });
        }
    });
});
