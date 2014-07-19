define('gateway/admin', [], function () {
    var GatewayAdmin = AbstractGateway.extend({
        fillMap: function (data, fn) {
            this.socket.send('/admin/fillTerrain', data, fn);
        },

        searchUser: function (login, fn) {
            this.socket.send('/admin/searchUser', {
                login: login
            }, function (data) {

            });
        }
    });

    return new GatewayAdmin();
});