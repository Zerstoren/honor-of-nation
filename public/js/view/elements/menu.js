define('view/elements/menu', [], function () {
    return AbstractView.extend({
        events: {
            "click ul li": "onClick"
        },

        render: function (holder) {
            this.$el.html(this.getTemplate('elements/menu'));
            holder.append(this.$el);
        },

        onClick: function (e) {
            this.trigger('onMenuClick', $(e.target).attr('action'));
        }
    });
});