define('factory/user', [
    'factory/abstract',
    'model/user'
], function (AbstractFactory, userDomain) {
    'use strict';

    var UserFactory = function () {};
    _.extend(UserFactory.prototype, AbstractFactory.prototype, {
        domain: userDomain
    });

    return new UserFactory();
});
