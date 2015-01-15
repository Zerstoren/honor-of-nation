define('gateway/army', [
], function () {
    var GatewayArmy = AbstractGateway.extend({
        merge: function (army, fn) {
            this.socket.send('/army/merge', {
                'army_list': army
            }, function (data) {
                if (data.done) {
                    fn(data);
                }
            }.bind(this));
        },

        split: function (id, size, fn) {
            this.socket.send('/army/split', {
                'size': size,
                'army': id
            }, function (data) {
                if (data.done) {
                    fn(data);
                }
            })
        },

        dissolution: function (id, fn) {
            this.socket.send('/army/dissolution', {
                'army': id
            }, function (data) {
                if (data.done) {
                    fn(data);
                }
            });
        }
    });

    return new GatewayArmy();
});
