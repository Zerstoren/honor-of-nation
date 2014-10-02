define('view/elements/resource', [
    'view/elements/tooltip'
], function (ViewElementsTooltip) {
    return AbstractView.extend({
        events: {},

        initialize: function () {
            this.tooltipManager = new ViewElementsTooltip(this, '.resources > div');
            this.template = this.getTemplate('elements/resource');
            this.initRactive();
        },

        render: function (holder) {
            holder.append(this.$el);
        },

        setUserResources: function (domain) {
            this.set('resources', domain);
        }
    });
});
