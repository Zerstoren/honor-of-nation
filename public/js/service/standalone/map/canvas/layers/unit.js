define('service/standalone/map/canvas/layers/unit', [
    'service/standalone/map/canvas/layers/abstract',

    'system/imageLoader'
], function (
    AbstractLayer,
    imageLoader
) {
    return atom.declare(AbstractLayer, {
        configure: function () {
            this.mapInstance = window.require('service/standalone/map');
            AbstractLayer.prototype.configure.apply(this);
        },

        army: null,
        updateObject: false,
        image: false,
//        pathway: {
//            t:  jQuery('<div class="unit_move_path t"></div>'),
//            tr: jQuery('<div class="unit_move_path tr"></div>'),
//            r:  jQuery('<div class="unit_move_path r"></div>'),
//            br: jQuery('<div class="unit_move_path br"></div>'),
//            b:  jQuery('<div class="unit_move_path b"></div>'),
//            bl: jQuery('<div class="unit_move_path bl"></div>'),
//            l:  jQuery('<div class="unit_move_path l"></div>'),
//            tl: jQuery('<div class="unit_move_path tl"></div>'),
//            c:  jQuery('<div class="unit_move_path c"></div>')
//        },

        setDomain: function (armyDomain) {
            this.army = armyDomain;
            this.image = imageLoader.get('commander');

            this.armyDrawPoint = null;
            this.modelShift = new LibCanvas.Point(10, -52);
            // set events

            this.createShape();
            this.update();
        },

        getDomain: function () {
            return this.army;
        },

        createShape: function () {
            if (this.army === null) {
                return this;
            }

            var i = 0,
//                result,
//                position,
//                drawPosition,
//                positions = [],
                unitPosition = this.mapInstance.help.fromIdToPlace(this.army.get('location')),
                unitArea = this._getArea(unitPosition.x, unitPosition.y, this.image, this.modelShift);

//            for (i; i < positions.length; i++) {
//                position = positions[i];
//            }

            this.shape = new LibCanvas.Shapes.Polygon(unitArea);
            this.unitShape = new LibCanvas.Shapes.Polygon(unitArea);

            return this;
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
            drawPosition.x += shift.x;
            drawPosition.y += shift.y;

            return [
                [drawPosition.x, drawPosition.y],
                [drawPosition.x + image.width, drawPosition.y],
                [drawPosition.x + image.width, drawPosition.y + image.height],
                [drawPosition.x, drawPosition.y + image.height]
            ];

        },

        isTriggerPoint: function (point) {
            return this.unitShape.hasPoint(point);
        },

        update: function () {
            this.updateObject = true;
        },

        renderTo: function (ctx) {
            ctx2d = ctx.ctx2d;
            ctx2d.drawImage(
                this.image,
                this.armyDrawPoint.x + this.modelShift.x,
                this.armyDrawPoint.y + this.modelShift.y
            );

            this.armyDrawPoint = null;
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

            this.createShape();
            this.redraw();
            this.updateObject = false;
            return true;
        },

        clearPrevious: function (ctx) {
            LibCanvas.App.Element.prototype.clearPrevious.apply(this, [ctx]);
        }
    });
});
