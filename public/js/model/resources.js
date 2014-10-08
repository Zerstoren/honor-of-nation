(function () {
    'use strict';

    define('model/resources', [], function () {
        return AbstractModel.extend({
            model_url: 'resources',

            RUBINS: 'rubins',
            WOOD  : 'wood',
            STEEL : 'steel',
            STONE : 'stone',
            EAT   : 'eat',
            GOLD  : 'gold',

            initialize: function (userDomain, load) {
                AbstractModel.prototype.initialize.apply(this, arguments);
                this.user = userDomain;

                if (load || false) {
                    this.load();
                }
            },

            load: function () {
                this.sync('get', {
                    data: {
                        user: this.user.get('_id')
                    },
                    success: this.onLoad.bind(this)
                });
            },

            onLoad: function (data) {
                if (data) {
                    this.attributes = data;
                }
            },

            getUser: function () {
                return this.user;
            }
        });
    });
}());
