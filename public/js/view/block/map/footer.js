define('view/block/map/footer', [
    'system/template'
], function(template) {
    'use strict';

    return Backbone.View.extend({
        initialize: function (holder) {
            this.holder = holder;
        },
        template: template('block/map/footer'),
        render: function () {
            this.holder.append(this.template);
        }
    });
});