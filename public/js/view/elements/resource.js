define('view/elements/resource', [], function () {
    return AbstractView.extend({
        events: {
            "mouseenter .resources > div": "onShowHint",
            "mouseout .resources > div": "onHideHint"
        },
        currentTooltip: null,

        initialize: function () {
            this.template = this.getTemplate('elements/resource');
            this.initRactive();
        },

        data: {},

        render: function (holder) {
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
