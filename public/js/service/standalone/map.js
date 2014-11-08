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
                container;

            container = this.$GetPrimaryContainer(e.x, e.y);

            if(container !== false) {
                type = container[0].classList[0].replace('_container', '');
                idContainer = container[0].id.split('_')[1];

                this.trigger('onMouseMoveObject', e.x, e.y, type, idContainer);
            } else {
                this.trigger('onMouseMoveObject', null, null, null);
            }
        },

        $onMouseClick: function (e) {
            var container, idContainer, type;

            container = this.$GetPrimaryContainer(e.x, e.y);

            if(container !== false) {
                if (this.$lastFocusedContainer) {
                    this.$lastFocusedContainer.removeClass('focused');
                    this.$lastFocusedContainer = null;

                    this.trigger('onMouseClickObject', null, null, null);
                }

                type = container[0].classList[0].replace('_container', '');
                idContainer = container[0].id.split('_')[1];

                this.trigger('onMouseClickObject', e.x, e.y, type, idContainer);
                this.$lastFocusedContainer = container;
                container.addClass('focused');
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
                container;

            container = this.$GetPrimaryContainer(e.x, e.y);

            if(container !== false) {
                type = container[0].classList[0].replace('_container', '');
                idContainer = container[0].id.split('_')[1];

                this.trigger('onMouseDoubleClickObject', e.x, e.y, type, idContainer);
            }
        },

        $GetPrimaryContainer: function(x, y) {
            var usedContainer = false,
                cell = this.getDomCell(x, y),
                items = cell.find('.cont > div');

            if(items.length === 0) {
                return false;
            }

            items.each(function(position, item) {
                item = jQuery(item);

                if(item.hasClass('unit_container') && !usedContainer) {
                    usedContainer = item;
                } else {
                    usedContainer = item;
                }
            });

            return usedContainer;
        }
    });

    var InitExemplar = Access.extend(Draw.prototype).extend(Mouse.prototype).extend(Init.prototype);
    return new InitExemplar();
});
