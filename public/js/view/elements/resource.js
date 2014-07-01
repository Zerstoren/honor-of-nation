define('view/elements/resource', [
    'system/template'
], function (template) {
    return Backbone.View.extend({
        events: {
            "mouseenter .resources > div": "onShowHint",
            "mouseout .resources > div": "onHideHint"
        },
        currentTooltip: null,

        initialize: function () {
            this.$el.html(template('elements/resource'));
        },

        render: function (holder) {
            holder.append(this.$el);
            this.delegateEvents();
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
