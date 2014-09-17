define('system/template', function () {
    'use strict';

    var sources = {},
        compiles = {};

    function getSource(tpl) {
        var source;

        if (sources[tpl]) {
            return sources[tpl];
        }

        jQuery.ajax({
            url: '/js/tpl/' + tpl + '.tpl',
            async: false,
            success: function (data) {
                source = data;
            },
            error: function () {
                throw new Error('Not found ' + tpl);
            }
        });

        sources[tpl] = source;

        return sources[tpl];
    }

    return getSource;
});