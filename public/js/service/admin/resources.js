define('service/admin/resources', [
    'gateway/admin',
    'view/admin/resources'
], function (
    gatewayAdmin,
    ViewAdminResources
) {
    return AbstractService.extend({
        initialize: function () {
            this.resourcesView = new ViewAdminResources();
            this.resourcesView.on('search', this.onSearch, this);
            this.resourcesView.on('save', this.onResourcesSend, this);
        },

        render: function (holder) {
            this.resourcesView.render(holder);
        },

        unRender: function () {
            this.resourcesView.unRender();
        },

        onSearch: function (x, y) {
            gatewayAdmin.loadResourceMap(x, y, function (domain, users, towns) {
                this.resourcesView.showEditForm(domain, users, towns);
            }.bind(this));
        },

        onResourcesSend: function (domain) {
            gatewayAdmin.saveResourceDomain(domain, function (result) {
                if (result.done) {
                    this.resourcesView.showSuccess();
                }
            }.bind(this));
        }
    });
});
