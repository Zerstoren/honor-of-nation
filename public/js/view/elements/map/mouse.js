define('view/elements/map/mouse', [], function () {

    return AbstractView.extend({
//        events: {
//            'click': 'mouseClick',
//            'dblclick': 'mouseDoubleClick',
//            'mousedown': 'mouseDragStart',
//            'mousemove global': 'mouseMove',
//            'mouseup global': 'mouseDragStop'
//        },

        initialize: function(service) {
            this.service = service;
            this.currentMovePosition = [-1, -1];


            this.$dragStarted = false;
            this.$dragUserUsed = false;
            this.$dragMapBasePosition = [0, 0];

            this.$activateSelfControl();
        },

        activateDrag: function() {
            this.$dragUserUsed = true;
        },

        deactivateDrag: function() {
            this.$dragUserUsed = false;
        },

        afterRender: function () {
            var self = this;
            this.$area = this.service.$layer.find('table');
            this.area = this.$area.get(0);

            this.area.addEventListener('click', function (e) {
                self.mouseClick(e);
            });

            this.area.addEventListener('dblclick', function (e) {
                self.mouseDoubleClick(e);
            });

            this.area.addEventListener('mousedown', function (e) {
                self.mouseDragStart(e);
            });

            document.addEventListener('mousemove', function (e) {
                self.mouseDragMove(e);
            });

            document.addEventListener('mouseup', function (e) {
                self.mouseDragStop(e);
            });
        },

        mouseClick: function(ev) {
            var tmp = this.$getInfoForEvent(ev);

            if(tmp) {
                if(ev.which === 1) {
                    this.trigger('mouseClick', this.$getInfoForEvent(ev));
                } else if(ev.which === 3) {
                    this.trigger('mouseRightClick', this.$getInfoForEvent(ev));
                } else if(ev.which === 2) {
                    this.trigger('mouseMiddleClick', this.$getInfoForEvent(ev));
                }
            }
        },

        mouseDoubleClick: function(ev) {
            var tmp = this.$getInfoForEvent(ev);

            if(tmp) {
                this.trigger('mouseDoubleClick', this.$getInfoForEvent(ev));
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
                    this.trigger('mouseMove', this.$getInfoForEvent(ev));
                }
            }
        },

        mouseDragStart: function(ev) {
            this.$dragStarted = true;
            if(this.$dragUserUsed) {
                return;
            }

            this.$dragMapBasePosition[0] = ev.clientX;
            this.$dragMapBasePosition[1] = ev.clientY;
        },

        mouseDragStop: function(ev) {
            if(this.$dragStarted === true) {
                this.$dragStarted = false;
            }
        },

        mouseDragMove: function(ev) {
            if(ev.which === 0) {
                this.mouseDragStop(ev);
                return;
            }

            if(this.$dragUserUsed) {
                return;
            }

            var move = [
                ev.clientX - this.$dragMapBasePosition[0],
                ev.clientY - this.$dragMapBasePosition[1]
            ];

            this.$dragMapBasePosition[0] = ev.clientX;
            this.$dragMapBasePosition[1] = ev.clientY;

            this.$mapDrag(move);
//            }
        },

        $activateSelfControl: function() {
//            this.on('mouseDragStart', function(ev) {
//                if(this.$dragUserUsed) {
//                    return;
//                }
//
//                this.$dragMapBasePosition[0] = ev.clientX;
//                this.$dragMapBasePosition[1] = ev.clientY;
//            }, this);
//
//            this.on('mouseDragStop', function() {
//                return !this.$dragUserUsed;
//            }, this);
//
//
//            this.on('mouseDragMove', function(ev) {
//                if(this.$dragUserUsed) {
//                    return false;
//                }
//
//                var move = [
//                    ev.clientX - this.$dragMapBasePosition[0],
//                    ev.clientY - this.$dragMapBasePosition[1]
//                ];
//
//                this.$dragMapBasePosition[0] = ev.clientX;
//                this.$dragMapBasePosition[1] = ev.clientY;
//
//                this.$mapDrag(move);
//
//                return true;
//            }, this);
        },

        $mapDrag: function(move) {
            var layer = this.area,
                currentX = (layer.style.left ? parseInt(layer.style.left, 10) : 0) + move[0],
                currentY = (layer.style.top ? parseInt(layer.style.top, 10) : 0) + move[1],
                jump = [0, 0];

            if(currentX >= this.service.minShiftX) {
                jump[0] = (this.service.addedWidth - this.service.config.cellSize) / this.service.config.cellSize / -1;
            } else if(currentX <= this.service.maxShiftX) {
                jump[0] = (this.service.addedWidth - this.service.config.cellSize) / this.service.config.cellSize;
            }

            if(currentY >= this.service.minShiftY) {
                jump[1] = (this.service.addedHeight - this.service.config.cellSize) / this.service.config.cellSize / -1;
            } else if(currentY <= this.service.maxShiftY) {
                jump[1] = (this.service.addedHeight - this.service.config.cellSize) / this.service.config.cellSize;
            }

            if(jump[0] !== 0 || jump[1] !== 0) {
                this.service.draw.correctLayerCoordinate(jump[0], jump[1]);
                currentX += (jump[0] * this.service.config.cellSize);
                currentY += (jump[1] * this.service.config.cellSize);
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

