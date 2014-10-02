define('service/standalone/map/gameMapItems/drawObjects/resource', [
    'factory/resources'
], function(
    factoryResources
) {
    "use strict";

    return AbstractService.extend({
        initialize: function($map, $template) {
            this.$mapDI = $map;
            this.$templateDI = $template;
            this.resourceFactory = factoryResources;
        },

        getResourceObject: function(x, y, type) {
            var domain,
                self = this,
                posId = this.$mapDI.help.fromPlaceToId(x, y);

            domain = this.resourceFactory.getFromIndex('pos_id', posId);

            if(domain === false) {
                this.resourceFactory.getAs(function(resourceDomain) {
                    self.drawBuildObject(x, y, resourceDomain);
                }, {
                    field: this.resourceFactory.FIELD_POSITION,
                    field_value: posId,
                    access: this.resourceFactory.ACCESS_VISIBLE,
                    access_value: ''
                });
            } else {
                this.drawBuildObject(x, y, domain[0]);
            }
        },

        drawBuildObject: function(x, y, domain) {
            var domCell = this.$mapDI.getDomCell(x, y);

            if(domain.$$domCell === domCell) {
                return false;
            }

            if(!domain.$$domCell) {
                domain.$$container = this.$templateDI.compile('map/objects/resource', {
                    data: domain.getData()
                });
            }

            if(domCell) {
                domain.$$domCell = domCell;
                domCell.find('.container').append(domain.$$container);
            }

            return true;
        }
    });
});
