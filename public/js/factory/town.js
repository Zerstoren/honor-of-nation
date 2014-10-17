define('factory/town', [
    'model/town'
], function (townDomain) {
    'use strict';

    var TownFactory = AbstractFactory.extend({
        domain: townDomain
    });

    return new TownFactory();
});
