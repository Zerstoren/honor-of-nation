define('service/standalone/map/loader', [
    'system/socket',
    'gateway/map',

    'service/standalone/map/gameMapItems/init',
    'service/standalone/map/draw'
], function (
    socket,
    gatewayMap,
    mapInstance,
    drawInstance
) {

    var Loader = AbstractService.extend({
        initialize: function () {
            this.$mapDI = mapInstance;
            this.$mapDrawDI = drawInstance;
            this.chanksLoaded = [];
            this.subscribeOnEvents();
        },

        subscribeOnEvents: function() {
            var self = this;

            this.$mapDI.on('onSetPosition', function(pos) {
                self.positionMapLoad(pos[0], pos[1]);
            });

            gatewayMap.on('reloadRegion', function(message) {
                self.regionReload(message.fromX, message.fromY, message.toX, message.toY);
            });

//            this.$mapDI.subscribe('mouseMove', function(a, b, c) {
//
//            });
        },

        positionMapLoad: function(x, y) {
            var dumpX, chankItem,
                self = this,
                chankList = [],
                width = this.$mapDI.getMapWidth(),
                height = this.$mapDI.getMapHeight(),
                maxWidth = x + width,
                maxHeight = y + height;

            for(0; y < maxHeight; y += 4) {
                dumpX = x;

                for(0; x < maxWidth; x += 4) {
                    chankItem = this.$mapDI.help.fromPlaceToChank(x, y);

                    if(!_.contains(chankList, chankItem) && !_.contains(this.chanksLoaded, chankItem)) {
                        chankList.push(chankItem);
                    }
                }

                x = dumpX;
            }

            if(chankList.length) {
                this.chanksLoaded = _.union(this.chanksLoaded, chankList);

                gatewayMap.loadChunks(chankList, function(message) {
                    self.$mapDrawDI.mapMerge(message.result.data);
                });
            }
        },

        regionReload: function(fromX, fromY, toX, toY) {
            var y, x, chankItem,
                self = this,
                chankList = [];

            for(y = fromY; y < toY; y += 4) {
                for(x = fromX; x < toX; x += 4) {
                    chankItem = this.$mapDI.help.fromPlaceToChank(x, y);

                    if(!Array.contain(chankList, chankItem)) {
                        chankList.push(chankItem);
                    }
                }
            }

            if(chankList.length) {
                Array.merge(this.chanksLoaded, chankList);

                gatewayMap.loadChunks(chankList, function(message) {
                    self.$mapDrawDI.mapMerge(message.result.data);
                });
            }
        }
    });

    return new Loader();
});