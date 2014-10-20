define('gateway/admin', [
    'factory/user',
    'factory/resources',
    'factory/mapResources',
    'factory/town'
], function (
        userFactory,
        resourcesFactory,
        mapResourceFactory,
        factoryTown
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
                fromX: data.fromX,
                fromY: data.fromY,
                toX: data.toX,
                toY: data.toY
            }, function (result) {
                if (result.done) {
                    fn(true);
                }
            });
        },

        loadResourceMap: function (x, y, fn) {
            this.socket.send('/admin/loadResourceMap', {
                x: x,
                y: y
            }, function (result) {
                var domain = false;

                if (result.resource) {
                    domain = mapResourceFactory.getDomainFromData(result.resource);
                }

                fn(domain, result.users, result.towns);
            });
        },

        saveResourceDomain: function (domain, fn) {
            this.socket.send('/admin/saveResourceDomain', {
               domain: domain.attributes
            }, function (result) {
                fn(result);
            });
        },

        loadTownMap: function (x, y, fn) {
            this.socket.send('/admin/loadTownMap', {
                x: x,
                y: y
            }, function (result) {
                if (result.done) {
                    fn(result.users);
                }
            });
        },

        saveTownMap: function (town, fn) {
            this.socket.send('/admin/saveTownDomain', {
                domain: town
            }, function (result) {
                if (result.done) {
                    var domain = factoryTown.getDomainFromData(result.town);
                    fn(domain);
                }
            });
        }
    });

    return new GatewayAdmin();
});