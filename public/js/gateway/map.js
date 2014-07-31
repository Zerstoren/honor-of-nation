define('gateway/map', [
], function () {
    var GatewayMap = AbstractGateway.extend({
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
