define('service/standalone/map/gameMapItems/Draw', [], function () {
    return AbstractService.extend({
        initialize: function() {
//            this.registerEvents(['onSetPosition', 'onUpdate', 'postUpdate']);

            this.positionX = 0;
            this.positionY = 0;

            this.sumWidth = 0;
            this.sumHeight = 0;

            this.$updateDataFnLayer = null;
        },

        /**
         * add relative position of camera.
         * @param x
         * @param y
         */
        correctLayerCoordinate: function(x, y) {
            this.positionX += x;
            this.positionY += y;
            this.trigger('onSetPosition', [this.positionX, this.positionY]);
            this.update();
        },

        update: function() {
            var y, x, yLength, xLength, tr, td, position, drawData,
                table = this.$area.get(0);

            if(this.$updateDataFnLayer === null) {
                return;
            }

            if(window.console.time) {
                window.console.time('update');
            }

            this.trigger('onUpdate', []);

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

            this.trigger('postUpdate', []);

            if(window.console.timeEnd) {
                window.console.timeEnd('update');
            }
        },

        getDomCell: function(x, y) {
            x -= this.positionX;
            y -= this.positionY;
            return this.$area.find('#td-' + x + 'x' + y);
        },

        setUpdateDataFnLayer: function(fn) {
            this.$updateDataFnLayer = fn;
        },

        $drawMap: function() {
            var bufferRow, bufferCell, x, y, table,
                monitorSizeX = window.innerWidth,
                monitorSizeY = window.innerHeight;

            this.sumHeight = Math.round(monitorSizeY / this.config.cellSize);
            this.sumWidth = Math.round(monitorSizeX / this.config.cellSize);

            this.addedWidth = 384;
            this.addedHeight = 384;

            this.minShiftX = -this.config.cellSize;
            this.maxShiftX = (this.addedWidth * 2 - this.config.cellSize) / -1;

            this.minShiftY = -this.config.cellSize;
            this.maxShiftY = (this.addedHeight * 2 - this.config.cellSize) / -1;

            this.sumHeight += (this.addedHeight / this.config.cellSize) * 2;
            this.sumWidth += (this.addedWidth / this.config.cellSize) * 2;

            table = document.createElement('TABLE');
            table.id = 'table-map';

            for(y = 0; y < this.sumHeight; y += 1) {
                bufferRow = document.createElement('TR');
                for(x = 0; x < this.sumWidth; x += 1) {
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

            this.$layer.append(table);
            this.$area = jQuery(table);
            this.$area.attr('cellpadding', '0');
            this.$area.attr('cellspacing', '0');
            this.$area.css({
                left: (this.addedWidth) / -1,
                top:  (this.addedHeight) / -1
            });

            this.layerPosition = {
                left: (this.addedWidth) / -1,
                top: (this.addedHeight) / -1
            };

            this.$afterDraw();
        },

        clear: function () {
            this.$area.detach();
        }
    });
});
