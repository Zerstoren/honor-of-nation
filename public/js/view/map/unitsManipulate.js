define('view/map/unitsManipulate', [
    'service/standalone/map'
], function (
    mapInstance
) {
    return AbstractView.extend({
        initialize: function () {
            mapInstance.on('mouseDragStart', this.onMouseDragStart, this);
            mapInstance.on('mouseMove', this.onUnitDrag, this);
            mapInstance.on('mouseUp', this.onStopUnitDrag, this);

            this.unitMove = false;
            this.targetPosition = [null, null];
            this.flag = jQuery('<div class="move-to-flag">');
        },

        onMouseDragStart: function (ev) {
            var target = jQuery(ev.target);
            target = target.is('.army_container,.army_box') ? target : target.parents('.army_container,.army_box');
            if (target.length === 0 || target.attr('data-type') !== 'army') {
                return;
            }

            this.unitMove = target.attr('data-id');
            mapInstance.deactivateDrag();
        },

        onUnitDrag: function (ev) {
            if (!this.unitMove) {
                return;
            }

            if (this.targetPosition[0] !== null && this.targetPosition[1] !== null) {
                this.flag.detach();
            }

            var domCell = mapInstance.getDomCell(ev.x, ev.y, 4);
            this.targetPosition = [ev.x, ev.y];
            domCell.append(this.flag);
        },

        onStopUnitDrag: function (ev) {
            if (!this.unitMove) {
                return;
            }

            if (this.targetPosition[0] !== null && this.targetPosition[1] !== null) {
                this.trigger('moveArmy', this.unitMove, this.targetPosition[0], this.targetPosition[1]);
                this.flag.detach();
                this.targetPosition = [null, null];
            }

            this.unitMove = false;
        }
    });
});