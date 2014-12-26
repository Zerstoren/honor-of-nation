define('view/elements/popup', [], function () {
    var hideTimer = -1,
        showTimer = -1,
        showLayer = null;

    return AbstractView.extend({
        initialize: function (triggerElement, config) {
            this.$fnCallback = {};
            if (!config) {
                config = {};
            }

            this.$config = {
                liveTarget: config.liveTarget || false,
                target: config.target || '.popup',
                timeout: config.timeout || 500,
                ignoreTop: config.ignoreTop || false,
                callback: config.popupCallback || false,
                align: config.align || 'right'
            };

            this.element = triggerElement;
            this.addEventListener();
        },

        destroy: function () {
            this.removeEventListener();
        },

        addEventListener: function () {
            var self = this;

            if (this.$config.liveTarget) {
                this.$fnCallback.mouseenter = function(e) {
                    self.startShowTimeout(e);
                };

                this.$fnCallback.mouseleave = function(e) {
                    self.stopShowTimeout(e);
                };

                this.element.on('mouseenter', this.$config.liveTarget, this.$fnCallback.mouseenter);
                this.element.on('mouseleave', this.$config.liveTarget, this.$fnCallback.mouseleave);
            } else {
                this.$fnCallback.mouseenter = function(e) {
                    self.startShowTimeout(e);
                };

                this.$fnCallback.mouseleave = function(e) {
                    self.stopShowTimeout(e);
                };

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
            var offset, config;

            showLayer = this;
            this.popup.css({display: 'block'});
            offset = this.target.offset();

            if (this.$config.align === 'right') {
                left = offset.left + this.target.width()
            } else {
                left = offset.left - this.popup[0].getBoundingClientRect().width
            }

            config = {
                top: offset.top,
                left: left
            };

            if (this.$config.ignoreTop) {
                delete config.top;
            }

            this.popup.css(config);
        },

        hideLayer: function() {
            showLayer = null;
            this.popup.css({display: 'none'});
            this.setPopup();
        },

        startShowTimeout: function (e) {
            var self = this;

            if (hideTimer !== -1 && showLayer !== null) {
                clearTimeout(hideTimer);
                hideTimer = -1;
                showLayer.hideLayer();
                this.setPopup(e);
                this.showLayer();
                return;
            }

            if (showTimer === -1 && showLayer !== null) {
                showLayer.hideLayer();
                this.setPopup(e);
                this.showLayer();
                return;
            }

            showTimer = setTimeout(function() {
                self.setPopup(e);
                self.showLayer();
                showTimer = -1;
            }, this.$config.timeout);
        },

        stopShowTimeout: function (e) {
            var self = this;

            if(showTimer !== -1) {
                clearTimeout(showTimer);
                showTimer = -1;
            } else {
                hideTimer = setTimeout(function() {
                    hideTimer = -1;
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
