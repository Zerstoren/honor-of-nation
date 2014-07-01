(function () {
    'use strict';

    define('model/user', [
        'model/abstract',

        'model/resources'
    ], function (
        abstractDomain,

        ModelResources
    ) {
        return abstractDomain.extend({
            model_url: 'user',

            auth: function (login, password, callback) {
                this.sync('login', this, {
                    data: {
                        login: login,
                        password: password
                    },
                    success: this.onLogin.bind(this, callback)
                })
            },

            onLogin: function (callback, data, message) {
                if (data) {
                    this.attributes = data;
                    this.attributes.resources = new ModelResources(this);
                }

                if (callback) {
                    callback(this, message.auth_result);
                }
            }
        });
    });
}());
