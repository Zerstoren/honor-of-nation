define('view/elements/map/draw', [], function () {
    "use strict";

    return AbstractView.extend({
        initialize: function(service) {
            // events: 'onSetPosition', 'onUpdate', 'postUpdate']
            this.service = service;

            this.positionX = 0;
            this.positionY = 0;

            this.sumWidth = 0;
            this.sumHeight = 0;
        },

        /**
         * add relative position of camera.
         * @param x
         * @param y
         */
        correctLayerCoordinate: function(x, y) {
            this.positionX += x;
            this.positionY += y;
            this.trigger('onSetPosition', this.positionX, this.positionY);
//            this.update();
        },

        getMapHeight: function() {
            return this.service.sumHeight;
        },

        getMapWidth: function() {
            return this.service.sumWidth;
        },

        /**
         * Set current position from top-left corner
         * @param x
         * @param y
         */
        setPosition: function(x, y) {
            this.positionX = x;
            this.positionY = y;
            this.trigger('onSetPosition', x, y);
//            this.update();
        },

        /**
         * Return current camera position
         *
         * @returns {Array}
         */
        getPosition: function() {
            return [this.positionX, this.positionY];
        },

        /**
         * set current camera position from center of monitor
         * @param x
         * @param y
         */
        setCameraPosition: function(x, y) {
            this.setPosition(
                x - parseInt(this.getMapWidth() / 2, 10),
                y - parseInt(this.getMapHeight() / 2, 10)
            );
        },

        update: function() {
            var y, x, yLength, xLength, tr, td, position, drawData,
                table = this.$area.get(0);

            if(window.console.time) {
                window.console.time('update');
            }

            this.trigger('onUpdate');

            yLength = table.childNodes.length;
            for(y = 0; y < yLength; y += 1) {
                tr = table.childNodes[y];
                xLength = tr.childNodes.length;

                for(x = 0; x < xLength; x += 1) {
                    td = tr.childNodes[x];
                    position = td.getAttribute('data-position').split('x');
                    position[0] = parseInt(position[0], 10) + this.positionX;
                    position[1] = parseInt(position[1], 10) + this.positionY;

                    if(td.childNodes[4].innerHTML) {
                        td.childNodes[4].innerHTML = '';
                    }

                    drawData = this.$updateDataFnLayer(position[0], position[1]);
                    td.className = drawData.join(" ");
                }
            }

            this.trigger('postUpdate');

            if(window.console.timeEnd) {
                window.console.timeEnd('update');
            }
        },

        getDomCell: function(x, y) {
            x -= this.positionX;
            y -= this.positionY;
            return this.$area.find('#td-' + x + 'x' + y);
        },

        $updateDataFnLayer: function (x, y) {
            if(x < 0 || x >= 2000 || y < 0 || y >= 2000) {
                return ['no_map'];
            }

            var tmp, classList = [];
            tmp = this.$getLand(x, y);

            if(!tmp) {
                return ['shadow'];
            }

            classList.push(tmp);

            tmp = this.$getDecoration(x, y);
            if(tmp) {
                classList.push(tmp);
            }

            tmp = this.$getBuild(x, y);
            if(tmp) {
                classList.push(tmp);
            }

            return classList;
        },

        $getLand: function(x, y) {
            if(this.service.map[y] === undefined || this.service.map[y][x] === undefined) {
                return 'shadow';
            }

            return "land-" +
                this.service.map[y][x][this.service.TRANSFER_ALIAS_LAND] + "-" +
                this.service.map[y][x][this.service.TRANSFER_ALIAS_LAND_TYPE];
        },

        $getDecoration: function(x, y) {
            if(this.service.map[y] === undefined || this.service.map[y][x] === undefined) {
                return false;
            }

            return "decor-" + this.service.map[y][x][this.service.TRANSFER_ALIAS_DECOR];
        },

        $getBuild: function(x, y) {
            if(this.service.map[y] === undefined || this.service.map[y][x] === undefined) {
                return false;
            }

            switch(this.service.map[y][x][this.service.TRANSFER_ALIAS_BUILD]) {
                case this.service.BUILD_TOWNS:
                    return this.this.serviceObjectsTownsDI.getBuildObject(
                        x,
                        y,
                        this.service.map[y][x][this.service.TRANSFER_ALIAS_BUILD_TYPE]
                    );

                case this.service.BUILD_RESOURCES:
                    return this.this.serviceObjectsResourceDI.getResourceObject(
                        x,
                        y,
                        this.service.map[y][x][this.service.TRANSFER_ALIAS_BUILD_TYPE]
                    );

                case this.service.BUILD_EMPTY:
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
                            if(this.service.map[y] === undefined) {
                                this.service.map[y] = {};
                            }
    
                            this.service.map[y][x] = map[y][x];
                        }
                    }
                }
            }
    
            this.update();
        },

        $drawMap: function() {
            var bufferRow, bufferCell, x, y, table,
                monitorSizeX = window.innerWidth,
                monitorSizeY = window.innerHeight,
                cellSize = this.service.config.cellSize;

            this.service.sumHeight = Math.round(monitorSizeY / cellSize);
            this.service.sumWidth = Math.round(monitorSizeX / cellSize);

            this.service.addedWidth = 384;
            this.service.addedHeight = 384;

            this.service.minShiftX = -cellSize;
            this.service.maxShiftX = (this.service.addedWidth * 2 - cellSize) / -1;

            this.service.minShiftY = -cellSize;
            this.service.maxShiftY = (this.service.addedHeight * 2 - cellSize) / -1;

            this.service.sumHeight += (this.service.addedHeight / cellSize) * 2;
            this.service.sumWidth += (this.service.addedWidth / cellSize) * 2;

            table = document.createElement('TABLE');
            table.id = 'table-map';

            for(y = 0; y < this.service.sumHeight; y += 1) {
                bufferRow = document.createElement('TR');
                for(x = 0; x < this.service.sumWidth; x += 1) {
                    bufferCell = document.createElement('TD');
                    bufferCell.setAttribute('data-position', x + 'x' + y);
                    bufferCell.id = 'td-' + x + 'x' + y;
                    bufferRow.appendChild(bufferCell);
                    bufferCell.innerHTML =
                        '<div class="level0"></div>' +
                        '<div class="level1"></div>' +
                        '<div class="level2"></div>' +
                        '<div class="level3"></div>' +
                        '<div class="container"></div>';
                }

                table.appendChild(bufferRow);
            }

            this.service.$layer.append(table);
            this.$area = jQuery(table);
            this.$area.attr('cellpadding', '0');
            this.$area.attr('cellspacing', '0');
            this.$area.css({
                left: (this.addedWidth) / -1,
                top:  (this.addedHeight) / -1
            });
        }
    });
});