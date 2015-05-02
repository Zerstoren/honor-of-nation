define('service/standalone/map/canvas/layers/abstract', [], function () {
    return atom.declare(LibCanvas.App.Element, {

        configure: function () {
            this.shape = null;

            this.projection = this.settings.get('projection');
            this.size       = this.settings.get('size');
            this.mapItems   = this.settings.get('mapItems');

            this.createShape();
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

        clearPrevious: function(){}
    });
});