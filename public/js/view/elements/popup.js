define('view/elements/popup', [], function () {
    var hideTimer = {},
        showTimer = {},
        showLayer = {};

    return AbstractView.extend({
        initialize: function (triggerElement, config) {
            this.$fnCallback = {};
            if (!config) {
                config = {};
            }

            this.$config = {
                namespace: config.namespace || 'default',
                liveTarget: config.liveTarget || false,
                target: config.target || '.popup',
                timeout: config.timeout || 500,
                ignoreTop: config.ignoreTop || false,
                callback: config.popupCallback || false,
                align: config.align || 'right', // left, center, right
                valign: config.valign || 'bottom' // bottom, middle, top
            };

            hideTimer[this.$config.namespace] = -1;
            showTimer[this.$config.namespace] = -1;
            showLayer[this.$config.namespace] = null;

            this.element = triggerElement;
            this.addEventListener();
        },

        destroy: function () {
            this.removeEventListener();
        },

        addEventListener: function () {
            var self = this;

            this.$fnCallback.mouseenter = function(e) {
                self.startShowTimeout(e);
            };

            this.$fnCallback.mouseleave = function(e) {
                self.stopShowTimeout(e);
            };

            if (this.$config.liveTarget) {
                this.element.on('mouseenter', this.$config.liveTarget, this.$fnCallback.mouseenter);
                this.element.on('mouseleave', this.$config.liveTarget, this.$fnCallback.mouseleave);
            } else {
                this.element.on('mouseenter', this.$fnCallback.mouseenter);
                this.element.on('mouseleave', this.$fnCallback.mouseleave);
            }
        },

        removeEventListener: function () {
            if (this.$config.liveTarget) {
                this.element.off('mouseenter', this.$config.liveTarget, this.$fnCallback.mouseenter);
                this.element.off('mouseleave', this.$config.liveTarget, this.$fnCallback.mouseleave);
            } else {
                this.element.off('mouseenter', this.$fnCallback.mouseenter);
                this.element.off('mouseleave', this.$fnCallback.mouseleave);
            }
        },

        showLayer: function () {
            if (!this.popup) {
                return;
            }

            var config, left, top, popupBR, targetBR;
            showLayer[this.$config.namespace] = this;
            this.popup.css({display: 'block'});

            popupBR = this.popup[0].getBoundingClientRect();
            targetBR = this.target[0].getBoundingClientRect();

            top = targetBR.top;

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
            if (!this.popup) {
                return;
            }

            showLayer[this.$config.namespace] = null;
            this.popup.css({display: 'none'});
            this.setPopup();
        },

        startShowTimeout: function (e) {
            var self = this;

            if (hideTimer[this.$config.namespace] !== -1 && showLayer[this.$config.namespace] !== null) {
                clearTimeout(hideTimer[this.$config.namespace]);
                hideTimer[this.$config.namespace] = -1;
                showLayer[this.$config.namespace].hideLayer();
                this.setPopup(e);
                this.showLayer();
                return;
            }

            if (showTimer[this.$config.namespace] === -1 && showLayer[this.$config.namespace] !== null) {
                showLayer[this.$config.namespace].hideLayer();
                this.setPopup(e);
                this.showLayer();
                return;
            }

            showTimer[this.$config.namespace] = setTimeout(function() {
                self.setPopup(e);
                self.showLayer();
                showTimer[self.$config.namespace] = -1;
            }, this.$config.timeout);
        },

        stopShowTimeout: function () {
            var self = this;
            if(showTimer[this.$config.namespace] !== -1) {
                clearTimeout(showTimer[this.$config.namespace]);
                showTimer[this.$config.namespace] = -1;
            } else {
                hideTimer[this.$config.namespace] = setTimeout(function() {
                    hideTimer[self.$config.namespace] = -1;
                    self.hideLayer();
                }, this.$config.timeout);
            }
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
