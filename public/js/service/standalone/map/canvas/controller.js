define('service/standalone/map/canvas/controller', [
    'service/standalone/map/canvas/layers/map',
    'service/standalone/map/canvas/layers/decor',
    'service/standalone/map/canvas/layers/build',
    'service/standalone/map/canvas/layers/shadow',
    'service/standalone/map/canvas/layers/unit',

    'service/standalone/map/canvas/support'
], function (
    MapLayer,
    DecorLayer,
    BuildLayer,
    ShadowLayer,
    UnitLayer,

    support
) {
    var MapItemPoint = atom.declare(LibCanvas.Point, {
        mapX   : null,
        mapY   : null,
        ground : null,
        decor  : null,
        shadow : false,
        build  : null,
        unit   : null,

        clearElements: function () {
            this.ground = null;
            this.decor  = null;
            this.shadow = false;
            this.build  = null;
            this.unit   = null;
        },

        setGround: function (img) {
            this.ground = img;
            return this;
        },

        setDecor: function (img, shift) {
            this.decor = {
                img: img,
                shift: shift
            };
            return this;
        },

        setShadow: function (bool) {
            this.shadow = bool;
            return this;
        },

        setBuild: function (fn) {
            this.build = fn;
            return this;
        },

        setUnit: function (fn) {
            this.unit = fn;
            return this;
        }
    });

    return AbstractService.extend({
        initialize: function () {
            this.mapItems = [];

            this.currentCameraLocation = new LibCanvas.Point(10, 10);
            this.cellWidth = 128;
            this.cellHeight = 64;
            this.canvasSize = new LibCanvas.Size(window.innerWidth * 2, window.innerHeight * 2);
            this.mapSize = this.calculateAppSize();
            this.size = new LibCanvas.Point(this.mapSize.width, this.mapSize.height)

            this.projection = new LibCanvas.Engines.Isometric.Projection({
                factor: [ 1, 0.5, 1 ],
                start : new LibCanvas.Point(
                    (this.canvasSize.width / 2) - (this.mapSize.width * this.cellWidth / 2),
                    (this.canvasSize.height / 2)
                ),
                size  : this.cellWidth / 2
            });

            this.createMapItems();

            this.initLayers();

            this.mouse = new LibCanvas.Mouse(this.app.container.bounds);

            this.addMouseControl();
            this.initDragger();
            this.shiftToCenter();

            this.redraw(true);
        },

        initLayers: function () {
            this.app = new LibCanvas.App({
                size: new LibCanvas.Size(this.canvasSize.width, this.canvasSize.height),
                appendTo: 'body'
            });

            this.mapLayer = this.app.createLayer({
                name: 'map',
                intersection: 'manual',
                zIndex: 1
            });

            this.mapLayer.stop();
            this.ground = new MapLayer(this.mapLayer, {
                projection: this.projection,
                size: this.size,
                mapItems: this.mapItems,
                zIndex: 1
            });

            this.decor = new DecorLayer(this.mapLayer, {
                projection: this.projection,
                size: this.size,
                mapItems: this.mapItems,
                zIndex: 2
            });

            this.build = new BuildLayer(this.mapLayer, {
                projection: this.projection,
                size: this.size,
                mapItems: this.mapItems,
                zIndex: 3
            });

            this.shadow = new ShadowLayer(this.mapLayer, {
                projection: this.projection,
                size: this.size,
                mapItems: this.mapItems,
                zIndex: 4
            });
            this.mapLayer.start();
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

        redraw: function (force) {
            var i, pos;
            if (!this.updateDataLayerCallback)
                return;

            if (force) console.time('sum');

            console.time('calculate');
            for (i = 0; i < this.mapItems.length; i++) {
                pos = this.mapItems[i];
                pos.clearElements();
                pos.mapX = pos.xp + this.currentCameraLocation.x;
                pos.mapY = pos.yp + this.currentCameraLocation.y;

                this.updateDataLayerCallback(pos);
            }
            console.timeEnd('calculate');

            if (force) {
                this.mapLayer.redrawForce();
            } else {
                this.mapLayer.redrawAll();
            }

            if (force) console.timeEnd('sum');
            console.log('Render complete');
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
                this.shift.addShift(newShift);
                this.currentCameraLocation.move(newCameraPosition);
                this.redraw(true);
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

        updateDataLayer: function (fn) {
            this.updateDataLayerCallback = fn;
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

            this.shift.addShift([this.cellWidth / 2 / -1, 0]);
            this.redraw(true);
        },

        addMouseControl: function () {
            var mouse = this.mouse,
                self = this,
                dataFn = function (e) {
                    var point = self.ground.to3D([
                            mouse.point.x - self.shift.getShift().x,
                            mouse.point.y - self.shift.getShift().y
                        ]
                    );

                    point.x += self.currentCameraLocation.x;
                    point.y += self.currentCameraLocation.y;

                    e.position = point;

                    return e;
                };

            mouse.events.add({
                click: function (e) {
                    if(e.which === 1) {
                        this.trigger('mouseClick', dataFn(e));
                    } else if(e.which === 3) {
                        this.trigger('mouseRightClick', dataFn(e));
                    } else if(e.which === 2) {
                        this.trigger('mouseMiddleClick', dataFn(e));
                    }
                }.bind(this),

                dblclick: function (e) {
                    this.trigger('mouseDoubleClick', dataFn(e));
                }.bind(this),

                move: function (e) {
                    this.trigger('mouseMove', dataFn(e));
                }.bind(this),

                down: function (e) {
                    this.trigger('mouseDown', dataFn(e));
                }.bind(this),

                up: function (e) {
                    this.trigger('mouseUp', dataFn(e));
                }.bind(this)
            });
        },

        calculateAppSize: function () {
            var matrixHeight, matrixWidth;

            matrixHeight = (this.canvasSize.width > this.canvasSize.height ? this.canvasSize.width : this.canvasSize.height) / 64;
            matrixWidth = (this.canvasSize.width > this.canvasSize.height ? this.canvasSize.width : this.canvasSize.height) / 64;

            return new LibCanvas.Size(Math.floor(matrixWidth), Math.floor(matrixHeight));
        },

        createMapItems: function () {
            var x, y, newPoint,
                mapWidth = this.canvasSize.width,
                mapHeight = this.canvasSize.height,
                s = new LibCanvas.Point(this.mapSize.width, this.mapSize.height);

            atom.array.empty(this.mapItems);

            for (y = 0; y < s.y; y++) {
                for (x = s.x - 1; x >= 0; x--) {
                    newPoint = this.createPoint(x, y);
                    if (
                        newPoint.x < -128 || newPoint.x > mapWidth ||
                        newPoint.y < -128 || newPoint.y > mapHeight
                    ) {
                        continue;
                    }
                    newPoint.xp = x;
                    newPoint.yp = y;
                    this.mapItems.push( newPoint );
                }
            }

            return this;
        },

        createPoint: function (x, y) {
            var point = new LibCanvas.Point3D(x, y, 1);
            var newPoint = new MapItemPoint(
                this.projection.toIsometric(point)
            );
            newPoint.xp = x;
            newPoint.yp = y;

            return newPoint;
        }
    });
});