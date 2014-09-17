define('controller/main', [
    'service/map/main',

    'service/standalone/map/draw',
    'service/standalone/map/loader',

    'service/standalone/user',
    'service/standalone/mapInterface'
], function(
    ServiceMapMain,

    drawMap,
    loaderMap,

    user,
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

            drawMap.init();
            mapInterface.render();
//            protect.serviceMapMain.render();
        }
    };
});
