define('service/standalone/map/canvas/mapLayer', [

], function (
) {
    return atom.declare(LibCanvas.App.Element, {
        mapItems: [],
        shape: null,

        configure: function () {
            this.projection = this.settings.get('projection');
            this.size       = this.settings.get('size');
            this.canvasSize = this.settings.get('canvasSize');
            this.camera     = this.settings.get('camera');

            this.polygons = [];

            this
                .createPolygons()
                .createShape();
        },

        createShape: function () {
            var s = this.size;

            this.shape = new LibCanvas.Shapes.Polygon([
                [ 0, 0 ],
                [ s.x, 0 ],
                [ s.x, s.y ],
                [ 0, s.y ]
            ].map(this.projection.toIsometric));

            return this;
        },

        createPolygons: function () {
            var x, y, newPoint,
                mapWidth = this.canvasSize.width,
                mapHeight = this.canvasSize.height,
                s = this.size;

            atom.array.empty(this.polygons);

            for (y = 0; y < s.y; y++) for (x = s.x - 1; x >= 0; x--) {
                newPoint = this.createPoint(x, y);
                if (
                    newPoint.x < -128 || newPoint.x > mapWidth ||
                    newPoint.y < -128 || newPoint.y > mapHeight
                ) {
                    continue;
                }

                this.mapItems.push( newPoint );
            }

            return this;
        },

        createPoint: function (x, y) {
            var point = new LibCanvas.Point3D(x, y, 1);
            var newPoint = this.projection.toIsometric(point);
            newPoint.xp = x;
            newPoint.yp = y;
            return newPoint;
        },

        hasPoint: function (coord) {
            var size = this.size,
                x = Math.ceil(coord.x),
                y = Math.ceil(coord.y);

            return x >= 0 && x < size.x
                && y >= 0 && y < size.y;
        },

        to3D: function (coord, z) {
            var result = this.projection.to3D( LibCanvas.Point( coord ), z );

            result.x = Math.floor(result.x);
            result.y = Math.floor(result.y);

            return this.hasPoint(result) ? result : null;
        },

        clearPrevious: function(){},

        renderTo: function (ctx) {
            var point,
                i = 0,
                cell;

            ctx2d = ctx.ctx2d;

            cell = preloader.get('item1');

            console.time('draw');

            for (i = 0; i < this.mapItems.length; i++) {
                point = this.mapItems[i];

                ctx2d.drawImage(cell, point.x, point.y + 32);

//                if ((point.xp + this.camera.x) % 10 === 0 || (point.yp + this.camera.y) % 10 === 0) {
//                    ctx.text({
//                        text: (point.xp + this.camera.x) + '-' + (point.yp + this.camera.y),
//                        color: '#f00',
//                        to: [point.x + 50, point.y + 48, point.x + 128, point.y + 256]
//                    });
//                }

            }

            console.timeEnd('draw');
        }
    });

});