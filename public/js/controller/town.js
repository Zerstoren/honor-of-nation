define('controller/town', [
    'service/standalone/mapInterface',

    'service/town/main'
], function(
    mapInterface,

    ServiceTownMain
) {
    'use strict';

    var protect = {
        serviceTownMain: null
    };

    return {
        show: function(townId) {
            if (protect.serviceTownMain === null) {
                protect.serviceTownMain = new ServiceTownMain();
            }

            mapInterface.render();
            protect.serviceTownMain.render(townId);
        },

        leaveShow: function () {
            protect.serviceTownMain.unRender();
        }
    };
});
