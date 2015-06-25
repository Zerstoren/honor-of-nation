define('service/standalone/map/canvas/support', [], function () {
    var CustomLayerShift, CustomDragger;

    CustomLayerShift = atom.declare(LibCanvas.App.LayerShift, {
        limitCallback: null,
        setLimitCallback: function (callback) {
            this.limitCallback = callback;
        },

        addElementsShift: function () {

        },

        addShift: function method(shift, withElements) {
            shift = new LibCanvas.Point( shift);

            var limit = this.limitShift,
                current = this.shift;

            if (limit) {
                shift.x = atom.number.limit(shift.x, limit.from.x - current.x, limit.to.x - current.x);
                shift.y = atom.number.limit(shift.y, limit.from.y - current.y, limit.to.y - current.y);
            }

            current.move( shift );
            this.layer.dom.addShift( shift );

            if (this.limitCallback) {
                limit = this.limitShift,
                current = this.shift;

                if (current.x === 0 || current.y === 0 || current.x === limit.x || current.y === limit.y) {
                    this.limitCallback({
                        leftEdge:   current.x === 0,
                        topEdge:    current.y === 0,
                        rightEdge:  current.x === limit.x,
                        bottomEdge: current.y === limit.y
                    });
                }
            }

            return this;
        }
    });

    CustomDragger = atom.declare(LibCanvas.App.Dragger, {
        initialize: function(mouse) {
            this.bindMethods([ 'dragStart' ]);
            this.events = new atom.Events(this);

            this.mouse  = mouse;
            this.shifts = [];

            this._events = {
                down: this.dragStart
            };

            this.mouse.events.add( this._events );
            jQuery(document).on('mousemove', this.dragMove.bind(this));
            jQuery(document).on('mouseup', this.dragStop.bind(this));
        },

        start: function (callback) {
            if (callback !== undefined) {
                this.callback = callback;
            }
            this.started = true;
            return this;
        },

        stop: function () {
            this.started = false;
            return this;
        },

        dragStart: function (e) {
            if (this.started === false) return;
            if (!this.shouldStartDrag(e)) return;
            this.drag = true;
            this.events.fire( 'start', [ e ]);
        },

        /** @private */
        dragStop: function (e) {
            if (!this.drag) return;

            for (var i = this.shifts.length; i--;) {
                var shift = this.shifts[i];
                shift.addElementsShift();
            }

            this.drag = false;
            this.mouse.set(e, true);
            this.events.fire( 'stop', [ e ]);
        },

        dragMove: function method (e) {
            method.previous.call(this, e);
            this.mouse.set(e, true);
            this.events.fire( 'move', [ e ]);
        }
    });

    return {
        CustomDragger: CustomDragger,
        CustomLayerShift: CustomLayerShift
    };
});