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
                this.trigger.apply(this, [eventName]);
            }.bind(this);

            fromView.on(eventName, traverseFn, this);

            return function () {
                fromView.un(eventName, traverseFn, this);
            }
        }
    });

    window.AbstractService.extend = Backbone.Model.extend;
});