define('system/router', function() {
    'use strict';

    return {
        ''                  : 'main/main',
        'login'             : 'user/login',

        'admin'             : 'admin/terrain'
    };
});