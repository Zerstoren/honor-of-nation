define('service/standalone/map', [
    'service/standalone/map/canvas/help',
    'service/standalone/map/canvas/controller'
], function (
    Help,
    CanvasController
) {
    var Init = AbstractService.extend({
        initialize: function () {
            this.drawMap = null;

            window.require(['service/standalone/map/draw'], function (draw) {
                this.drawMap = draw;

                this.traverseEvent('calculate', this.controller);
                this.traverseEvent('mouseMove', this.controller);

                this.controller.on('mouseMove', this.$onMouseMove, this);
                this.controller.on('mouseClick', this.$onMouseClick, this);
                this.controller.on('mouseDoubleClick', this.$onMouseDoubleClick, this);

                this.controller.on('mouseDown', this.$onDragStart, this);
                this.controller.on('mouseUp', this.$onDragStop, this);
                this.controller.on('mouseMove', this.$onDragMove, this);
            }.bind(this));

            this.controller = new CanvasController();
            this.help = new Help();
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

        deactivateDrag: function () {
            this.controller.disableDrag();
        },

        activateDrag: function () {
            this.controller.enableDrag();
        },

        $onDragStart: function (e) {
            this.trigger(
                'onDragStart',
                this.drawMap.getInfo(e)
            );
        },

        $onDragStop: function (e) {
            this.trigger(
                'onDragStop',
                this.drawMap.getInfo(e)
            );
        },

        $onDragMove: function (e) {
            this.trigger(
                'onDragMove',
                this.drawMap.getInfo(e)
            );
        },

        $onMouseMove: function (e) {
            this.trigger(
                'onMouseMoveObject',
                this.drawMap.getInfo(e)
            );
        },

        $onMouseClick: function (e) {
            this.trigger(
                'onMouseClickObject',
                this.drawMap.getInfo(e)
            );
        },

        $onMouseDoubleClick: function (e) {
            this.trigger(
                'onMouseDoubleClickObject',
                this.drawMap.getInfo(e)
            );
        }
    });

    return new Init();
});
