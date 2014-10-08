(function () {
    'use strict';

    define('model/mapResources', [], function () {
        return AbstractModel.extend({
            model_url: 'map_resources',

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
}());
