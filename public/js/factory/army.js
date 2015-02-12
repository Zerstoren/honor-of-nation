define('factory/army', [
    'model/army'
], function (ArmyDomain) {
    'use strict';

    var ArmyFactory = AbstractFactory.extend({
        domain: ArmyDomain,

        getDomainFromData: function (data) {
            var domain;

            if (!(domain = this.getFromPool(data._id))) {
                domain = new this.domain(data);
                this.trigger('add', domain);
            }

            return domain;
        }
    });
    return new ArmyFactory();
});
