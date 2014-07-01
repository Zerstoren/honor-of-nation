define('view/elements/menu', [
    'system/template'
], function (
    template
) {
    return Backbone.View.extend({
        events: {
            "click ul li": "onClick"
        },

        initialize: function () {
            this.$el.html(template('elements/menu'));
        },

        render: function (holder) {
            holder.append(this.$el);
            this.delegateEvents();
        },

        onClick: function (e) {
            this.trigger('onMenuClick', $(e.target).attr('action'));
        }
    });
});