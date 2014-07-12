define('factory/user', [
    'model/user'
], function (userDomain) {
    'use strict';

    var UserFactory = AbstractFactory.extend({
        domain: userDomain
    });

    return new UserFactory();
});
