define('view/block/map/footer', [], function() {
    'use strict';

    return AbstractView.extend({
        initialize: function (holder) {
            this.holder = holder;
        },

        render: function () {
            this.holder.append(this.template('block/map/footer'));
        }
    });
});