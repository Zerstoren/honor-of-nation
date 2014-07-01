define('system/config', [
    'system/socket'
], function (
    socket
) {
    "use strict";

    var $$config = {};
    socket.send('/system/configs', {}, function(message) {
        var time = new Date();

        $$config = message;
        $$config.diffTime = parseInt(time.getTime() / 1000, 10) - message.time;
    });

    function Config() {

    }

    Config.prototype.getMapSize = function() {
        return $$config.map_size;
    };

    Config.prototype.getChankSize = function() {
        return $$config.chank_size;
    };

    Config.prototype.getTime = function() {
        var time = parseInt(new Date().getTime() / 1000, 10);

        return time + $$config.diffTime;
    };

    return new Config();
});
