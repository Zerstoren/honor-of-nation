define('service/standalone/map/objects/abstract', [], function () {
    return AbstractService.extend({
        setStyleForBox: function (ctx, type) {
            var drawColor;

            if (type === 1) {
                drawColor = 'rgba(240, 240, 240, 0.9)'
            } else {
                drawColor = 'rgba(240, 240, 240, 0.9)'
            }

            ctx.set({
                fillStyle: drawColor,
                strokeStyle: 'rgba(30, 30, 30, 1)'
            });
        },

        drawBox: function (text, point, ctx) {
            var textBox = new LibCanvas.Shapes.Rectangle({
                center: new LibCanvas.Point(point.x + 64, point.y + 90),
                size  : new LibCanvas.Size(158, 30)
            });

            ctx.fill(textBox);
            ctx.stroke(textBox);

            ctx.text({
                text: text,
                family: 'Calibry',
                align: 'center',
                size: 12,
                padding: [-2, 10],
                to: textBox,
                color: 'black'
            });
        }
    });
});