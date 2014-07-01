define('system/template', function () {
    'use strict';

    var sources = {},
        compiles = {};

    function getSource(tpl) {
        var source;

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

    function compileTemplate(tpl) {
        if (compiles[tpl] === undefined) {
            compiles[tpl] = Handlebars.compile(getSource(tpl));
        }

        return compiles[tpl];
    }


    function getTemplate(tpl, data) {
        return compileTemplate(tpl)(data);
    }

    return getTemplate;
});