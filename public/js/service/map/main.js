define('service/map/main', [
    'system/preStart',
    'system/route',

    'model/user',
    'collection/user',

    'view/elements/resource'
], function (
    preStart,
    systemRoute,

    ModelUser,
    CollectionUser,

    viewElementResource
) {
    return AbstractService.extend({

    });
});
