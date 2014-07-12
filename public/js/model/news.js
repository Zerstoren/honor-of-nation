(function () {
    'use strict';

    define('model/news', [
        'factory/user'
    ], function (
        factoryUser
    ) {
        return AbstractModel.extend({
            model_url: '/news/',

            initialize: function () {
                this.on('change:user', this.onChangeUser, this);
            },

            onChangeUser: function (domain, value) {
                var userDomain = factoryUser.getDomainFromData({
                    id: value
                });

                this.set('user', userDomain, {silent: true});
            }
        });
    });
}());
