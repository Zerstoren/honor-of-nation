define('view/elements/popup', [], function () {
    var hideTimer = -1,
        showTimer = -1,
        showLayer = null;

    return AbstractView.extend({
        initialize: function (triggerElement, config) {
            if (!config) {
                config = {};
            }

            this.$config = {
                target: config.target || '.popup',
                timeout: config.timeout || 500,
                callback: config.popupCallback || false
            };

            this.element = triggerElement;
            this.addEventListener();
        },

        addEventListener: function () {
            var self = this;

            this.element.on('mouseenter', function(e) {
                self.startShowTimeout(e);
            });

            this.element.on('mouseleave', function(e) {
                self.stopShowTimeout(e);
            });
        },

        showLayer: function () {
            var offset;

            showLayer = this;
            this.popup.css({display: 'block'});
            offset = this.target.offset();

            this.popup.css({
                top: offset.top,
                left: offset.left + this.target.width()
            });
        },

        hideLayer: function() {
            showLayer = null;
            this.popup.css({display: 'none'});
            this.setPopup();
        },

        startShowTimeout: function (e) {
            var self = this;

//            if (hideTimer !== -1 && self === showLayer) {
//                clearTimeout(hideTimer);
//                hideTimer = -1;
//                return;
//            }

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
                this.target = jQuery(e.target);
                this.popup = this.target.find(this.$config.target);
            } else {
                this.target = null;
                this.popup = null;
            }
        }
    });
});
