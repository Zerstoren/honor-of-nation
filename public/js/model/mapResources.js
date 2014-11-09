define('model/mapResources', [
    'factory/user'
], function (
    factoryUser
) {
    return AbstractModel.extend({
        model_url: 'map_resources',

        initialize: function () {
            AbstractModel.prototype.initialize.apply(this, arguments);
            this.on('change:user', this.onSetUser, this);
        },

        teardown: function () {
            AbstractModel.prototype.teardown.apply(this, arguments);
            this.un('change:user', this.onSetUser, this);
        },

        onSetUser: function (self, data, oldData) {
            this.attributes.user = data ? factoryUser.getDomainFromData(data) : data;
        },

        getUserLogin: function () {

            alert(1);
            return this.get('user').get('login');
        },

        mapLoad: function (success) {
            this.sync('get', {
                data: {
                    posId: this.get('pos_id')
                },
                success: function (resource) {
                    this.set(resource);
                    success();
                }.bind(this)
            });
        }
    });
});
