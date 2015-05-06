define('view/map/unitsManipulate', [
    'service/standalone/map'
], function (
    mapInstance
) {
    return AbstractView.extend({
        initialize: function () {
            mapInstance.on('onDragStart', this.onMouseDragStart, this);
            mapInstance.on('onDragMove', this.onUnitDrag, this);
            mapInstance.on('onDragStop', this.onStopUnitDrag, this);
            window.m = mapInstance;
            this.unitMove = false;
        },

        onMouseDragStart: function (ev) {
            if (!ev.unit()) {
                return true;
            }

            this.unitMove = ev.unit();
            this.unitLayer = ev.unit().getLayerObject();

            mapInstance.deactivateDrag();

            return true;
        },

        onUnitDrag: function (ev) {
            if (!this.unitMove) {
                return true;
            }

            var e = ev.e();
            this.unitLayer.setMoveTargetPosition([e.layerX, e.layerY]);

            return true;
        },

        onStopUnitDrag: function (ev) {
            if (!this.unitMove) {
                return true;
            }

            mapInstance.activateDrag();

            this.unitLayer.setMoveTargetPosition(null);

            this.trigger('moveArmy', this.unitMove, ev.x(), ev.y());
            this.unitMove = false;

            return true;
        }
    });
});