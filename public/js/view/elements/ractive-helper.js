define('view/elements/ractive-helper', [
    'view/elements/map/help'
], function (ViewElementsMapHelp) {

    var mapHelp = new ViewElementsMapHelp();

    Ractive.defaults.data = {
        formatters: {
            fromIdToPlace: function (posId) {
                var pos = mapHelp.fromIdToPlace(parseInt(posId, 10));
                return pos.x + 'x' + pos.y;
            }
        }
    };
});