define('gateway/admin', [], function () {
    var GatewayAdmin = AbstractGateway.extend({
        fillMap: function (data, fn) {
            this.socket.send('/admin/fillTerrain', data, fn);
        }
    });

    return new GatewayAdmin();
});