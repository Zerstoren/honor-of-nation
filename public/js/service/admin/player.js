define('service/admin/player', [
    'gateway/admin',

    'view/admin/player'
], function (
    gatewayAdmin,

    ViewAdminPlayer
) {
    return AbstractService.extend({
        initialize: function () {
            this.playerView = new ViewAdminPlayer();

            this.playerView.on('search-user', this.onSearchUser, this);
        },

        render: function (holder) {
            this.playerView.render(holder);
        },

        unRender: function () {
            this.playerView.unRender();
        },

        onSearchUser: function(userLogin) {
            gatewayAdmin.searchUser(userLogin, function (data) {

            }.bind(this));
        }
    });
});