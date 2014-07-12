define('gateway/admin', [
    'gateway/abstract'
], function (
    GatewayAbstract
) {
    var GatewayAdmin = function () {

    };

    GatewayAdmin.prototype.fillMap = function (data, fn) {
        this.socket.send('/admin/fillTerrain', data, fn);
    };

    _.extend(GatewayAdmin.prototype, GatewayAbstract.prototype);

    return new GatewayAdmin();
});