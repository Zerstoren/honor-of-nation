define('service/standalone/messages', [
    'system/socket',

    'service/standalone/user'
], function (
    systemSocket,

    serviceStandaloneUser
) {
    var Messages = AbstractService.extend({
        init: function () {
            systemSocket.on('message/delivery/resourceUpdate', this.onResourcesUpdate, this);
        },

        onResourcesUpdate: function (msg) {
            if (msg.done) {
                serviceStandaloneUser.getMe(function (domain) {
                    domain.getResources().set(msg.resources);
                })
            }
        }
    });

    return new Messages();
});