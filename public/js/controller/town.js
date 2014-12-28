define('controller/town', [
    'service/standalone/mapInterface',

    'service/town/main',
    'service/standalone/user'
], function(
    mapInterface,

    ServiceTownMain,
    ServiceStandaloneUser
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

            ServiceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (domain) {
                mapInterface.render();
                protect.serviceTownMain.render(townId);
            });
        },

        leaveShow: function () {
            protect.serviceTownMain.unRender();
        },

        updateTownBuilds: function (builds, queue) {
            protect.serviceTownMain.update(builds, queue);
        }
    };
});
