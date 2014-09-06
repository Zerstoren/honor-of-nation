define('view/block/no/body', [], function() {
    'use strict';

    return AbstractView.extend({
        holderEl: null,

        initialize: function (holder) {
            this.holder = holder;
        },

        render: function () {
            this.holder.append(this.getTemplate('block/no/body'));
        },

        getHolder: function () {
            if (this.holderEl === null) {
                this.holderEl = jQuery('#main-holder');
            }

            return this.holderEl;
        }
    });
});