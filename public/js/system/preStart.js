define('system/preStart', [
    'system/bootstrap',
    'system/socket',
    'view/block/error',
    'service/standalone/user',

    'view/block/map/header',
    'view/block/map/footer',
    'view/block/map/body',

    'view/block/no/body'
], function (
    systemBootstrap,
    systemSocket,
    viewBlockError,
    serviceUser,

    ViewBlockMapHeader,
    ViewBlockMapFooter,
    ViewBlockMapBody,

    ViewBlockNoBody
) {
    'use strict';
    var map, no,
        lastRender,
        holder = jQuery('body > div.interface');

    map = function () {
        this.map.header.render();
        this.map.body.render();
        this.map.footer.render();
    };

    map.header = new ViewBlockMapHeader(holder);
    map.body   = new ViewBlockMapBody(holder);
    map.footer = new ViewBlockMapFooter(holder);

    no = function () {
        this.no.body.render();
    };
    no.body = new ViewBlockNoBody(holder);

    function renderMapBlock(controller, method, eventPath) {
        if (lastRender === 'map') {
            return;
        }

        lastRender = 'map';

        holder.empty();
    }

    function renderNoBlock(controller, method, eventPath) {
        if (lastRender === 'no') {
            return;
        }

        lastRender = 'no';

        holder.empty();
    }

    systemSocket.on('message', function (message) {
        if (message.done === false || message.done === undefined) {
            viewBlockError.showErrorBox(message);
        }
    });

    serviceUser.login();

    return {
        map: map,
        no: no
    };
});
