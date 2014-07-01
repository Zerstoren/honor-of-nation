define('view/elements/map/mouse', [], function () {

    return Backbone.View.extend({
        initialize: function(service) {
            this.service = service;
            this.currentMovePosition = [-1, -1];
        },

        activateDrag: function() {
            this.$dragUserUsed = true;
        },

        deactivateDrag: function() {
            this.$dragUserUsed = false;
        },

        $afterDraw: function() {
            this.registerEvents([
                'mouseClick', 'mouseRightClick', 'mouseMiddleClick', 'mouseDoubleClick',
                'mouseMove',
                'mouseDragStart', 'mouseDragMove', 'mouseDragStop'
            ]);

            this.$dragStarted = false;
            this.$dragUserUsed = false;
            this.$dragMapBasePosition = [0, 0];

            this.$attachEvents();
            this.$activateSelfControl();
        },

        $attachEvents: function() {
            var self = this;

            this.$area.click(function(ev) {
                self.mouseClick(ev);
            });

            this.$area.mousedown(function(ev) {
                self.mouseDragStart(ev);
            });

            this.$area.dblclick(function(ev) {
                self.mouseDoubleClick(ev);
            });

            jQuery(document).mouseup(function(ev) {
                self.mouseDragStop(ev);
            });

            jQuery(document).mousemove(function(ev) {
                self.mouseMove(ev);
            });
        },

        mouseClick: function(ev) {
            var tmp = this.$getInfoForEvent(ev);

            if(tmp) {
                if(ev.which === 1) {
                    this.fireEvent('mouseClick', this.$getInfoForEvent(ev));
                } else if(ev.which === 3) {
                    this.fireEvent('mouseRightClick', this.$getInfoForEvent(ev));
                } else if(ev.which === 2) {
                    this.fireEvent('mouseMiddleClick', this.$getInfoForEvent(ev));
                }
            }
        },

        mouseDoubleClick: function(ev) {
            var tmp = this.$getInfoForEvent(ev);

            if(tmp) {
                this.fireEvent('mouseDoubleClick', this.$getInfoForEvent(ev));
            }
        },

        mouseMove: function(ev) {
            var tmp;

            if(this.$dragStarted === true) {
                this.mouseDragMove(ev);
            } else {
                tmp = this.$getInfoForEvent(ev);

                if(tmp && (tmp[0] !== this.currentMovePosition[0] || tmp[1] !== this.currentMovePosition[1])) {
                    this.currentMovePosition = tmp;
                    this.fireEvent('mouseMove', this.$getInfoForEvent(ev));
                }
            }
        },

        mouseDragStart: function(ev) {
            this.$dragStarted = true;
            this.fireEvent('mouseDragStart', ev);
        },

        mouseDragStop: function(ev) {
            if(this.$dragStarted === true) {
                this.fireEvent('mouseDragStop', ev);
                this.$dragStarted = false;
            }
        },

        mouseDragMove: function(ev) {
            /*if(ev.which === 0) {
                this.mouseDragStop(ev);
            } else {*/
            this.fireEvent('mouseDragMove', ev);
            //}

        },

        $activateSelfControl: function() {
            var self = this;

            this.subscribe('mouseDragStart', function(ev) {
                if(self.$dragUserUsed) {
                    return;
                }

                self.$dragMapBasePosition[0] = ev.clientX;
                self.$dragMapBasePosition[1] = ev.clientY;
            });

            this.subscribe('mouseDragStop', function() {
                return !self.$dragUserUsed;
            });

            this.subscribe('mouseDragMove', function(ev) {
                if(self.$dragUserUsed) {
                    return false;
                }

                var move = [
                    ev.clientX - self.$dragMapBasePosition[0],
                    ev.clientY - self.$dragMapBasePosition[1]
                ];

                self.$dragMapBasePosition[0] = ev.clientX;
                self.$dragMapBasePosition[1] = ev.clientY;

                self.$mapDrag(move);

                return true;
            });
        },

        $mapDrag: function(move) {
            var layer = this.$area.get(0),
                currentX = (layer.style.left ? parseInt(layer.style.left, 10) : 0) + move[0],
                currentY = (layer.style.top ? parseInt(layer.style.top, 10) : 0) + move[1],
                jump = [0, 0];

            if(currentX >= this.minShiftX) {
                jump[0] = (this.addedWidth - this.config.cellSize) / this.config.cellSize / -1;
            } else if(currentX <= this.maxShiftX) {
                jump[0] = (this.addedWidth - this.config.cellSize) / this.config.cellSize;
            }

            if(currentY >= this.minShiftY) {
                jump[1] = (this.addedHeight - this.config.cellSize) / this.config.cellSize / -1;
            } else if(currentY <= this.maxShiftY) {
                jump[1] = (this.addedHeight - this.config.cellSize) / this.config.cellSize;
            }

            if(jump[0] !== 0 || jump[1] !== 0) {
                this.correctLayerCoordinate(jump[0], jump[1]);
                currentX += (jump[0] * this.config.cellSize);
                currentY += (jump[1] * this.config.cellSize);
            }

            layer.style.left = currentX + 'px';
            layer.style.top = currentY + 'px';
        },

        $getInfoForEvent: function(ev) {
            var positionX, positionY, tmp,
                parent = ev.target;

            while(parent !== null && parent.nodeName !== 'TD') {
                parent = parent.parentNode;
            }

            if(parent === null || parent.parentNode.parentNode.id !== 'table-map') {
                return null;
            }

            tmp = parent.getAttribute('data-position').split('x');
            positionX = parseInt(tmp[0], 10) + this.positionX;
            positionY = parseInt(tmp[1], 10) + this.positionY;

            return [
                positionX,
                positionY,
                ev.target,
                ev
            ];
        }
    });
});

