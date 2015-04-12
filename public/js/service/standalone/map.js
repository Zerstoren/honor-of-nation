define('service/standalone/map', [
    'service/standalone/map/canvas/help',
    'service/standalone/map/canvas/controller'
], function (
    Help,
    CanvasController
) {
    var Init = AbstractService.extend({
        initialize: function () {
            this.controller = new CanvasController();
            this.help = new Help();

            this.traverseEvent('updateDataLayer', this.controller);
            this.traverseEvent('mouseMove', this.controller);

            this.controller.on('mouseMove', this.$onMouseMove, this);
            this.controller.on('mouseClick', this.$onMouseClick, this);
            this.controller.on('mouseDoubleClick', this.$onMouseDoubleClick, this);
        },

        getMapSize: function () {
            return this.controller.mapSize;
        },

        getMapItems: function () {
            return this.controller.mapItems;
        },

        draw: function () {
            this.controller.redraw();
        },

        updateDataLayer: function (fn) {
            this.controller.updateDataLayer(fn);
        },

        getCameraPosition: function () {
            return this.controller.currentCameraLocation.clone();
        },

        setCameraPosition: function (x, y) {
            this.controller.currentCameraLocation.set(x, y);
            this.controller.redraw();
            this.trigger('onSetPosition', x, y);
        },

        getCenterCameraPosition: function () {
            return this.controller.getCenterCameraPosition();
        },

        setCenterCameraPosition: function (x, y) {
            this.controller.centerCameraToPosition([x, y]);
            this.trigger('onSetPosition', x, y);
        },

        reload: function () {
            this.controller.reloadInfo();
        },

        $onMouseMove: function (e) {
            var mapDrawInstance = require('service/standalone/map/draw'),
                result = mapDrawInstance.getInfo(e.position.x, e.position.y, 'build');

            if (result) {
                this.trigger(
                    'onMouseMoveObject',
                    e.position.x,
                    e.position.y,
                    result.type,
                    result.domain.get('_id')
                );
            } else {
                this.trigger('onMouseMoveObject', null, null, null);
            }
        },

        $onMouseClick: function (e) {
            var mapDrawInstance = require('service/standalone/map/draw'),
                result = mapDrawInstance.getInfo(e.position.x, e.position.y, 'build');

            if(result) {
                this.trigger(
                    'onMouseClickObject',
                    e.position.x,
                    e.position.y,
                    result.type,
                    result.domain.get('_id')
                );
            } else if (!this.controller.isDragged()) {
                this.trigger('onMouseClickObject', null, null, null);
            }
        },

        $onMouseDoubleClick: function (e) {
            var mapDrawInstance = require('service/standalone/map/draw'),
                result = mapDrawInstance.getInfo(e.position.x, e.position.y, 'build');

            if (result) {
                this.trigger(
                    'onMouseDoubleClickObject',
                    e.position.x,
                    e.position.y,
                    result.type,
                    result.domain.get('_id')
                );
            }
        }
    });

    return new Init();
});
