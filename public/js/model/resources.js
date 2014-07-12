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

            initialize: function (userDomain) {
                AbstractModel.prototype.initialize.apply(this, arguments);
                this.user = userDomain;
                this.load();
            },

            load: function () {
                this.sync('get', this, {
                    data: {
                        user: this.user.get('_id')
                    },
                    success: this.onLoad.bind(this)
                })
            },

            onLoad: function (data, message) {
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
