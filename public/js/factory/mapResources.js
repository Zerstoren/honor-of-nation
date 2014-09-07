define('factory/resources', [
    'model/mapResources'
], function (MapResourcesDomain) {
    'use strict';

    var ResourcesFactory = AbstractFactory.extend({
        domain: MapResourcesDomain,

        getDomainFromData: function (data) {
            var domain = new this.domain();
            domain.set('pos_id', data.pos_id);
            domain.set('type', data.type);
            domain.set('user', data.user);
            domain.set('town', data.town);
            domain.set('count', data.count);
            domain.set('production', data.production);

            return domain;

        }
    });
    return new ResourcesFactory();
});
