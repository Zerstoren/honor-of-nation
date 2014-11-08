define('system/router', function() {
    'use strict';
    return {
        'main/main'         : '',
        'user/login'        : 'login',

        'admin/admin'       : 'admin',

        'town/show'         : /^town\/([0-9abcdef]{24})$/
    };
});