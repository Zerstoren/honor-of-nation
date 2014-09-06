define('view/block/map/body', [], function() {
    'use strict';

    return AbstractView.extend({
        holderEl: null,

        initialize: function (holder) {
            this.holder = holder;
        },

        render: function () {
            this.$el.html(this.getTemplate('block/map/body'));
            this.holder.append(this.$el);
        },

        getHolder: function () {
            if (this.holderEl === null) {
                this.holderEl = jQuery('#map-body-holder');
            }

            return this.holderEl;
        }
    });
});