define('service/standalone/messages', [
    'system/socket',

    'service/standalone/user',
    'factory/town'
], function (
    systemSocket,

    serviceStandaloneUser,
    factoryTown
) {
    var Messages = AbstractService.extend({
        init: function () {
            systemSocket.on('message:/delivery/resourceUpdate', this.onResourcesUpdate, this);
            systemSocket.on('message:/delivery/buildsUpdate', this.onBuildsUpdate, this);
        },

        onResourcesUpdate: function (msg) {
            serviceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (domain) {
                domain.getResources().set(msg.resources);
            });
        },

        onBuildsUpdate: function (msg) {
            townDomain = factoryTown.getFromPool(msg.town);
            townDomain.set({
                'queue': msg.queue,
                'builds': msg.builds
            });
        }
    });

    return new Messages();
});