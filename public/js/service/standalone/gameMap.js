define('service/standalone/gameMap', [
    'system/socket',
    'service/standalone/user',

    'view/elements/map/draw',
    'view/elements/map/help',
    'view/elements/map/mouse'

], function (
    socket,
    userService,

    MapDraw,
    MapHelp,
    MapMouse
) {
    var GameMap = function() {
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

        userService.getMe(function (userDomain) {
            this.draw.setCameraPosition(
                userDomain.get('position').x,
                userDomain.get('position').y
            );
        }.bind(this));
    };

    GameMap.prototype.TRANSFER_ALIAS_POS_ID = 'pi';
    GameMap.prototype.TRANSFER_ALIAS_LAND = 'l';
    GameMap.prototype.TRANSFER_ALIAS_LAND_TYPE = 'lt';
    GameMap.prototype.TRANSFER_ALIAS_DECOR = 'd';
    GameMap.prototype.TRANSFER_ALIAS_BUILD = 'b';
    GameMap.prototype.TRANSFER_ALIAS_BUILD_TYPE = 'bt';

    GameMap.prototype.BUILD_EMPTY = 0;
    GameMap.prototype.BUILD_RESOURCES = 1;
    GameMap.prototype.BUILD_POSTS = 2;
    GameMap.prototype.BUILD_FORTIFICATION = 3;
    GameMap.prototype.BUILD_ROAD = 4;
    GameMap.prototype.BUILD_TOWNS = 5;
    GameMap.prototype.BUILD_RUINS = 6;


    GameMap.prototype.subscribeOnEvents = function() {
        var self = this;

        this.draw.on('onSetPosition', function(x, y) {
            self.positionMapLoad(x, y);
        });

        socket.on('/sync/map/reload_region', function(message) {
            self.regionReload(message.fromX, message.fromY, message.toX, message.toY);
        });
    };

    GameMap.prototype.positionMapLoad = function(x, y) {
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

            socket.send('/map/load_chunks', {
                chunkList: chunkList
            }, function(message) {
//                self.draw.mapMerge(message.map);
            });
        }
    };

    GameMap.prototype.regionReload = function(fromX, fromY, toX, toY) {
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

            socket.send('/map/load_chunks', {
                chunkList: chunkList
            }, function(message) {
                console.log(message)
//                self.$mapDrawDI.mapMerge(message.map);
            });
        }
    };


    return new GameMap();
});
