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
            this.$el.html(this.template);
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