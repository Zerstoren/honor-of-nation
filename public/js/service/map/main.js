define('service/map/main', [
    'factory/army',
    'service/standalone/map',
    'service/standalone/map/draw'
], function (
    factoryArmy,
    mapInstance,
    mapDrawInstance
) {
    return AbstractService.extend({
        initialize: function () {
            factoryArmy.on('add', this.onAddArmy, this);
        },

        onAddArmy: function (domain) {
            mapDrawInstance.getInstanceArmy().addArmy(domain);
            mapInstance.update();
        }
    });
});
