define('model/town', [
    'system/socket'
], function (socket) {
    return AbstractModel.extend({
        model_url: 'town',

        getById: function (callback) {
            this.sync('get', {
                data: {
                    'id': this.get('id')
                },
                success: function (town) {
                    this.set(town);
                    success();
                }
            });
        },

        mapLoad: function (success) {
            this.sync('get_pos_id', {
                data: {
                    posId: this.get('pos_id')
                },
                success: function (town) {
                    this.set(town);
                    success();
                }.bind(this)
            });
        }
    });
});