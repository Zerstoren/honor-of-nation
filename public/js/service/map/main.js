define('service/map/main', [
    'system/preStart',
    'system/route',
    'service/abstract',

    'model/user',
    'collection/user',

    'view/elements/resource'
], function (
    preStart,
    systemRoute,

    ServiceAbstract,
    ModelUser,
    CollectionUser,

    viewElementResource
) {
    var Map = function () {

    };

    _.extend(Map.prototype, ServiceAbstract.prototype);

    return Map;
});
