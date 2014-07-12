define('view/elements/resource', [
    'system/template'
], function (template) {
    return Backbone.View.extend({
        events: {
            "mouseenter .resources > div": "onShowHint",
            "mouseout .resources > div": "onHideHint"
        },
        currentTooltip: null,

        render: function (holder) {
            this.$el.html(template('elements/resource'));
            holder.append(this.$el);
        },

        onShowHint: function (e) {
            this.tooltip = jQuery(e.target);
            this.tooltip.tooltip({
                trigger: '',
                title: this.tooltip.data('hint'),
                placement: 'right',
                container: 'body'
            });

            this.tooltip.tooltip('show');
        },

        onHideHint: function (e) {
            this.tooltip.tooltip('destroy');
        }
    });
});
