define('service/standalone/mapInterface', [
    'system/preStart',
    'system/route',

    'model/user',
    'collection/user',

    'service/standalone/user',

    'view/elements/resource'
], function (
    preStart,
    systemRoute,

    ModelUser,
    CollectionUser,

    ServiceStandaloneUser,

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
                    ServiceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (user) {
                        if (user.get('_id') !== domain.get('user')._id) {
                            return;
                        }

                        systemRoute.navigate('/town/' + domain.get('_id'));
                    });

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