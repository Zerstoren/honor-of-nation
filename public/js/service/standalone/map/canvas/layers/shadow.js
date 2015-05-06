define('service/standalone/map/canvas/layers/shadow', [
    'service/standalone/map/canvas/layers/abstract',
    'system/imageLoader'
], function (
    AbstractLayer,
    imageLoader
) {
    return atom.declare(AbstractLayer, {
        renderTo: function (ctx) {
            var point, ctx2d,
                i,
                cell;

            ctx2d = ctx.ctx2d;

            console.time('shadow');

            cell = imageLoader.get('shadow');

            for (i = 0; i < this.mapItems.length; i++) {
                point = this.mapItems[i];
                if (!point.shadow) {
                    continue;
                }

                ctx2d.drawImage(cell, point.x, point.y + 32);
            }

            console.timeEnd('shadow');
        }
    });

});