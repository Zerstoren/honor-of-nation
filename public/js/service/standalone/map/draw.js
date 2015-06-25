define('service/standalone/map/draw', [
    'service/standalone/user',
    'service/standalone/map',

    'system/imageLoader',

    'service/standalone/map/objects/resource',
    'service/standalone/map/objects/town',
    'service/standalone/map/objects/army',

    'service/standalone/map/eventWrapper'
], function (
    userService,
    mapInstance,

    imageLoader,

    MapDrawObjectsResource,
    MapDrawObjectsTown,
    MapDrawObjectsArmy,

    EventWrapper
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
            this.map  = {};

            this.onUpdateDataFnLayer();

            if (window.env === 'develop') {
                var self = this;
                window.debugLand = function () {
                    self.getLand = function (x, y) {
                        if(self.map[y] === undefined || self.map[y][x] === undefined) {
                            return false;
                        }

                        return imageLoader.get('ground-debug');
                    };
                    mapInstance.draw();
                };

                if (localStorage.getItem('debugLand') == 'true') {
                    window.debugLand();
                }
            }
        },

        init: function () {
            if(this.$isInit) {
                return false;
            }

            this.$isInit = true;

            userService.getDeffer().deffer(DefferedTrigger.ON_GET_AND_UPDATE, function (userDomain) {
                this.$mapDI.setCenterCameraPosition(
                    userDomain.get('position').x,
                    userDomain.get('position').y
                );
            }.bind(this));

            jQuery(window).resize(function (e) {
                var camera = this.$mapDI.getCenterCameraPosition();
                this.$mapDI.reload();
                this.$mapDI.setCenterCameraPosition(camera.x, camera.y);
            }.bind(this));

            return true;
        },

        onUpdateDataFnLayer: function () {
            var self = this,
                location;

            this.$mapDI.updateDataLayer(function (point) {
                var x = point.mapX,
                    y = point.mapY;

                if(x < 0 || x >= 2000 || y < 0 || y >= 2000) {
                    return point.setShadow(true);
                }

                location = mapInstance.help.fromPlaceToId(x, y);
                var tmp;
                if(!(tmp = self.getLand(x, y, location))) {
                    return point.setShadow(true);
                }

                point.setGround(tmp);

                if((tmp = self.getDecoration(x, y, location))) {
                    point.setDecor(tmp);
                }

                point.setBuild(
                    self.getBuild(x, y, location)
                );

                return null;
            });
        },

        getLand: function(x, y) {
            if(this.map[y] === undefined || this.map[y][x] === undefined) {
                return false;
            }

            return imageLoader.get("ground-" +
                this.map[y][x][this.TRANSFER_ALIAS_LAND] + "-" +
                this.map[y][x][this.TRANSFER_ALIAS_LAND_TYPE]);
        },

        getDecoration: function(x, y) {
            if(this.map[y] === undefined || this.map[y][x] === undefined) {
                return false;
            }

            return imageLoader.get("decor-" + this.map[y][x][this.TRANSFER_ALIAS_DECOR]);
        },

        getBuild: function(x, y) {
            if(this.map[y] === undefined || this.map[y][x] === undefined) {
                return false;
            }

            switch(this.map[y][x][this.TRANSFER_ALIAS_BUILD]) {
                case this.BUILD_TOWNS:
                    return this.mapDrawObjectsTowns.getTownObject(
                        x,
                        y
                    );

                case this.BUILD_RESOURCES:
                    return this.mapDrawObjectsResource.getResourceObject(
                        x,
                        y
                    );

                case this.BUILD_EMPTY:
                    return false;

                default:
                    return false;
            }
        },

        getInfo: function (e) {
            var army,
                x = e.position.x,
                y = e.position.y,
                ev = new EventWrapper(e);

            if(this.map[y] === undefined || this.map[y][x] === undefined) {
                ev.setShadow(true);
                return ev;
            }

            ev.setShadow(false);

            ev.setLand(
                this.map[y][x][this.TRANSFER_ALIAS_LAND],
                this.map[y][x][this.TRANSFER_ALIAS_LAND_TYPE]
            );

            ev.setDecor(this.map[y][x][this.TRANSFER_ALIAS_DECOR]);

            switch(this.map[y][x][this.TRANSFER_ALIAS_BUILD]) {
                case this.BUILD_TOWNS:
                    ev.setBuild(
                        'town',
                        this.mapDrawObjectsTowns.getDetail(x, y)
                    );
                    break;

                case this.BUILD_RESOURCES:
                    ev.setBuild(
                        'resource',
                        this.mapDrawObjectsResource.getDetail(x, y)
                    );
                    break;
            }

            if ((army = this.mapDrawObjectsArmy.searchByPosition(x, y))) {
                _.each(army, function (layerItem) {
                    if (layerItem.isTriggerPoint([e.offsetX, e.offsetY])) {
                        ev.setUnit('army', layerItem.getDomain())
                    }
                });
            }

            return ev;
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

            this.$mapDI.draw();
        },

        getInstanceArmy: function () {
            return this.mapDrawObjectsArmy;
        }
    });

    return new Draw();
});