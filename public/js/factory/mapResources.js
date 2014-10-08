define('factory/mapResources', [
    'model/mapResources'
], function (MapResourcesDomain) {
    'use strict';

    var ResourcesFactory = AbstractFactory.extend({
        domain: MapResourcesDomain,
        index: 'pos_id',

        getDomainFromData: function (data) {
            var domain;

            if (!(domain = this.getFromPool(data._id))) {
                domain = new this.domain();
            }

            domain.set('_id', data._id);
            domain.set('pos_id', data.pos_id);
            domain.set('type', data.type);
            domain.set('user', data.user);
            domain.set('town', data.town);
            domain.set('amount', data.amount);
            domain.set('base_output', data.base_output);
            domain.set('output', data.output);

            return domain;

        }
    });
    return new ResourcesFactory();
});
