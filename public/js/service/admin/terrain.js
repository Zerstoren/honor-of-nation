define('service/admin/terrain', [
    'gateway/admin',
    'view/admin/terrain'
], function (
    gatewayAdmin,
    ViewAdminTerrain
) {
    return AbstractService.extend({
        initialize: function () {
            this.terrainView = new ViewAdminTerrain();
            this.terrainView.on('send', this.onTerrainSend, this)
        },

        render: function (holder) {
            this.terrainView.render(holder);
        },

        unRender: function () {
            this.terrainView.unRender();
        },

        onTerrainSend: function (data) {
            gatewayAdmin.fillMap(data, function (result) {
                if (result.done) {
                    this.terrainView.successSave();
                }
            }.bind(this));
        }
    });
});
