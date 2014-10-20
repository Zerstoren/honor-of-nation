define('service/admin/town', [
    'view/admin/town',
    'gateway/admin'
], function (
    ViewAdminTown,
    gatewayAdmin
) {
    return AbstractService.extend({
        initialize: function () {
            this.townView = new ViewAdminTown();
            this.townView.on('search', this.onSearch, this);
            this.townView.on('save', this.onSave, this);
        },

        render: function (holder) {
            this.townView.render(holder);
        },

        unRender: function () {
            this.townView.unRender();
        },

        onSearch: function (x, y) {
            gatewayAdmin.loadTownMap(x, y, function (users, town) {
                this.townView.showEdit(users, town);
            }.bind(this));
        },

        onSave: function (town) {
            gatewayAdmin.saveTownMap(town, function (townDomain) {
                this.townView.successSave(townDomain);
            }.bind(this));
        }
    })
});