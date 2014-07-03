define('service/standalone/mapInterface', [
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

    var MapInterface = function () {

    };

    MapInterface.prototype.render = function () {
        if (this._renderedChecking() === true) {
            return false;
        }

        preStart.map();
        preStart.map.header.on('onMenuClick', this.onClickMenu, this);

        return true;
    };

    MapInterface.prototype.onClickMenu = function (type) {
        switch(type) {
            case 'admin':
                systemRoute.navigate('/admin');
                break;

            default:
                alert(type + ' is not created');
                break;
        }
    };

    MapInterface.prototype._renderedChecking = function () {
        return jQuery('.mpi__header').length !== 0;
    };

    _.extend(MapInterface.prototype, ServiceAbstract.prototype);

    return new MapInterface();
});