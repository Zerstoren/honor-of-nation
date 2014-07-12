define('controller/admin', [
    'system/preStart',
    'service/standalone/mapInterface',

    'service/admin/main',
    'service/admin/terrain'
], function(
    preStart,
    mapInterface,

    ServiceAdminMain,
    ServiceAdminTerrain
) {
    'use strict';

    var protect = {
        serviceAdminTerrain: null,
        serviceAdminMain: null
    };

    return {
        admin: function() {
            if (protect.serviceAdminMain === null) {
                protect.serviceAdminMain = new ServiceAdminMain();
            }

            if (protect.serviceAdminTerrain === null) {
                protect.serviceAdminTerrain = new ServiceAdminTerrain();
            }

            mapInterface.render();
            protect.serviceAdminMain.render();
        },

        leaveAdmin: function () {
            protect.serviceAdminMain.unRender();
        }
    };
});
