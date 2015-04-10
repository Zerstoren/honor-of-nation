define('service/standalone/map/canvas/layers/unit', [
    'service/standalone/map/canvas/layers/abstract'
], function (
    AbstractLayer
) {
    return atom.declare(AbstractLayer, {
        renderTo: function (ctx) {
            var point, ctx2d,
                i,
                cell;

            ctx2d = ctx.ctx2d;

//            console.time('shadow');
//
//            console.timeEnd('shadow');
        }
    });

});
