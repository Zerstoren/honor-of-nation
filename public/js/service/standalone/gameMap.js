define('service/standalone/gameMap', [
    'system/socket',
    'service/standalone/user',

    'gateway/map',

    'view/elements/map/draw',
    'view/elements/map/help',
    'view/elements/map/mouse'

], function (
    socket,
    userService,

    gatewayMap,

    MapDraw,
    MapHelp,
    MapMouse
) {
    var GameMap = AbstractService.extend({
        initialize: function() {
            this.holder = jQuery('body > div.game-map');
            this.$layer = jQuery(this.holder);

            this.chunksLoaded = [];
            this.map = {};
            this.config = {
                cellSize: 96
            };

            this.draw = new MapDraw(this);
            this.help = new MapHelp(this);
            this.mouse = new MapMouse(this);

            this.draw.$drawMap();
            this.subscribeOnEvents();
            this.mouse.afterRender();

            userService.getMe(function (userDomain) {
                this.draw.setCameraPosition(
                    userDomain.get('position').x,
                    userDomain.get('position').y
                );
            }.bind(this));
        },

        TRANSFER_ALIAS_POS_ID: 'pi',
        TRANSFER_ALIAS_LAND: 'l',
        TRANSFER_ALIAS_LAND_TYPE: 'lt',
        TRANSFER_ALIAS_DECOR: 'd',
        TRANSFER_ALIAS_BUILD: 'b',
        TRANSFER_ALIAS_BUILD_TYPE: 'bt',

        BUILD_EMPTY: 0,
        BUILD_RESOURCES: 1,
        BUILD_POSTS: 2,
        BUILD_FORTIFICATION: 3,
        BUILD_ROAD: 4,
        BUILD_TOWNS: 5,
        BUILD_RUINS: 6,

        subscribeOnEvents: function() {
            var self = this;

            this.draw.on('onSetPosition', function(x, y) {
                self.positionMapLoad(x, y);
            });

            socket.on('/sync/map/reload_region', function(message) {
                self.regionReload(message.fromX, message.fromY, message.toX, message.toY);
            });
        },

        positionMapLoad: function(x, y) {
            var dumpX, chunkItem,
                self = this,
                chunkList = [],
                width = this.draw.getMapWidth(),
                height = this.draw.getMapHeight(),
                maxWidth = x + width,
                maxHeight = y + height;

            for(0; y < maxHeight; y += 4) {
                dumpX = x;

                for(0; x < maxWidth; x += 4) {
                    chunkItem = this.help.fromPlaceToChunk(x, y);

                    if(!_.contains(chunkList, chunkItem) && !_.contains(this.chunksLoaded, chunkItem)) {
                        chunkList.push(chunkItem);
                    }
                }

                x = dumpX;
            }

            if(chunkList.length) {
                this.chunksLoaded = _.union(this.chunksLoaded, chunkList);
                gatewayMap.loadChunks(chunkList, function(message) {
                    self.draw.mapMerge(message.result.data);
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

                    if(!_.contains(chunkList, chunkItem)) {
                        chunkList.push(chunkItem);
                    }
                }
            }

            if(chunkList.length) {
                this.chunksLoaded = _.union(this.chunksLoaded, chunkList);
                gatewayMap.loadChunks(chunkList, function(message) {
                    self.draw.mapMerge(message.result.data);
                });
            }
        }
    });

    return new GameMap();
});
