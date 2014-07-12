define('libs/abstract/gateway', ['system/socket'], function (socket) {

    window.AbstractGateway = function () {
        this.initialize.apply(this, arguments);
    };

    _.extend(window.AbstractGateway.prototype, Backbone.Events, {
        socket: socket,
        initialize: function () {

        }
    });

    window.AbstractGateway.extend = Backbone.Model.extend;
});