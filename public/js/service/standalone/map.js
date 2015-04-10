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

        setCameraPosition: function (x, y) {
            this.controller.centerCameraToPosition([x, y]);
            this.trigger('onSetPosition', x, y);
        },

        draw: function () {
            this.controller.redraw();
        },

        updateDataLayer: function (fn) {
            this.controller.updateDataLayer(fn);
        },

        $onMouseMove: function (e) {
//            var type = null,
//                idContainer,
//                container = jQuery(e.target);
//
//            container = container.is('.map-item,.box_message') ?  container : jQuery(e.target).parents('.map-item,.box_message');
//
//            if(container.length) {
//                type = container.attr('data-type');
//                idContainer = container.attr('data-id');
//
//                this.trigger('onMouseMoveObject', e.x, e.y, type, idContainer);
//            } else {
//                this.trigger('onMouseMoveObject', null, null, null);
//            }
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
//            var idContainer, type, base,
//                container = jQuery(e.target);
//
//            container = container.is('.map-item,.box_message') ?  container : jQuery(e.target).parents('.map-item,.box_message');
//
//            if(container.length) {
//                if (this.$lastFocusedContainer) {
//                    this.$lastFocusedContainer.removeClass('focused');
//                    this.$lastFocusedContainer = null;
//
//                    this.trigger('onMouseClickObject', null, null, null);
//                }
//
//                type = container.attr('data-type');
//                idContainer = container.attr('data-id');
//                base = container.parents('.cont').find('.map-item[data-id="' + idContainer + '"]');
//
//                this.trigger('onMouseClickObject', e.x, e.y, type, idContainer);
//                this.$lastFocusedContainer = base;
//                base.addClass('focused');
//            } else if (!this.$dragStarted) {
//                this.trigger('onMouseClickObject', null, null, null);
//
//                if (this.$lastFocusedContainer) {
//                    this.$lastFocusedContainer.removeClass('focused');
//                    this.$lastFocusedContainer = null;
//                }
//            }
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
