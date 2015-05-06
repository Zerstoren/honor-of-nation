define('service/standalone/mapInterface', [
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

    var MapInterface = AbstractService.extend({
        render: function () {
            if (this._renderedChecking() === true) {
                return false;
            }

            preStart.map();
            preStart.map.header.on('onMenuClick', this.onClickMenu, this);
            preStart.map.footer.on('open', this.onOpen, this);

            return true;
        },

        onOpen: function (type, domain) {
            switch(type) {
                case 'town':
                    systemRoute.navigate('/town/' + domain.get('_id'));
                    break;
            }
        },

        onClickMenu: function (type) {
            switch(type) {
                case 'admin':
                    systemRoute.navigate('/admin');
                    break;

                default:
                    alert(type + ' is not created');
                    break;
            }
        },

        _renderedChecking: function () {
            return jQuery('.mpi__header').length !== 0;
        }
    });

    return new MapInterface();
});