define('service/standalone/map/canvas/layers/cursor', [
    'service/standalone/map/canvas/layers/abstract',
    'system/imageLoader'
], function (
    AbstractLayer,
    imageLoader
) {
    return atom.declare(AbstractLayer, {
        cursor: {x: -1, y: -1},
        updateCursor: false,
        blockDraw: false,

        configure: function method () {
            this.image = imageLoader.get('cursor');
            this.shape = new LibCanvas.Shapes.Polygon([[0, 0], [0, 0], [0, 0], [0, 0]]);
            this.newShape = this.shape.clone();
            this.shift = new LibCanvas.Point(0, -32);
            method.previous.call(this);

            this.controller.on('mouseMove', this.setCursor, this);
            this.controller.on('mouseDown', this.stopDrawCursor, this);
            this.controller.on('mouseUp', this.restoreDrawCursor, this);

        },

        setCursor: function (ev) {
            if (this.cursor.x !== ev.position.x || this.cursor.y !== ev.position.y) {
                this.cursor.x = ev.position.x;
                this.cursor.y = ev.position.y;

                this.update();
            }
        },

        stopDrawCursor: function () {
            this.blockDraw = true;
            this.update();
        },

        restoreDrawCursor: function () {
            this.blockDraw = false;
            this.update();
        },

        update: function () {
            this.updateCursor = true;
        },

        onUpdate: function () {
            if (this.updateCursor === false) {
                return false;
            }

            if (this.blockDraw === true) {
                this.newShape = new LibCanvas.Shapes.Polygon([[0, 0], [0, 0], [0, 0], [0, 0]]);
            } else {
                this.newShape = new LibCanvas.Shapes.Polygon(
                    this._getArea(this.cursor.x, this.cursor.y, this.image, this.shift)
                );
            }

            this.updateCursor = false;
            this.redraw();
            return true;
        },

        renderTo: function (ctx) {
            var ctx2d = ctx.ctx2d;

            if (this.blockDraw === false) {
                ctx2d.drawImage(
                    this.image,
                    this.newShape.points[0].x,
                    this.newShape.points[0].y
                );
            }

            this.shape = this.newShape;
        },

        clearPrevious: function (ctx) {
            LibCanvas.App.Element.prototype.clearPrevious.apply(this, [ctx]);
        }
    });
});
