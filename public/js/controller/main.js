define('controller/main', [
    'service/map/main',

    'service/standalone/user',
    'service/standalone/gameMap',
    'service/standalone/mapInterface'
], function(
    ServiceMapMain,

    user,
    gameMap,
    mapInterface
) {
    'use strict';

    var protect = {
        serviceMapMain: null
    };

    return {
        main: function() {
            if (protect.serviceMapMain === null) {
                protect.serviceMapMain = new ServiceMapMain();
            }

            mapInterface.render();
//            protect.serviceMapMain.render();
        }
    };
});
