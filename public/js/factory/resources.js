define('factory/resources', [
    'model/resources'
], function (ResourcesDomain) {
    'use strict';

    var ResourcesFactory = AbstractFactory.extend({
        domain: ResourcesDomain,

        getDomainFromData: function (user, data) {
            var domain = new this.domain(user);
            domain.set(domain.RUBINS, data[domain.RUBINS]);
            domain.set(domain.WOOD, data[domain.WOOD]);
            domain.set(domain.STEEL, data[domain.STEEL]);
            domain.set(domain.STONE, data[domain.STONE]);
            domain.set(domain.EAT, data[domain.EAT]);
            domain.set(domain.GOLD, data[domain.GOLD]);

            return domain;
        }
    });
    return new ResourcesFactory();
});
