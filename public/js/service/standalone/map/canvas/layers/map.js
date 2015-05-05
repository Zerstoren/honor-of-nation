define('service/standalone/map/canvas/layers/map', [
    'service/standalone/map/canvas/layers/abstract',
    'system/imageLoader'
], function (
    AbstractLayer,
    imageLoader
) {
    return atom.declare(AbstractLayer, {
        renderTo: function (ctx) {
            var point, ctx2d,
                i = 0,
                cell;

            ctx2d = ctx.ctx2d;

            console.time('ground');

            for (i = 0; i < this.mapItems.length; i++) {
                point = this.mapItems[i];
                if (!point.ground) {
                    continue;
                }

                ctx2d.drawImage(point.ground, point.x, point.y + 32);
            }

            console.timeEnd('ground');
        }
    });

});