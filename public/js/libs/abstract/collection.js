define('libs/abstract/collection', [
    'system/socket'
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

        where: function () {
            return new this.constructor(
                Backbone.Collection.prototype.where.apply(this, arguments)
            );
        },

        sync: function (method, options) {
            var url = '/collection/' + this.collection_url + '/' + method,
                data = options.data || {};

            socket.send(url, data, function (data) {
                if (!data.done) {
                    return;
                }

                var i, list = data.data;

                this.reset();
                for (i = 0; i < list.length; i++) {
                    this.add(new this.model(list[i]));
                }

                if (options.success) {
                    options.success(this);
                }
            }.bind(this));
        }
    });
});
