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

            //cell = imageLoader.get('ground-2-1');

            for (i = 0; i < this.mapItems.length; i++) {
                point = this.mapItems[i];
                if (!point.ground) {
                    continue;
                }

                ctx2d.drawImage(point.ground, point.x, point.y + 32);

//                if ((point.xp + this.camera.x) % 10 === 0 || (point.yp + this.camera.y) % 10 === 0) {
//                    ctx.text({
//                        text: (point.xp + this.camera.x) + '-' + (point.yp + this.camera.y),
//                        color: '#f00',
//                        to: [point.x + 50, point.y + 48, point.x + 128, point.y + 256]
//                    });
//                }

            }

            console.timeEnd('ground');
        }
    });

});