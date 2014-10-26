define('gateway/town', [], function () {
    var GatewayTown = AbstractGateway.extend({
        loadBuilds: function (townDomain, success) {
            this.socket.send('/town/get_builds', {
                id: townDomain.get('id')
            }, function (data) {
                if (data.done) {
                    success(data.data);
                }
            });
        }
    });

    return new GatewayTown();
});