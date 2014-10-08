define('system/template', function () {
    'use strict';

    var sources = {};

    if (env === 'production') {
        requirejs(['tpls'], function (tpls) {
            sources = tpls;
        });
    }

    function getSource(tpl, data) {
        var source;

        if (sources[tpl]) {
            if (data) {
                return (new Ractive({
                   template: sources[tpl],
                   data: data
                })).toHTML();
            }

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

        if (data) {
            return (new Ractive({
               template: sources[tpl],
               data: data
            })).toHTML();
        }

        return sources[tpl];
    }

    return getSource;
});