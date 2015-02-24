define('service/standalone/messages', [
    'system/socket',
    'service/standalone/map',

    'service/standalone/user',
    'factory/town',
    'factory/army',
    'factory/mapResources'
], function (
    systemSocket,
    mapInstance,

    serviceStandaloneUser,
    factoryTown,
    factoryArmy,
    factoryMapResources
) {
    var Messages = AbstractService.extend({
        init: function () {
            systemSocket.on('message:/delivery/resourceUpdate', this.onResourcesUpdate, this);
            systemSocket.on('message:/delivery/buildsUpdate', this.onBuildsUpdate, this);
            systemSocket.on('message:/delivery/unitsUpdate', this.onUnitsUpdate, this);
            systemSocket.on('message:/delivery/unitsUpdateOnMap', this.onUnitsUpdateOnMap, this);
            systemSocket.on('message:/delivery/townUpdate', this.onTownUpdate, this);
            systemSocket.on('message:/delivery/mapResourcesUpdate', this.onMapResourceUpdate, this)
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
        },

        onTownUpdate: function (data) {
            if (!data.done) {
                return;
            }

            var town = factoryTown.getDomainFromData(data.town);
            town.set(data.town);
            mapInstance.update();
        },

        onMapResourceUpdate: function (data) {
            if (!data.done) {
                return;
            }

            _.each(data.resources, function (resource) {
                factoryMapResources.updateDomainFromData(resource);
                mapInstance.update();
            });
        }
    });

    return new Messages();
});