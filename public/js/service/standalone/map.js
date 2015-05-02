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

            this.traverseEvent('calculate', this.controller);
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

        fromPositionToMapItem: function (x, y) {
            return this.controller.fromPositionToMapItem(x, y);
        },

        createUnitLayerControl: function () {
            return this.controller.createUnitLayerControl();
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
            var ev = require('service/standalone/map/draw').getInfo(e);
            this.trigger(
                'onMouseMoveObject',
                ev
            );
        },

        $onMouseClick: function (e) {
            var ev = require('service/standalone/map/draw').getInfo(e);
            this.trigger(
                'onMouseClickObject',
                ev
            );
        },

        $onMouseDoubleClick: function (e) {
            var ev = require('service/standalone/map/draw').getInfo(e);
            this.trigger(
                'onMouseDoubleClickObject',
                ev
            );
        }
    });

    return new Init();
});
