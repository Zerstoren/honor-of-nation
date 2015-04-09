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

        dragStart: function (e) {
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
            this.events.fire( 'stop', [ e ]);
        }
    });

    return {
        CustomDragger: CustomDragger,
        CustomLayerShift: CustomLayerShift
    };
});