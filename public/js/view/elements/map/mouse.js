define('view/elements/map/mouse', [], function () {

    return AbstractView.extend({
        events: {
            'click td': 'mouseClick',
            'dblclick td': 'mouseDoubleClick',
            'mousedown td': 'mouseDragStart',
            'mousemove global': 'mouseMove',
            'mouseup global': 'mouseDragStop'
        },

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
            this.$el = this.service.$layer.find('table');
            this.el = this.$el.get(0);
            this.delegateEvents();
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
            this.trigger('mouseDragStart', ev);
        },

        mouseDragStop: function(ev) {
            if(this.$dragStarted === true) {
                this.trigger('mouseDragStop', ev);
                this.$dragStarted = false;
            }
        },

        mouseDragMove: function(ev) {
            /*if(ev.which === 0) {
                this.mouseDragStop(ev);
            } else {*/
            this.trigger('mouseDragMove', ev);
            //}

        },

        $activateSelfControl: function() {
            this.on('mouseDragStart', function(ev) {
                if(this.$dragUserUsed) {
                    return;
                }

                this.$dragMapBasePosition[0] = ev.clientX;
                this.$dragMapBasePosition[1] = ev.clientY;
            }, this);

            this.on('mouseDragStop', function() {
                return !this.$dragUserUsed;
            }, this);


            this.on('mouseDragMove', function(ev) {
                if(this.$dragUserUsed) {
                    return false;
                }

                var move = [
                    ev.clientX - this.$dragMapBasePosition[0],
                    ev.clientY - this.$dragMapBasePosition[1]
                ];

                this.$dragMapBasePosition[0] = ev.clientX;
                this.$dragMapBasePosition[1] = ev.clientY;

                this.$mapDrag(move);

                return true;
            }, this);
        },

        $mapDrag: function(move) {
            var layer = this.el,
                currentX = (layer.style.left ? parseInt(layer.style.left, 10) : 0) + move[0],
                currentY = (layer.style.top ? parseInt(layer.style.top, 10) : 0) + move[1],
                jump = [0, 0];

            if(currentX >= this.service.minShiftX) {
                jump[0] = (this.service.addedWidth - this.service.config.cellSize) / this.service.config.cellSize / -1;
            } else if(currentX <= this.maxShiftX) {
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

