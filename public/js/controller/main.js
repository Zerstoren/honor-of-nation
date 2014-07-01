define('controller/main', [
    'service/map/main',

    'service/standalone/user',
    'service/standalone/gameMap'
], function(
    ServiceMapMain,

    user,
    gameMap
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

            protect.serviceMapMain.render();
        }
    };
});
