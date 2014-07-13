define('service/admin/main', [
    'system/preStart',
    'system/route',
    'gateway/admin',

    'service/admin/terrain',

    'view/admin/main'
], function (
    preStart,
    systemRoute,
    gatewayAdmin,

    ServiceAdminTerrain,

    ViewAdminMain
) {
    return AbstractService.extend({
        initialize: function () {
            this.selectType = null;

            this.mainView = new ViewAdminMain();
            this.mainView.on('close', this.onClose, this);
            this.mainView.on('selectType', this.onSelectType, this);

            this.serviceTerrain = new ServiceAdminTerrain();
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
            }

            this.unSelectType();
            this.selectType = type;
        },

        unSelectType: function (reset) {
            switch(this.selectType) {
                case 'terrain':
                    this.serviceTerrain.unRender();
                    break;
            }

            if (reset) {
                this.selectType = null;
            }
        }
    });
});