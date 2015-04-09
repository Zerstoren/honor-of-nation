define('service/standalone/map/canvas/controller', [
    'service/standalone/map/canvas/mapLayer',
    'service/standalone/map/canvas/support'
], function (
    MapLayer,
    support
) {
    return AbstractService.extend({
        initialize: function () {
            this.currentCameraLocation = new LibCanvas.Point(10, 10);
            this.cellWidth = 128;
            this.cellHeight = 64;
            this.canvasSize = new LibCanvas.Size(window.innerWidth * 2, window.innerHeight * 2);
            this.mapSize = this.calculateAppSize();

            this.app = new LibCanvas.App({
                size: new LibCanvas.Size(this.canvasSize.width, this.canvasSize.height),
                appendTo: 'body',
            });

            this.mapLayer = this.app.createLayer({
                name: 'map',
                intersection: 'manual'
            });

            this.mouse = new LibCanvas.Mouse(this.app.container.bounds);
            this.map = new MapLayer(this.mapLayer, {
                projection: new LibCanvas.Engines.Isometric.Projection({
                    factor: [ 1, 0.5, 1 ],
                    start : new LibCanvas.Point(
                        (this.canvasSize.width / 2) - (this.mapSize.width * this.cellWidth / 2),
                        (this.canvasSize.height / 2)
                    ),
                    size  : 64
                }),
                camera: this.currentCameraLocation,
                size: new LibCanvas.Point(this.mapSize.width, this.mapSize.height),
                canvasSize: this.canvasSize
            });

            this.addMouseControl();
            this.initDragger();
            this.shiftToCenter();
        },

        initDragger: function () {
            this.move = null;
            this.shift = new support.CustomLayerShift(this.mapLayer);
            this.shift.setLimitCallback(this.onMapEdge.bind(this));

            this.updateShiftLimit();

            this.dragger = new support.CustomDragger( this.mouse )
                .addLayerShift( this.shift )
                .start(function (e) {
                    return e.button == 0 || e.type == "touchstart";
                }.bind(this));
        },

        onMapEdge: function (edge) {
            var mapUpdate = false,
                moveSize = 4,
                newShift = new LibCanvas.Point(0, 0),
                newCameraPosition = new LibCanvas.Point(0, 0);

            if (edge.leftEdge || edge.rightEdge) {
                if (edge.leftEdge) {
                    newShift.move([
                        this.cellWidth * moveSize / -1,
                        0
                    ]);

                    newCameraPosition.move([-moveSize, -moveSize]);
                    mapUpdate = true;
                } else {
                    newShift.move([
                        this.cellWidth * moveSize,
                        0
                    ]);
                    newCameraPosition.move([moveSize, moveSize]);
                    mapUpdate = true;
                }
            }

            if(edge.topEdge || edge.bottomEdge) {
                if (edge.topEdge) {
                    newShift.move([
                        0,
                        this.cellHeight * moveSize / -1
                    ]);
                    newCameraPosition.move([moveSize, moveSize / -1]);
                    mapUpdate = true;
                } else {
                    newShift.move([
                        0,
                        this.cellHeight * moveSize
                    ]);
                    newCameraPosition.move([moveSize / -1, moveSize]);
                    mapUpdate = true;
                }
            }

            if (mapUpdate) {
                this.mapLayer.redrawAll(function () {
                    this.shift.addShift(newShift);
                    this.currentCameraLocation.move(newCameraPosition)
                }.bind(this));
            }
        },

        updateShiftLimit: function () {
            this.shift.setLimitShift(
                new LibCanvas.Shapes.Rectangle(
                    new LibCanvas.Point(this.canvasSize.width / 2 / -1, this.canvasSize.height / 2 / -1),
                    new LibCanvas.Point(0, 0)
                )
            );
        },

        shiftToCenter: function () {
            var mapSize = this.app.settings.get('size').clone();
            var mapRectange = new LibCanvas.Shapes.Rectangle({
                from: new LibCanvas.Point(0, 0),
                size: mapSize
            });

            var leftShift = Math.floor(mapRectange.center.x - (window.innerWidth / 2));
            var rightShift = Math.floor(mapRectange.center.y - (window.innerHeight / 2));

            this.shift.setShift([leftShift / -1, rightShift / -1], false);
        },

        centerCameraToPosition: function(position) {
            this.shiftToCenter();
            position = new LibCanvas.Point(position);
            this.currentCameraLocation.set(
                position.x - (this.mapSize.width / 2),
                position.y - (this.mapSize.height / 2)
            );
            this.shift.addShift([-64, 0]);

            this.mapLayer.redrawAll();
        },

        addMouseControl: function () {
//            var mouse = this.mouse,
//                dataFn = function (e) {
//                    point = this.map.to3D([
//                            mouse.point.x - this.shift.getShift().x,
//                            mouse.point.y - this.shift.getShift().y
//                        ]
//                    );
//
//                    e.position = point;
//
//                    return e;
//                };
//
//            mouse.events.add({
//                click: function (e, mouse) {
//
//                }.bind(this)
//            });
//
        },

        calculateAppSize: function () {
            var matrixHeight, matrixWidth;

            matrixHeight = (this.canvasSize.width > this.canvasSize.height ? this.canvasSize.width : this.canvasSize.height) / 64;
            matrixWidth = (this.canvasSize.width > this.canvasSize.height ? this.canvasSize.width : this.canvasSize.height) / 64;

            return new LibCanvas.Size(Math.floor(matrixWidth), Math.floor(matrixHeight));
        }
    });
});