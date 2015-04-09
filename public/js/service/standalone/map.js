define('service/standalone/map', [
//    'service/standalone/map/gameMapItems/Mouse',
//    'service/standalone/map/gameMapItems/Draw',
//    'service/standalone/map/gameMapItems/Access',
    'service/standalone/map/camvas/help',
    'service/standalone/map/canvas/controller'
], function (
    Help,
    CanvasController
//    Mouse,
//    Draw,
//    Access,
) {
    var Init = AbstractService.extend({
        initialize: function () {
            this.controller = new CanvasController();
            this.help = new Help();

//            this.on('mouseMove', this.$onMouseMove, this);
//            this.on('mouseClick', this.$onMouseClick, this);
//            this.on('mouseDoubleClick', this.$onMouseDoubleClick, this);
        }

//        $onMouseMove: function (e) {
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
//        },
//
//        $onMouseClick: function (e) {
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
//        },
//
//        $onMouseDoubleClick: function (e) {
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
//                this.trigger('onMouseDoubleClickObject', e.x, e.y, type, idContainer);
//            }
//        }
    });

    return new Init();
});
