define('gateway/abstract', [
    'system/socket'
], function (socket) {
    var Abstract = function () {

    };

    Abstract.prototype.socket = socket;

    _.extend(Abstract.prototype, Backbone.Events);

    return Abstract;
});