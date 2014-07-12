define('libs/abstract/service', [], function () {
    window.AbstractService = function () {
        this.initialize.apply(this, arguments);
    };
    _.extend(window.AbstractService.prototype, Backbone.Events, {
        initialize: function () {

        }
    });

    window.AbstractService.extend = Backbone.Model.extend;
});