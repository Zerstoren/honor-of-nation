define('libs/abstract/service', [], function () {
    window.AbstractService = function () {
        this.initialize.apply(this, arguments);
    };
    _.extend(window.AbstractService.prototype, Backbone.Events, {
        initialize: function () {
            this._traverseEvents = {};
        },

        traverseEvent: function (eventName, fromView) {
            var traverseFn = function () {
                var args = Array.prototype.slice.call(arguments);
                this.trigger.apply(this, _.union([eventName], args));
            };

            fromView.on(eventName, traverseFn, this);

            return function () {
                fromView.off(eventName, traverseFn, this);
            };
        }
    });

    window.AbstractService.extend = Backbone.Model.extend;
});