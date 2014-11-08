define('controller/admin', [
    'service/standalone/mapInterface',

    'service/admin/main',
], function(
    mapInterface,

    ServiceAdminMain
) {
    'use strict';

    var protect = {
        serviceAdminMain: null
    };

    return {
        admin: function() {
            if (protect.serviceAdminMain === null) {
                protect.serviceAdminMain = new ServiceAdminMain();
            }

            mapInterface.render();
            protect.serviceAdminMain.render();
        },

        leaveAdmin: function () {
            protect.serviceAdminMain.unRender();
        }
    };
});
