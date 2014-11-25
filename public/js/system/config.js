define('system/config', [
    'system/socket'
], function (
    socket
) {
    "use strict";

    var $$config = {};
    socket.send('/system/configs', {}, function(message) {
        var time = new Date();

        $$config = message.data;
        $$config.diffTime = parseInt(time.getTime() / 1000, 10) - $$config.time;
    });

    function Config() {

    }

    Config.prototype.getMapSize = function() {
        return $$config.map_size;
    };

    Config.prototype.getChunkSize = function() {
        return $$config.chunk_size;
    };

    Config.prototype.getTime = function() {
        var time = parseInt(new Date().getTime() / 1000, 10);

        return time + $$config.diffTime;
    };

    Config.prototype.getBaseRate = function () {
        return $$config.rate_base_rate;
    };

    Config.prototype.getRateBuildUp = function () {
        return $$config.rate_build_up;
    };

    return new Config();
});
