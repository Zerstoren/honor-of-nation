define('view/test', [
    'system/template'
], function(
    template
) {
    'use strict';

    return Backbone.View.extend({
        template: template('test'),

        events: {
            'click div.name': "open"
        },

        open: function(e) {
            console.log(1, e.target);
        },

        render: function() {
            this.$el.append(this.template);
            jQuery('body').html(this.$el);
        }
    });
});
