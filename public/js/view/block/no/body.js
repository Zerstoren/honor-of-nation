define('view/block/no/body', [], function() {
    'use strict';

    return AbstractView.extend({
        holder: null,

        initialize: function (holder) {
            this.holder = holder;
        },

        render: function () {
            this.holder.append(this.getTemplate('block/no/body'));
        },

        getHolder: function () {
            if (this.holder === null) {
                this.holder = jQuery('#main-holder');
            }

            return this.holder;
        }
    });
});