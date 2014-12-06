define('libs/abstract/model', ['system/socket'], function (socket) {
    window.AbstractModel = Backbone.Model.extend({
        model_url: null,

        initialize: function() {
            if (this.model_url === null) {
                throw new Error('For domain not set url block');
            }
        },

        sync: function (method, options) {
            options = options || {};

            var url = '/model/' + this.model_url + '/' + method,
                data = _.extend(
                    {id: this.get('id')},
                    options.data ? options.data : {}
                );

            socket.send(url, data, function (data) {
                if (!data.done) {
                    return;
                }

                this.set(data.data);

                if (options.success) {
                    options.success(data.data, data);
                }
            }.bind(this));
        }
    });
});