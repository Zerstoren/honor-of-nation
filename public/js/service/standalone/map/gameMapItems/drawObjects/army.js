define('service/standalone/map/gameMapItems/drawObjects/army', [
    'system/template',
    'factory/army',
    'model/army',
    'service/standalone/map',
    'service/standalone/math'
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

        updateArmyPosition: function (oldLocation, general) {
            var indexPosition = this.armyMap[oldLocation].indexOf(general),
                location = general.get('location');

            this.armyMap[oldLocation].splice(indexPosition, 1);
            if (!this.armyMap[location]) {
                this.armyMap[location] = [];
            }

            this.armyMap[location].push(general);
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

                this.getArmyPathWay(domain);
            }

            return true;
        },

        getArmyPathWay: function (domain) {
            var i, position, domCell,
                path = domain.get('move_path');

            for (i = 0; i < path.length; i++) {
                position = mapInstance.help.fromIdToPlace(path['pos_id']);
                domCell = mapInstance.getDomCell(position[0], position[1]);
                domCell.find('.cont').append('<div class="unit_move_path ' + path['direction'] + '"></div>');

                console.log(path);
            }
        }
    });
});
