define('system/preStart', [
    'system/bootstrap',
    'system/socket',
    'system/errorHandler',

    'view/block/error',
    'view/elements/ractive-helper',
    'service/standalone/user',
    'service/standalone/messages',

    'view/block/map/header',
    'view/block/map/footer',
    'view/block/map/body',

    'view/block/no/body',

    'system/config'
], function (
    systemBootstrap,
    systemSocket,
    systemErrorHandler,

    viewBlockError,
    viewElementsRactiveHelper,
    serviceUser,
    serviceMessages,

    ViewBlockMapHeader,
    ViewBlockMapFooter,
    ViewBlockMapBody,

    ViewBlockNoBody,

    config
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
            if (message.error) {
                viewBlockError.showErrorBox(message.error);
            } else {
                viewBlockError.showErrorBox(message);
            }
        }
    });

    systemSocket.on('error:notOpen', function () {
        viewBlockError._connectionIsNotEstablished();
        console.log('notOpen');
    });

    systemSocket.on('error:close', function () {
        viewBlockError._connectionIsNotEstablished();
        console.log('close');
    });

    systemSocket.on('error:closed', function () {
        viewBlockError._connectionIsNotEstablished();
        console.log('closed');
    });

    systemSocket.on('dropdown', function () {
        viewBlockError._connectionIsNotEstablished();
        console.log('dropdown');
    });

    systemSocket.on('connect', function () {
        viewBlockError._connectionIsEstablished();
        serviceUser.login();
        config.$reload();
        console.log('connect');
    });

    systemSocket.on('startup', function () {
        viewBlockError._connectionIsEstablished();
        serviceUser.login();
        config.$reload();
        console.log('startup');
    });

    serviceMessages.init();
    systemErrorHandler.init();

    systemSocket.connect();

    return {
        map: map,
        no: no
    };
});
