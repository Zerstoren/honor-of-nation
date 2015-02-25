define('factory/mapResources', [
    'model/mapResources',
    'factory/user'
], function (
    MapResourcesDomain,
    factoryUser
) {
    'use strict';

    var ResourcesFactory = AbstractFactory.extend({
        domain: MapResourcesDomain,

        getDomainFromData: function (data) {
            data.user = data.user ? factoryUser.getDomainFromData(data.user) : null;
            return AbstractFactory.prototype.getDomainFromData.apply(this, [data]);
        },

        updateDomainFromData: function (data) {
            data.user = data.user ? factoryUser.getDomainFromData(data.user) : null;
            return AbstractFactory.prototype.updateDomainFromData.apply(this, [data]);
        }
    });
    return new ResourcesFactory();
});
