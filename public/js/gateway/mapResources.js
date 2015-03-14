define('gateway/mapResources', [] , function () {
    var MapResources = AbstractGateway.extend({
        mapLoad: function(posId, success) {
            this.socket.send('/town_builds/remove', {
                posId: posId
            }, function (data) {
                if (data.done) {
                    return data.resource;
                }
            });
        }
    });
});