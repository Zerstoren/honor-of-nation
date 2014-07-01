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

    Map.prototype.render = function () {
        preStart.map();

        preStart.map.header.on('onMenuClick', this.onClickMenu, this);
    };

    Map.prototype.onClickMenu = function (type) {
        switch(type) {
            case 'admin':
                systemRoute.navigate('/admin', false, true);
                break;

            default:
                alert(type + ' is not created');
                break;
        }
    };

    _.extend(Map.prototype, ServiceAbstract.prototype);

    return Map;
});
