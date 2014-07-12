define('service/admin/main', [
    'system/preStart',
    'system/route',
    'gateway/admin',

    'service/abstract',

    'view/admin/main',
    'view/admin/terrain'
], function (
    preStart,
    systemRoute,
    gatewayAdmin,

    ServiceAbstract,

    ViewAdminMain,
    ViewAdminTerrain
) {
    var Main = function () {
        this.selectType = null;

        this.mainView = new ViewAdminMain();
        this.mainView.on('close', this.onClose, this);
        this.mainView.on('selectType', this.onSelectType, this);

        this.terrainView = new ViewAdminTerrain();
        this.terrainView.on('send', this.onTerrainSend, this)
    };

    Main.prototype.render = function () {
        this.holder = preStart.map.body.getHolder();
        this.mainView.render(this.holder);
        this.onSelectType('terrain');
    };

    Main.prototype.unRender = function () {
        this.mainView.unRender();
        this.unSelectType();
    };

    Main.prototype.onClose = function () {
        systemRoute.navigate('');
    };

    Main.prototype.onSelectType = function (type) {
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
    };

    Main.prototype.unSelectType = function () {
        switch(this.selectType) {
            case 'terrain':
                this.terrainView.unRender();
                break;
        }

        this.selectType = null;
    };

    Main.prototype.onTerrainSend = function (data) {
        gatewayAdmin.fillMap(data, function (result) {
            this.terrainView.successSave();
        }.bind(this));
    };

    _.extend(Main.prototype, ServiceAbstract.prototype);

    return Main;
});