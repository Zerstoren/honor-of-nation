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
            this.playerView.on('save-info', this.onSaveInfo, this);

            this.user = null;
        },

        render: function (holder) {
            this.playerView.render(holder);
        },

        unRender: function () {
            this.playerView.unRender();
            this.user = null;
        },

        onSearchUser: function(userLogin) {
            gatewayAdmin.searchUser(userLogin, function (err, user, resources) {
                if (!err) {
                    this.user = user;
                    this.playerView.showUserData(user, resources);
                }
            }.bind(this));
        },

        onSaveInfo: function (resources) {
            gatewayAdmin.saveUserResources(this.user.get('login'), resources, function (err) {
                if (!err) {
                    this.playerView.successSave();
                }
            }.bind(this));
        }
    });
});