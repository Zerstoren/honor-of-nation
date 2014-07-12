define('libs/abstract/collection', [], function () {
    window.AbstractCollection = Backbone.Collection.extend({
        collection_url: null,

        initialize: function () {
            if (this.collection_url === null) {
                throw new Error('For collection not set url block');
            }
        },

        sync: function (method, model, options) {
            var url = '/collection/' + this.collection_url + '/' + method,
                data = options.data || {};

            socket.send(url, data, function (data) {
                if (options.success) {
                    options.success(data.data);
                }
            });
        }
    });
});
