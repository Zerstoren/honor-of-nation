define('service/abstract', [], function () {
    'use strict';

    var Abstract = function () {};
    _.extend(Abstract.prototype, Backbone.Events);

    return Abstract;
});