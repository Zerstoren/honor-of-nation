define('view/elements/popover', [], function () {

    return AbstractView.extend({
        PLACE_TOP: 'top',
        PLACE_LEFT: 'left',
        PLACE_RIGHT: 'right',
        PLACE_BOTTOM: 'bottom',

        initialize: function (targetElement, config) {
            this.popover = null;

            if (!config) {
                config = {};
            }

            this.$config = {
                content: config.content || '',
                placement: config.placement || 'top',
                container: 'body',
//                template: config.template || '',
                title: config.title || ''
            };

            this.element = targetElement;
        },

        show: function () {
            var options = {
                html: true,
                content: this.$config.content,
                placement: this.$config.placement,
                template: this.$config.template,
                title: this.$config.title
            };

            this.element.popover(options);
            this.element.popover('show');
        },

        hide: function () {
            this.element.popover('hide');
        },

        destroy: function () {
            this.element.popover('destroy');
        }
    });
});
