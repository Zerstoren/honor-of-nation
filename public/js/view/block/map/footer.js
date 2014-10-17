define('view/block/map/footer', [
    'service/standalone/map',
    'model/dummy'
], function(
    map,
    ModelDummy
) {
    'use strict';

    return AbstractView.extend({
        initialize: function (holder) {
            this.holder = holder;
            this.template = this.getTemplate('block/map/footer');
            this.data.footer = new ModelDummy({
                x: '-',
                y: '-'
            });

            this.initRactive();
        },

        render: function () {
            this.holder.append(this.$el);
            map.on('mouseMove', this.onMouseMove, this);
        },

        onMouseMove: function (coordinate) {
            this.data.footer.set('x', coordinate[0]);
            this.data.footer.set('y', coordinate[1]);
        }
    });
});