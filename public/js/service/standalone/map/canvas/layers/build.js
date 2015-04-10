define('service/standalone/map/canvas/layers/build', [
    'service/standalone/map/canvas/layers/abstract'
], function (
    AbstractLayer
) {
    return atom.declare(AbstractLayer, {
        renderTo: function (ctx) {
            var point, build,
                i,
                cell;

            console.time('build');
            for (i = 0; i < this.mapItems.length; i++) {
                point = this.mapItems[i];
                build = point.build;

                if (!build) {
                    continue;
                }

                build(point, ctx);
            }
            console.timeEnd('build');
        }
    });

});