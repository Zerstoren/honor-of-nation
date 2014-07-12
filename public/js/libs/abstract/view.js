define('libs/abstract/view', ['system/template'], function (template) {
    window.AbstractView = Backbone.View.extend({
        template: template
    });
});