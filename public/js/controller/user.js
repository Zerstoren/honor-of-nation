define('controller/user', [
    'service/standalone/user'
], function(
    serviceUser
) {
    'use strict';

    return {
        login: function() {
            serviceUser.renderForm();
        }
    };
});
