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

        search: function (name, value) {
            var search = {};
            search[name] = value;
            return this.where(search).at(0);
        },

        where: function () {
            return new this.constructor(
                Backbone.Collection.prototype.where.apply(this, arguments)
            );
        },

        whereIn: function (attr, values) {
            var result = this.filter(function (model) {
                return values.indexOf(model.get(attr)) !== -1;
            });

            return new this.constructor(result);
        },

        update: function (data) {
            var i;

            for (i = 0; i < data.length; i++) {
                this.add(new this.model(data[i]));
            }
        },

        clean: function () {
            this.remove(this.models);
        },

        sync: function (method, options) {
            var url = '/collection/' + this.collection_url + '/' + method,
                data = options.data || {};

            socket.send(url, data, function (data) {
                if (!data.done) {
                    return;
                }

                this.reset();
                this.update(data.data);

                if (options.success) {
                    options.success(this);
                }
            }.bind(this));
        }
    });
});
