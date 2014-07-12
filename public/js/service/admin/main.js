define('service/admin/main', [
    'system/preStart',
    'system/route',
    'gateway/admin',

    'view/admin/main',
    'view/admin/terrain'
], function (
    preStart,
    systemRoute,
    gatewayAdmin,

    ViewAdminMain,
    ViewAdminTerrain
) {
    return AbstractService.extend({
        initialize: function () {
            this.selectType = null;

            this.mainView = new ViewAdminMain();
            this.mainView.on('close', this.onClose, this);
            this.mainView.on('selectType', this.onSelectType, this);

            this.terrainView = new ViewAdminTerrain();
            this.terrainView.on('send', this.onTerrainSend, this)
        },

        render: function () {
            this.holder = preStart.map.body.getHolder();
            this.mainView.render(this.holder);
            this.onSelectType('terrain');
        },

        unRender: function () {
            this.mainView.unRender();
            this.unSelectType();
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
                    this.terrainView.render(holder);
                    break;
            }

            this.selectType = type;
        },

        unSelectType: function () {
            switch(this.selectType) {
                case 'terrain':
                    this.terrainView.unRender();
                    break;
            }

            this.selectType = null;
        },

        onTerrainSend: function (data) {
            gatewayAdmin.fillMap(data, function (result) {
                this.terrainView.successSave();
            }.bind(this));
        }
    });
});