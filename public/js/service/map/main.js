define('service/map/main', [
    'libs/easypath',
    'factory/army',
    'service/standalone/map',
    'service/standalone/map/draw',

    'view/map/unitsManipulate',

    'gateway/army'
], function (
    EasyStar,
    factoryArmy,
    mapInstance,
    mapDrawInstance,

    ViewMapUnitsManipulate,

    gatewayArmy
) {
    return AbstractService.extend({
        initialize: function () {
            factoryArmy.on('add', this.onAddArmy, this);
            this.viewUnitsManipulate = new ViewMapUnitsManipulate();
            this.viewUnitsManipulate.on('moveArmy', this.onMoveArmy, this);
        },

        onAddArmy: function (domain) {
            mapDrawInstance.getInstanceArmy().addArmy(domain);
            mapInstance.update();
        },

        onMoveArmy: function (armyId, x, y) {
            var army = factoryArmy.getFromPool(armyId),
                prevX = army.getX(),
                prevY = army.getY(),
                sizeX = x > prevX ? x - prevX : prevX - x,
                sizeY = y > prevY ? y - prevY : prevY - y,
                path = [], grid, estar, fromX, fromY, toX, toY;

            grid = new EasyStar.grid(sizeX, sizeY);
            estar = new EasyStar.js();

            if (prevX > x) {
                fromX = prevX - x;
                toX = 0;
            } else {
                fromX = 0;
                toX = x - prevX;
            }

            if (prevY > y) {
                fromY = prevY - y;
                toY = 0;
            } else {
                fromY = 0;
                toY = y - prevY;
            }

            estar.enableDiagonals();
            estar.setGrid(grid.get());
            estar.setAcceptableTiles([0]);
            estar.findPath(fromX, fromY, toX, toY, function (pathCalculate) {
                var pathItem, direction,
                    prevXPosition = fromX,
                    prevYPosition = fromY;

                if (pathCalculate === null) {
                    return;
                }

                var i;
                for(i = 0; i < pathCalculate.length; i++) {
                    if (i === 0) {
                        continue;
                    }
                    pathItem = pathCalculate[i];

                    switch((prevXPosition - pathItem.x) + "x" + (prevYPosition - pathItem.y)) {
                        case "0x1": direction = 't'; break;
                        case "1x1": direction = 'tr'; break;
                        case "1x0": direction = 'r'; break;
                        case "1x-1": direction = 'br'; break;
                        case "0x-1": direction = 'b'; break;
                        case "-1x-1": direction = 'bl'; break;
                        case "-1x0": direction = 'l'; break;
                        case "-1x1": direction = 'tl'; break;
                    }

                    path.push([
                        pathItem.x + (prevX > x ? x : prevX),
                        pathItem.y + (prevY > y ? y : prevY),
                        direction
                    ]);
                }
            });
            estar.calculate();

            if (path.length) {
                gatewayArmy.move(armyId, path);
            }
        }
    });
});
