define('gateway/armyQueue', [
], function () {
    var GatewayMap = AbstractGateway.extend({
        create: function (town, unitId, count, fn) {
            this.socket.send('/army/queue/add', {
                'unitId': unitId,
                'town': town.get('_id'),
                'count': count
            }, function (data) {
                if (data.done) {
                    fn(data);
                }
            });
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
