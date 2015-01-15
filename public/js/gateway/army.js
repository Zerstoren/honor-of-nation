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

        moveOut: function (id, fn) {
            this.socket.send('/army/out_build', {
                army: id
            }, function (data) {
                if (data.done) {
                    fn(data);
                }
            });
        },

        addSolidersToGeneral: function (soliders, general, fn) {
            this.socket.send('/army/add_soliders_general', {
                general: general,
                soliders: soliders
            }, function (data) {
                if (data.done) {
                    fn(data);
                }
            });
        },

        addSuite: function (general, solider, fn) {
            this.socket.send('/army/add_suite', {
                general: general,
                solider: solider
            }, function (data) {
                if (data.done) {
                    fn(data);
                }
            });
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
