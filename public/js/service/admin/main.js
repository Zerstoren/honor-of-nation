define('service/admin/main', [
    'system/preStart',
    'system/route',
    'gateway/admin',

    'service/admin/terrain',
    'service/admin/player',
    'service/admin/resources',
    'service/admin/town',

    'view/admin/main'
], function (
    preStart,
    systemRoute,
    gatewayAdmin,

    ServiceAdminTerrain,
    ServiceAdminPlayer,
    ServiceAdminResources,
    ServiceAdminTown,

    ViewAdminMain
) {
    return AbstractService.extend({
        initialize: function () {
            this.selectType = null;

            this.mainView = new ViewAdminMain();
            this.mainView.on('close', this.onClose, this);
            this.mainView.on('selectType', this.onSelectType, this);

            this.serviceTerrain = new ServiceAdminTerrain();
            this.servicePlayer = new ServiceAdminPlayer();
            this.serviceResources = new ServiceAdminResources();
            this.serviceTown = new ServiceAdminTown();
        },

        render: function () {
            this.holder = preStart.map.body.getHolder();
            this.mainView.render(this.holder);
            this.onSelectType('terrain');
        },

        unRender: function () {
            this.mainView.unRender();
            this.unSelectType(true);
        },

        onClose: function () {
            systemRoute.navigate('');
        },

        onSelectType: function (type) {
            if (type === this.selectType) {
                return;
            }

            var holder = this.mainView.getHolder();

            switch(type) {
                case 'terrain':
                    this.serviceTerrain.render(holder);
                    break;
                case 'player':
                    this.servicePlayer.render(holder);
                    break;
                case 'resources':
                    this.serviceResources.render(holder);
                    break;
                case 'town':
                    this.serviceTown.render(holder);
                    break;

            }

            this.unSelectType();
            this.selectType = type;
        },

        unSelectType: function (reset) {
            switch(this.selectType) {
                case 'terrain':
                    this.serviceTerrain.unRender();
                    break;
                case 'player':
                    this.servicePlayer.unRender();
                    break;
                case 'resources':
                    this.serviceResources.unRender();
                    break;
                case 'town':
                    this.serviceTown.unRender();
                    break;
            }

            if (reset) {
                this.selectType = null;
            }
        }
    });
});