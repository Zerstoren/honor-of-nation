define('service/standalone/map/canvas/layers/unit', [
    'service/standalone/map/canvas/layers/abstract',

    'service/standalone/user',
    'system/imageLoader'
], function (
    AbstractLayer,

    ServiceStandaloneUser,
    imageLoader
) {
    return atom.declare(AbstractLayer, {
        configure: function method () {
            this.movePath = [];
            this.mapInstance = window.require('service/standalone/map');
            method.previous.call(this);
        },

        army: null,
        updateObject: false,
        image: false,
        taskForMove: null,
        taskForMoveEvent: null,
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
            var imageMoveFlag = imageLoader.get('unit-marker-move'),
                imageMoveAttack = imageLoader.get('unit-attack');

            this.armyDrawPoint = null;

            this.army = armyDomain;
            this.image = imageLoader.get('commander');

            this.imageMove = {
                flag  : {
                    image: imageMoveFlag,
                    shift: new LibCanvas.Point(
                        parseInt(imageMoveFlag.width / -2),
                        parseInt(imageMoveFlag.height / -2)
                    )
                },

                attack: {
                    image: imageMoveAttack,
                    shift: new LibCanvas.Point(
                        parseInt(imageMoveAttack.width / -2),
                        parseInt(imageMoveAttack.height / -2)
                    )
                }
            };
            this.currentMoveImage = null;

            this.imagePathShift = new LibCanvas.Point(32, -33);
            this.modelShift = new LibCanvas.Point(10, -72);


            this.shape = new LibCanvas.Shapes.Polygon([[0, 0], [0, 0], [0, 0], [0, 0]]);

            this.update();

            this.army.on('change:location', this.update, this);
            this.army.on('change:move_path', this.update, this);
        },

        setMoveTargetPosition: function (point, ev) {
            if (point) {
                this.taskForMove = new LibCanvas.Point(point);
                this.taskForMoveEvent = ev;
            } else {
                this.taskForMove = null;
                this.taskMove = null;
                this.taskForMoveEvent = null;
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
                move,
                shift,
                area = [],
                unitPosition = this.mapInstance.help.fromIdToPlace(this.army.get('location')),
                unitArea = this._getArea(unitPosition.x, unitPosition.y, this.image, this.modelShift),
                movePath = this.army.get('move_path');

            area = _.union(area, unitArea);

            if (this.taskForMove) {
                var ev = this.taskForMoveEvent;

                if (ev.unit() === null || ev.unit().get('_id') === this.army.get('_id')) {
                    move = this.imageMove.flag.image;
                    shift = this.imageMove.flag.shift;

                    this.currentMoveImage = move;
                } else if (ServiceStandaloneUser.getStateFor(ev.unit().get('user')._id) === ServiceStandaloneUser.STATE_WAR) {
                    move = this.imageMove.attack.image;
                    shift = this.imageMove.attack.shift;

                    this.currentMoveImage = move;
                }

                if (move) {
                    markerMove = this._getPolygonDescription(this.taskForMove, move, shift);
                    area = _.union(area, markerMove);
                    this.taskMove = new LibCanvas.Shapes.Polygon(markerMove);
                }
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
            var ctx2d = ctx.ctx2d;

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
                    this.currentMoveImage,
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
                armyDrawPoint = this.controller.fromPositionToMapItem(
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
        }
    });
});
