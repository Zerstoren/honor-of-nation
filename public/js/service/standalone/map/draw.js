define('service/standalone/map/draw', [
    'service/standalone/user',

    'service/standalone/map/gameMapItems/init'
], function (
    userService,
    mapInstance
) {
    var Draw = AbstractService.extend({

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

        initialize: function () {
            this.$mapDI = mapInstance;
//            this.mapDrawObjectsTownsDI = mapDrawObjectsTowns;
//            this.mapDrawObjectsResourceDI = mapDrawObjectsResource;
            this.$isInit = false;
        },

        init: function () {
            if(this.$isInit) {
                return false;
            }

            this.$isInit = true;

            userService.getMe(function (userDomain) {
                this.$mapDI.setCameraPosition(
                    userDomain.get('position').x,
                    userDomain.get('position').y
                );

            }.bind(this));

            this.map  = {};
            this.$previousMousePosition = [0, 0];

            this.setUpdateDataFnLayer();

            jQuery(window).resize(function (e) {
                var position = this.$mapDI.getPosition();
                this.$mapDI.clear();
                this.$mapDI.$drawMap();
                this.$mapDI.setPosition(position[0], position[1]);
            }.bind(this));


            return true;
        },

        setUpdateDataFnLayer: function() {
            var self = this;

            this.$mapDI.setUpdateDataFnLayer(function (x, y) {
                if(x < 0 || x >= 2000 || y < 0 || y >= 2000) {
                    return ['no_map'];
                }

                var tmp, classList = [];
                tmp = self.getLand(x, y);
                if(!tmp) {
                    return ['shadow'];
                }

                classList.push(tmp);

                tmp = self.getDecoration(x, y);
                if(tmp) {
                    classList.push(tmp);
                }

                tmp = self.getBuild(x, y);
                if(tmp) {
                    classList.push(tmp);
                }

                return classList;
            });
        },

        getLand: function(x, y) {
            if(this.map[y] === undefined || this.map[y][x] === undefined) {
                return 'shadow';
            }

            return "land-" +
                this.map[y][x][this.TRANSFER_ALIAS_LAND] + "-" +
                this.map[y][x][this.TRANSFER_ALIAS_LAND_TYPE];
        },

        getDecoration: function(x, y) {
            if(this.map[y] === undefined || this.map[y][x] === undefined) {
                return false;
            }

            return "decor-" + this.map[y][x][this.TRANSFER_ALIAS_DECOR];
        },

        getBuild: function(x, y) {
            if(this.map[y] === undefined || this.map[y][x] === undefined) {
                return false;
            }

            switch(this.map[y][x][this.TRANSFER_ALIAS_BUILD]) {
                case this.BUILD_TOWNS:
                    return this.mapDrawObjectsTownsDI.getBuildObject(
                        x,
                        y,
                        this.map[y][x][this.TRANSFER_ALIAS_BUILD_TYPE]
                    );

                case this.BUILD_RESOURCES:
                    return this.mapDrawObjectsResourceDI.getResourceObject(
                        x,
                        y,
                        this.map[y][x][this.TRANSFER_ALIAS_BUILD_TYPE]
                    );

                case this.BUILD_EMPTY:
                    return false;

                default:
                    return false;
            }
        },

        mapMerge: function(map) {
            var x, y;

            for(y in map) {
                if(map.hasOwnProperty(y)) {
                    for(x in map[y]) {
                        if(map[y].hasOwnProperty(x)) {
                            if(this.map[y] === undefined) {
                                this.map[y] = {};
                            }

                            this.map[y][x] = map[y][x];
                        }
                    }
                }
            }

            this.$mapDI.update();
        }
    });

    return new Draw();
});