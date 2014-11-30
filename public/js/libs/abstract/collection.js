define('libs/abstract/collection', [
    'system/socket',
], function (
    socket
) {
    window.AbstractCollection = Backbone.Collection.extend({
        collection_url: null,
        model: null,

        initialize: function () {
            if (this.collection_url === null) {
                throw new Error('For collection not set url block');
            }

            if (this.model === null) {
                throw new Error('For collection not set model');
            }
        },

        sync: function (method, model, options) {
            var url = '/collection/' + this.collection_url + '/' + method,
                data = options.data || {};

            socket.send(url, data, function (data) {
                if (!data.done) {
                    return;
                }

                var i, list = data.data;
                for (i = 0; i < list; i++) {
                    this.add(this.model(list));
                }

                if (options.success) {
                    options.success(this);
                }
            });
        }
    });
});
