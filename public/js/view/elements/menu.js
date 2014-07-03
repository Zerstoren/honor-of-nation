define('view/elements/menu', [
    'system/template'
], function (
    template
) {
    return Backbone.View.extend({
        events: {
            "click ul li": "onClick"
        },

        render: function (holder) {
            this.$el.html(template('elements/menu'));
            holder.append(this.$el);
        },

        onClick: function (e) {
            this.trigger('onMenuClick', $(e.target).attr('action'));
        }
    });
});