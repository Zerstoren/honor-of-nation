define('model/town', [], function () {
    return AbstractModel.extend({
        model_url: 'town',

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