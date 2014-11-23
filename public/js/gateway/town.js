define('gateway/town', [], function () {
    var GatewayTown = AbstractGateway.extend({
        loadBuilds: function (townDomain, success) {
            this.socket.send('/town_builds/get_builds', {
                town: townDomain.get('_id')
            }, function (data) {
                if (data.done) {
                    success(data.builds, data.queue);
                }
            });
        },

        createBuild: function (townDomain, key, level, success) {
            this.socket.send('/town_builds/create', {
                town: townDomain.get('_id'),
                key: key,
                level: level
            }, function (data) {
                if (data.done) {
                    success(data.builds, data.queue);
                }
            });
        },

        cancelBuild: function (townDomain, key, level, success) {
            this.socket.send('/town_builds/remove', {
                town: townDomain.get('_id'),
                key: key,
                level: level
            }, function (data) {
                if (data.done) {
                    success(data.builds, data.queue);
                }
            });
        }
    });

    return new GatewayTown();
});