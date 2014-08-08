define('gateway/map', [
], function () {
    var GatewayMap = AbstractGateway.extend({
        initialize: function () {
            this.socket.on('/sync/map/reload_region', function (message) {
                this.trigger('reloadRegion', message);
            }, this)
        },

        loadChunks: function (chunkList, fn) {
            this.socket.send('/map/load_chunks', {
                chunkList: chunkList
            }, function (data) {
                if (data.done) {
                    fn(data);
                }
            });
        }
    });

    return new GatewayMap();
});
