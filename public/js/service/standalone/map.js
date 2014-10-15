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
        }
    });

    var InitExemplar = Access.extend(Draw.prototype).extend(Mouse.prototype).extend(Init.prototype);
    return new InitExemplar();
});
