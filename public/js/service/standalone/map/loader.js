define('service/standalone/map/loader', [
    'system/socket',
    'gateway/map',

    'service/standalone/map',
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
            this.chunksLoaded = [];
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
        },

        positionMapLoad: function(x, y) {
            var chunkItem,
                self = this,
                mapItems = this.$mapDI.getMapItems(),
                mapItem,
                chunkList = [],
                i;

            for (i = 0; i < mapItems.length; i++) {
                mapItem = mapItems[i];

                chunkItem = this.$mapDI.help.fromPlaceToChunk(mapItem.mapX, mapItem.mapY);

                if(!_.contains(chunkList, chunkItem) && !_.contains(this.chunksLoaded, chunkItem)) {
                    chunkList.push(chunkItem);
                }
            }

            if(chunkList.length) {
                this.chunksLoaded = _.union(this.chunksLoaded, chunkList);

                gatewayMap.loadChunks(chunkList, function(message) {
                    self.$mapDrawDI.mapMerge(message.result.data);
                });
            }
        },

        regionReload: function(fromX, fromY, toX, toY) {
            var y, x, chunkItem,
                self = this,
                chunkList = [];

            for(y = fromY; y < toY; y += 4) {
                for(x = fromX; x < toX; x += 4) {
                    chunkItem = this.$mapDI.help.fromPlaceToChunk(x, y);

                    if(!Array.contain(chunkList, chunkItem)) {
                        chunkList.push(chunkItem);
                    }
                }
            }

            if(chunkList.length) {
                Array.merge(this.chunksLoaded, chunkList);

                gatewayMap.loadChunks(chunkList, function(message) {
                    self.$mapDrawDI.mapMerge(message.result.data);
                });
            }
        }
    });

    return new Loader();
});