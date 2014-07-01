define('view/block/map/body', [
    'system/template'
], function(template) {
    'use strict';

    return Backbone.View.extend({
        template: template('block/map/body'),
        holderEl: null,

        initialize: function (holder) {
            this.holder = holder;
        },

        render: function () {
            this.holder.append(this.template);
        },

        getHolder: function () {
            if (this.holderEl === null) {
                this.holderEl = jQuery('#main-holder');
            }

            return this.holderEl;
        }
    });
});