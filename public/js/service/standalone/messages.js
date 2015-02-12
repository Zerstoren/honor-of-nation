define('service/standalone/messages', [
    'system/socket',

    'service/standalone/user',
    'factory/town',
    'factory/army'
], function (
    systemSocket,

    serviceStandaloneUser,
    factoryTown,
    factoryArmy
) {
    var Messages = AbstractService.extend({
        init: function () {
            systemSocket.on('message:/delivery/resourceUpdate', this.onResourcesUpdate, this);
            systemSocket.on('message:/delivery/buildsUpdate', this.onBuildsUpdate, this);
            systemSocket.on('message:/delivery/unitsUpdate', this.onUnitsUpdate, this);
            systemSocket.on('message:/delivery/unitsUpdateOnMap', this.onUnitsUpdateOnMap, this);
        },

        onResourcesUpdate: function (msg) {
            serviceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (domain) {
                domain.getResources().set(msg.resources);
            });
        },

        onBuildsUpdate: function (msg) {
            var townDomain = factoryTown.getFromPool(msg.town);
            townDomain.set({
                'queue': msg.queue,
                'builds': msg.builds
            });
        },

        onUnitsUpdate: function (msg) {
            this.trigger('unitsUpdate', msg.town, msg.armyQueue);
        },

        onUnitsUpdateOnMap: function (data) {
            if (!data.done) {
                return;
            }

            var i;
            for (i = 0; i < data.units.length; i++) {
                factoryArmy.getDomainFromData(data.units[i]);
            }
        }
    });

    return new Messages();
});