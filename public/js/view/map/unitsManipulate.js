define('view/map/unitsManipulate', [
    'service/standalone/map',
    'service/standalone/user',
], function (
    mapInstance,
    ServiceStandaloneUser
) {
    return AbstractView.extend({
        initialize: function () {
            mapInstance.on('onDragStart', this.onMouseDragStart, this);
            mapInstance.on('onDragMove', this.onUnitDrag, this);
            mapInstance.on('onDragStop', this.onStopUnitDrag, this);
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
            this.unitLayer.setMoveTargetPosition([e.offsetX, e.offsetY], ev);

            return true;
        },

        onStopUnitDrag: function (ev) {
            if (!this.unitMove) {
                return true;
            }

            mapInstance.activateDrag();

            this.unitLayer.setMoveTargetPosition(null);

            if (
                ev.unit() &&
                ServiceStandaloneUser.getStateFor(ev.unit().get('user')._id) !== ServiceStandaloneUser.STATE_WAR &&
                ev.unit().get('_id') !== this.unitLayer.army.get('_id')
            ) {
                debugger;
            }

            this.trigger('moveArmy', this.unitMove, ev.x(), ev.y());
            this.unitMove = false;

            return true;
        }
    });
});