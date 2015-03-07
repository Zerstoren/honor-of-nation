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
        pathway: {
            t:  jQuery('<div class="unit_move_path t"></div>'),
            tr: jQuery('<div class="unit_move_path tr"></div>'),
            r:  jQuery('<div class="unit_move_path r"></div>'),
            br: jQuery('<div class="unit_move_path br"></div>'),
            b:  jQuery('<div class="unit_move_path b"></div>'),
            bl: jQuery('<div class="unit_move_path bl"></div>'),
            l:  jQuery('<div class="unit_move_path l"></div>'),
            tl: jQuery('<div class="unit_move_path tl"></div>'),
            c:  jQuery('<div class="unit_move_path c"></div>')
        },

        initialize: function () {
            this.armyMap = {};
            mapInstance.on('postUpdate', this.onUpdate, this);
            this.armyForPostUpdate = [];
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

        onUpdate: function () {
            var i;
            for(i = 0; i < this.armyForPostUpdate.length; i++) {
                this.getArmyPathWay(this.armyForPostUpdate[i]);
            }
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

                this.armyForPostUpdate.push(domain);
            }

            return true;
        },

        getArmyPathWay: function (domain) {
            var i, position, domCell,
                path = domain.get('move_path');

            for (i = 0; i < path.length; i++) {
                position = mapInstance.help.fromIdToPlace(path[i]['pos_id']);
                domCell = mapInstance.getDomCell(position.x, position.y);
                domCell.find('.cont').append(this.pathway[path[i]['direction']].clone());
            }

            this.armyForPostUpdate = [];
        }
    });
});
