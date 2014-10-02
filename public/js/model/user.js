(function () {
    'use strict';

    define('model/user', [
        'model/resources'
    ], function (
        ModelResources
    ) {
        return AbstractModel.extend({
            model_url: 'user',

            auth: function (login, password, callback) {
                this.sync('login', this, {
                    data: {
                        login: login,
                        password: password
                    },
                    success: this.onLogin.bind(this, callback)
                });
            },

            getResources: function () {
                return this.resources;
            },

            onLogin: function (callback, data, message) {
                if (data) {
                    this.attributes = data.user;
                    this.resources = new ModelResources(data.resources);
                }

                if (callback) {
                    callback(this, message.auth_result);
                }
            }
        });
    });
}());
