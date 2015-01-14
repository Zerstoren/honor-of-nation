define('view/elements/popover', [], function () {

    return AbstractView.extend({
        PLACE_TOP: 'top',
        PLACE_LEFT: 'left',
        PLACE_RIGHT: 'right',
        PLACE_BOTTOM: 'bottom',

        initialize: function (view, targetElement, config) {
            this.popover = null;

            if (!config) {
                config = {};
            }

            this.$config = {
                content: config.content || '.popover',
                placement: config.placement || 'top',
                container: 'body',
                title: config.title || ''
            };

            this.targetElement = targetElement;
            this.element = view.find(targetElement);
            var options = {
                html: true,
                content: this.element.find(this.$config.content).children('*').clone(),
                template: this.$config.template,
                placement: this.$config.placement,
                title: this.$config.title
            };

            this.element.popover(options);

            this.onHide = function (e) {
                var target = jQuery(e.target);

                if (target.hasClass('popover')) {
                    return;
                }

                if (target.parents('.popover').length) {
                    return;
                }

                if (target.is(this.targetElement) && target.find('.popover').length) {
                    return;
                }

                this.hide();
            }.bind(this);

            this.addEventListener();
        },

        addEventListener: function () {
            jQuery(document).on('click', this.onHide);
        },

        showPopover: null,
        onHide: null,

        show: function () {
            this.element.popover('show');
        },

        hide: function () {
            this.element.popover('hide');
        },

        destroy: function () {
            jQuery(document).off('click', this.onHide);
            this.element.popover('destroy');
        }
    });
});
