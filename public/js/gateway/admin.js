define('gateway/admin', [
    'factory/user',
    'factory/resources'
], function (
        userFactory,
        resourcesFactory
) {
    var GatewayAdmin = AbstractGateway.extend({
        fillMap: function (data, fn) {
            this.socket.send('/admin/fillTerrain', data, fn);
        },

        searchUser: function (login, fn) {
            this.socket.send('/admin/searchUser', {
                login: login
            }, function (data) {
                var resources, user;

                if (data.done === false) {
                    fn(data.error);
                } else {
                    user = userFactory.getDomainFromData(data.user);
                    resources = resourcesFactory.getDomainFromData(data.user, data.resources);
                    fn(false, user, resources);
                }
            });
        },

        saveUserResources: function (userLogin, resources, fn) {
            this.socket.send('/admin/saveResources', {
                userLogin: userLogin,
                resources: resources
            }, function (data) {
                fn(false);
            });
        },

        saveCoordinate: function (data, fn) {
            this.socket.send('/admin/saveUserShowCoordinate', {
                data: data
            }, function (result) {
                if (result.done) {
                    fn(true);
                }
            })
        }
    });

    return new GatewayAdmin();
});