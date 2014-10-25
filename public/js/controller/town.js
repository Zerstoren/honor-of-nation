define('controller/town', [
    'service/town/main'
], function(
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

            protect.serviceTownMain.render(townId);
        }
    };
});
