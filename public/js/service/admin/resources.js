define('service/admin/resources', [
    'gateway/admin',
    'view/admin/resources'
], function (
    gatewayAdmin,
    ViewAdminResources,
    ModelMapResources
) {
    return AbstractService.extend({
        initialize: function () {
            this.resourcesView = new ViewAdminResources();
            this.resourcesView.on('search', this.onSearch, this)
        },

        render: function (holder) {
            this.resourcesView.render(holder);
        },

        unRender: function () {
            this.resourcesView.unRender();
        },

        onSearch: function (x, y) {
            gatewayAdmin.loadResourceMap(x, y, function (domain, users) {
                this.resourcesView.showEditForm(domain, users);
            }.bind(this));
        },

        onResourcesSend: function (data) {

        }
    });
});
