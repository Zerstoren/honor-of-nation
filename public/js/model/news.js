(function () {
    'use strict';

    define('model/news', [
        'model/abstract',
        'factory/user'
    ], function (
        AbstractDomain,
        factoryUser
    ) {
        return AbstractDomain.extend({
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
