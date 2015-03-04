define('system/config', [
    'system/socket'
], function (
    socket
) {
    "use strict";

    var $$config = {};

    function Config() {

    }

    Config.prototype.$reload = function () {
        socket.send('/system/configs', {}, function(message) {
            var time = new Date();

            $$config = message.data;
            $$config.diffTime = parseInt(time.getTime() / 1000, 10) - $$config.time;
        });
    };

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

    Config.prototype.getEquipmentWeapon = function () {
        return $$config.equipment_weapon;
    };

    Config.prototype.getEquipmentArmor = function () {
        return $$config.equipment_armor;
    };

    Config.prototype.getEquipmentUnit = function () {
        return $$config.equipment_unit;
    };

    Config.prototype.getPowerRestore = function () {
        return $$config.power_restore;
    };

    Config.prototype.$reload();

    return new Config();
});
