define('service/standalone/map/draw', [
    'service/standalone/user',

    'service/standalone/map',
    'service/standalone/map/gameMapItems/drawObjects/resource',
    'service/standalone/map/gameMapItems/drawObjects/town',
    'service/standalone/map/gameMapItems/drawObjects/army'
], function (
    userService,
    mapInstance,
    MapDrawObjectsResource,
    MapDrawObjectsTown,
    MapDrawObjectsArmy
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
            this.mapDrawObjectsTowns = new MapDrawObjectsTown();
            this.mapDrawObjectsResource = new MapDrawObjectsResource();
            this.mapDrawObjectsArmy = new MapDrawObjectsArmy();
            this.$isInit = false;
        },

        init: function () {
            if(this.$isInit) {
                return false;
            }

            this.$isInit = true;

            userService.getDeffer().deffer(DefferedTrigger.ON_GET_AND_UPDATE, function (userDomain) {
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

        updateArmyPosition: function (oldLocation, general) {
            this.mapDrawObjectsArmy.updateArmyPosition(oldLocation, general);
        },

        setUpdateDataFnLayer: function() {
            var self = this;

            this.$mapDI.setUpdateDataFnLayer(function (x, y) {
                var location = mapInstance.help.fromPlaceToId(x, y);
                if(x < 0 || x >= 2000 || y < 0 || y >= 2000) {
                    return ['no_map'];
                }

                var tmp, classList = [];
                if(!(tmp = self.getLand(x, y, location))) {
                    return ['shadow'];
                }

                classList.push(tmp);

                if((tmp = self.getDecoration(x, y, location))) {
                    classList.push(tmp);
                }

                self.getBuild(x, y, location);
                self.getArmy(x, y, location);

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
                    return this.mapDrawObjectsTowns.getTownObject(
                        x,
                        y,
                        this.map[y][x][this.TRANSFER_ALIAS_BUILD_TYPE]
                    );

                case this.BUILD_RESOURCES:
                    return this.mapDrawObjectsResource.getResourceObject(
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

        getArmy: function (x, y, mapId) {
            if (!this.mapDrawObjectsArmy.armyMap[mapId]) {
                return false;
            }

            return this.mapDrawObjectsArmy.getArmyObject(x, y, mapId);
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
        },

        getInstanceArmy: function () {
            return this.mapDrawObjectsArmy;
        }
    });

    return new Draw();
});