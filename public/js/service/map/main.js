define('service/map/main', [
    'factory/army',
    'service/standalone/map',
    'service/standalone/map/draw',

    'view/map/unitsManipulate',

    'gateway/army'
], function (
    factoryArmy,
    mapInstance,
    mapDrawInstance,

    ViewMapUnitsManipulate,

    gatewayArmy
) {
    return AbstractService.extend({
        initialize: function () {
            factoryArmy.on('add', this.onAddArmy, this);
            this.viewUnitsManipulate = new ViewMapUnitsManipulate();
            this.viewUnitsManipulate.on('moveArmy', this.onMoveArmy, this);
        },

        onAddArmy: function (domain) {
            mapDrawInstance.getInstanceArmy().addArmy(domain);
            mapInstance.update();
        },

        onMoveArmy: function (armyId, x, y) {
            gatewayArmy.move(armyId, x, y);
        }
    });
});
