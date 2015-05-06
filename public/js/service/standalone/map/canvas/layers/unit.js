define('service/standalone/map/canvas/layers/unit', [
    'service/standalone/map/canvas/layers/abstract',

    'system/imageLoader'
], function (
    AbstractLayer,
    imageLoader
) {
    return atom.declare(AbstractLayer, {
        configure: function method () {
            window.ctx = this.layer.ctx;
            this.mapInstance = window.require('service/standalone/map');
            this.movePath = [];
            method.previous.call(this);
        },

        army: null,
        updateObject: false,
        image: false,
        taskForMove: null,
        taskMove: null,
        newShape: null,
        movePath: null,

        pathway: {
            t:  imageLoader.get('move-top-left'),
            tr: imageLoader.get('move-top'),
            r:  imageLoader.get('move-top-right'),
            br: imageLoader.get('move-right'),
            b:  imageLoader.get('move-bottom-right'),
            bl: imageLoader.get('move-bottom'),
            l:  imageLoader.get('move-bottom-left'),
            tl: imageLoader.get('move-left'),
            c:  imageLoader.get('move-center')
        },

        setDomain: function (armyDomain) {
            this.armyDrawPoint = null;

            this.army = armyDomain;
            this.image = imageLoader.get('commander');
            this.imageMove = imageLoader.get('unit-marker-move');

            this.moveImageShift = new LibCanvas.Point(
                parseInt(this.imageMove.width / -2),
                parseInt(this.imageMove.height / -2)
            );
            this.imagePathShift = new LibCanvas.Point(32, -33);
            this.modelShift = new LibCanvas.Point(10, -72);


            this.shape = new LibCanvas.Shapes.Polygon([[0, 0], [0, 0], [0, 0], [0, 0]]);

            this.update();

            this.army.on('change:location', this.update, this);
            this.army.on('change:move_path', this.update, this);
        },

        setMoveTargetPosition: function (point) {
            if (point) {
                this.taskForMove = new LibCanvas.Point(point);
            } else {
                this.taskForMove = null;
                this.taskMove = null;
            }

            this.update();
        },

        getDomain: function () {
            return this.army;
        },

        isTriggerPoint: function (point) {
            return this.unitShape.hasPoint(point);
        },

        update: function () {
            this.updateObject = true;
        },

        createShape: function () {
            if (this.army === null) {
                return this;
            }

            this.movePath = [];

            var self = this,
                markerMove,
                area = [],
                unitPosition = this.mapInstance.help.fromIdToPlace(this.army.get('location')),
                unitArea = this._getArea(unitPosition.x, unitPosition.y, this.image, this.modelShift),
                movePath = this.army.get('move_path');

            area = _.union(area, unitArea);

            if (this.taskForMove) {
                markerMove = this._getPolygonDescription(this.taskForMove, this.imageMove, this.moveImageShift);
                area = _.union(area, markerMove);
                this.taskMove = new LibCanvas.Shapes.Polygon(markerMove);
            }

            if (movePath.length) {
                _.each(movePath, function (item) {
                    var location = self.mapInstance.help.fromIdToPlace(item.pos_id),
                        position = self._getArea(
                            location.x,
                            location.y,
                            self.pathway[item.direction],
                            self.imagePathShift
                        );

                    self.movePath.push({
                        location: new LibCanvas.Point([position[0][0], position[0][1]]),
                        direction: self.pathway[item.direction]
                    });

                    area = _.union(area, position);
                });
            }

            this.unitShape = new LibCanvas.Shapes.Polygon(unitArea);

            this.newShape = new LibCanvas.Shapes.Polygon(area);


            return this;
        },

        renderTo: function (ctx) {
            var self = this;

            ctx2d = ctx.ctx2d;

            if (this.movePath.length) {
                _.each(this.movePath, function (item) {
                    ctx2d.drawImage(
                        item.direction,
                        item.location.x,
                        item.location.y
                    );
                });
            }

            ctx2d.drawImage(
                this.image,
                this.armyDrawPoint.x + this.modelShift.x,
                this.armyDrawPoint.y + this.modelShift.y
            );

            if (this.taskMove) {
                ctx2d.drawImage(
                    this.imageMove,
                    this.taskMove.get(0).x,
                    this.taskMove.get(0).y
                );
            }

            this.shape = this.newShape;
        },

        onUpdate: function () {
            if (this.updateObject === false) {
                return false;
            }

            var positionArmy = this.mapInstance.help.fromIdToPlace(this.army.get('location')),
                armyDrawPoint = this.mapInstance.fromPositionToMapItem(
                    positionArmy.x, positionArmy.y
                );

            this.armyDrawPoint = this.projection.toIsometric(armyDrawPoint);

            this.updateObject = false;
            this.createShape();
            this.redraw();
            return true;
        },

        clearPrevious: function (ctx) {
            LibCanvas.App.Element.prototype.clearPrevious.apply(this, [ctx]);
        },

        _getArea: function (x, y, image, shift) {
            var drawPosition,
                mapPosition = this.mapInstance.fromPositionToMapItem(x, y);

            if (shift === undefined) {
                shift = {
                    x: 0,
                    y: 0
                };
            }

            if (image === undefined) {
                image = {
                    width: 0,
                    height: 0
                };
            }

            if (!mapPosition) {
                return null;
            }

            drawPosition = this.projection.toIsometric([mapPosition.x, mapPosition.y]);
            return this._getPolygonDescription(drawPosition, image, shift);
        },

        _getPolygonDescription: function (drawPoint, image, shift) {
            if (shift === undefined) {
                shift = {
                    x: 0,
                    y: 0
                };
            }

            if (image === undefined) {
                image = {
                    width: 0,
                    height: 0
                };
            }

            drawPoint.x += shift.x;
            drawPoint.y += shift.y;

            return [
                [drawPoint.x, drawPoint.y],
                [drawPoint.x + image.width, drawPoint.y],
                [drawPoint.x + image.width, drawPoint.y + image.height],
                [drawPoint.x, drawPoint.y + image.height]
            ];
        }
    });
});
