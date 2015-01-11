define('gateway/armyQueue', [
], function () {
    var GatewayArmyQueue = AbstractGateway.extend({
        create: function (town, unitId, count, fn) {
            this.socket.send('/army/queue/create', {
                'unit': unitId,
                'town': town.get('_id'),
                'count': count
            }, function (data) {
                if (data.done) {
                    fn(data);
                }
            });
        },

        remove: function (town, _id, fn) {
            this.socket.send('/army/queue/remove', {
                'town': town.get('_id'),
                'queue_id': _id
            }, function (data) {
                if (data.done) {
                    fn(data);
                }
            });
        }
    });

    return new GatewayArmyQueue();
});
