define('gateway/army', [
    'model/army',
    'collection/army'
], function (
    ModelArmy,
    CollectionArmy
) {
    var GatewayArmy = AbstractGateway.extend({
        detail: function (id, user, fn) {
            this.socket.send('/army/detail', {
                army: id,
                user: user.get('_id')
            }, function (data) {
                if (data.done) {
                    fn(
                        this._createArmyFromDeepObject(
                            data
                        )
                    );
                }
            }.bind(this));
        },

        _createArmyFromDeepObject: function (data) {
            var i, domain, suite, sub_army = [];

            domain = new ModelArmy(data.current);
            suite = data.suite ? new ModelArmy(data.suite) : null;
            for(i = 0; i < data.sub_army.length; i++) {
                sub_army.push(
                    this._createArmyFromDeepObject(data.sub_army[i])
                );
            }

            domain.set('suite', suite);
            domain.set('sub_army', sub_army);

            return domain;
        },

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
