define('service/standalone/map', [
    'service/standalone/map/gameMapItems/Mouse',
    'service/standalone/map/gameMapItems/Draw',
    'service/standalone/map/gameMapItems/Access',
    'service/standalone/map/gameMapItems/Help'
], function (
    Mouse,
    Draw,
    Access,
    Help
) {
    var Init = AbstractService.extend({
        initialize: function () {
            this.$layer = jQuery('#canvas_map');

            this.config = {
                cellSize: 96
            };

            Draw.prototype.initialize.apply(this);
            Mouse.prototype.initialize.apply(this);

            this.help = new Help();

            this.$drawMap();
            this.on('mouseMove', this.$onMouseMove, this);
            this.on('mouseClick', this.$onMouseClick, this);
            this.on('mouseDoubleClick', this.$onMouseDoubleClick, this);
        },

        $onMouseMove: function (e) {
            var type = null,
                idContainer,
                container = jQuery(e.target);

            container = container.is('.map-item,.box_message') ?  container : jQuery(e.target).parents('.map-item,.box_message');

            if(container.length) {
                type = container.attr('data-type');
                idContainer = container.attr('data-id');

                this.trigger('onMouseMoveObject', e.x, e.y, type, idContainer);
            } else {
                this.trigger('onMouseMoveObject', null, null, null);
            }
        },

        $onMouseClick: function (e) {
            var idContainer, type, base,
                container = jQuery(e.target);

            container = container.is('.map-item,.box_message') ?  container : jQuery(e.target).parents('.map-item,.box_message');

            if(container.length) {
                if (this.$lastFocusedContainer) {
                    this.$lastFocusedContainer.removeClass('focused');
                    this.$lastFocusedContainer = null;

                    this.trigger('onMouseClickObject', null, null, null);
                }

                type = container.attr('data-type');
                idContainer = container.attr('data-id');
                base = container.parents('.cont').find('.map-item[data-id="' + idContainer + '"]');

                this.trigger('onMouseClickObject', e.x, e.y, type, idContainer);
                this.$lastFocusedContainer = base;
                base.addClass('focused');
            } else {
                this.trigger('onMouseClickObject', null, null, null);

                if (this.$lastFocusedContainer) {
                    this.$lastFocusedContainer.removeClass('focused');
                    this.$lastFocusedContainer = null;
                }
            }
        },

        $onMouseDoubleClick: function (e) {
            var type = null,
                idContainer,
                container = jQuery(e.target);

            container = container.is('.map-item,.box_message') ?  container : jQuery(e.target).parents('.map-item,.box_message');

            if(container.length) {
                type = container.attr('data-type');
                idContainer = container.attr('data-id');

                this.trigger('onMouseDoubleClickObject', e.x, e.y, type, idContainer);
            }
        }
    });

    var InitExemplar = Access.extend(Draw.prototype).extend(Mouse.prototype).extend(Init.prototype);
    return new InitExemplar();
});
