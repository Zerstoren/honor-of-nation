define('view/elements/popover', [], function () {
    return AbstractView.extend({
        initialize: function (triggerElement, config) {
            this.$fnCallback = {};
            if (!config) {
                config = {};
            }

            this.enabled = true;
            this.document = jQuery(document.body);
            this.$config = {
                namespace: config.namespace || 'default',
                liveTarget: config.liveTarget || false,
                target: config.target || '.popover',
                timeout: config.timeout || 500,
                ignoreTop: config.ignoreTop || false,
                callback: config.popupCallback || false,
                manual: config.manual || false,
                align: config.align || 'right', // left, center, right
                valign: config.valign || 'default' // bottom, middle, top, default
            };

            this.element = triggerElement;

            this.$fnCallback.click = this.showLayer.bind(this);
            this.$fnCallback.hide = function (e) {
                var target = jQuery(e.target);
                if (target.is(this.$config.target) || target.parents(this.$config.target).length) {
                    return;
                }

                this.hideLayer();
            }.bind(this);

            if (!this.$config.manual) {
                this.addEventListener();
            }
        },

        enable: function () {
            this.enabled = true;
        },

        disable: function() {
            this.enabled = false;
            this.hideLayer();
        },

        destroy: function () {
            this.removeEventListener();
        },

        addEventListener: function () {
            this.element.on('click', this.$config.liveTarget, this.$fnCallback.click);
        },

        removeEventListener: function () {
            this.element.off('click', this.$config.liveTarget, this.$fnCallback.click);
        },

        showLayer: function (e) {
            if (!this.enabled) {
                return;
            }

            if (this.popup) {
                this.$fnCallback.hide(e);
                return;
            }

            setTimeout(function () {
                this.document.bind('click.popover', this.$fnCallback.hide);
            }.bind(this), 0);

            this.setPopup(e);

            var config, left, top, popupBR, targetBR;
            this.popup.css({display: 'block'});
            this.recalculatePosition();
            this.trigger('show');
        },

        recalculatePosition: function () {
            var config;
            var popupBR = this.popup[0].getBoundingClientRect();
            var targetBR = this.target[0].getBoundingClientRect();

            var top = targetBR.top;
            var left;

            if (this.$config.valign === 'top') {
                top = targetBR.top - popupBR.height;
            } else if (this.$config.valign === 'bottom') {
                top = targetBR.top + targetBR.width;
            } else if (this.$config.valign === 'middle') {
                top = (targetBR.top + parseInt(targetBR.height / 2)) - parseInt(popupBR.height / 2);
            }

            if (this.$config.align === 'right') {
                left = targetBR.left + targetBR.width;
            } else if (this.$config.align === 'left') {
                left = targetBR.left - popupBR.width;
            } else if (this.$config.align === 'center') {
                // (target left + (target width / 2)) - popup width / 2
                left = (targetBR.left + parseInt(targetBR.width / 2)) - parseInt(popupBR.width / 2);
            }

            if ((top + popupBR.height) > window.innerHeight) {
                top = window.innerHeight - popupBR.height;
            } else if (top < 0) {
                top = 0;
            }

            if ((left + popupBR.width) > window.innerWidth) {
                left = window.innerWidth - popupBR.width;
            } else if (left < 0) {
                left = 0;
            }

            config = {
                top: top,
                left: left
            };

            if (this.$config.ignoreTop) {
                delete config.top;
            }

            this.popup.css(config);
        },

        hideLayer: function() {
            this.document.unbind('click.popover');

            if (!this.popup) {
                return;
            }

            this.popup.css({display: 'none'});
            this.setPopup();
            this.trigger('hide');
        },

        setPopup: function (e) {
            if (e) {
                this.target = jQuery(e.currentTarget);
                this.popup = this.target.find(this.$config.target);
            } else {
                this.target = null;
                this.popup = null;
            }
        }
    });
});
