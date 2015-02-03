define('view/elements/drag', [], function () {
    return Backbone.View.extend({
        initialize: function (config) {
            this.showed = null;
            this.enabled = true;
            this.dragged = false;
            this.startedFrom = null;
            this.destinated = false;
            this.massiveTarget = null;

            this.position = {
                x: null,
                y: null
            };

            this.pseudoPosition = {
                x: 0,
                y: 0
            };

            this.$config = {
                section: config.section,
                target: config.target,
                destination: config.destination,
                handler: config.handler,
                massiveDestination: config.massiveDestination || false,
                onStart: config.onStart || null,
                onStop: config.onStop || null,
                moveOut: config.moveOut || 10
            };

            this.addEventListeners();
        },

        enable: function () {
            this.enabled = true;
        },

        disable: function () {
            this.enabled = false;
        },

        remove: function () {
            this.removeEventListeners();
        },

        attachDuplicate: function (e) {
            var cloneItem,
                targetBounce,
                target;

            target = this.startedFrom;
            this.showed = cloneItem = target.clone();

            if (this.$config.massiveDestination) {
                this.destinationPosition = [];
                this.destination = this.$config.section.find(this.$config.destination);
                this.destination.each(function (num, item) {
                    if (item === cloneItem.prevObject[0]) {
                        return;
                    }

                    var clientBound = item.getBoundingClientRect();
                    clientBound.element = item;
                    this.destinationPosition.push(clientBound);
                }.bind(this));
            } else {
                this.destination = this.$config.section.find(this.$config.destination);
                this.destinationPosition = this.destination[0].getBoundingClientRect();
            }

            target.after(cloneItem);

            targetBounce = target[0].getBoundingClientRect();
            this.pseudoPosition.x = e.pageX - targetBounce.left;
            this.pseudoPosition.y = e.pageY - targetBounce.top;

            this.showed.addClass('draggable');
            this.showed.css({
                position: 'fixed',
                top: e.pageY - this.pseudoPosition.y,
                left: e.pageX - this.pseudoPosition.x
            });
        },

        onMouseDown: function (e) {
            if (!this.enabled) {
                return;
            }

            var target = jQuery(e.target);

            this.dragged = true;
            this.position.x = e.pageX;
            this.position.y = e.pageY;
            this.startedFrom = target.is(this.$config.target) ? target : target.parents(this.$config.target);
        },

        _isInPosition: function (destinationPosition, pagePosition) {
            return (destinationPosition.left < pagePosition.pageX && destinationPosition.right > pagePosition.pageX) &&
                (destinationPosition.top < pagePosition.pageY && destinationPosition.bottom > pagePosition.pageY);
        },

        onMouseMove: function (e) {
            if (!this.dragged) {
                return;
            }

            var i, destinated, target,
                moveOut = this.$config.moveOut;

            if (
                this.showed === null &&
                (
                    (e.pageX <= this.position.x - moveOut || this.position.x + moveOut <= e.pageX) ||
                    (e.pageY <= this.position.y - moveOut || this.position.y + moveOut <= e.pageY)
                )
            ) {
                if (this.$config.onStart) {
                    this.$config.onStart();
                }

                this.attachDuplicate(e);

            } else if (!this.showed) {
                return;
            }

            this.showed.css({
                top: e.pageY - this.pseudoPosition.y,
                left: e.pageX - this.pseudoPosition.x
            });

            if (this.$config.massiveDestination) {
                destinated = this.destinated;

                for (i = 0; i < this.destinationPosition.length; i++) {
                    if (this._isInPosition(this.destinationPosition[i], e)) {
                        destinated = true;
                        target = this.destinationPosition[i].element;
                        break;
                    } else {
                        destinated = false;
                    }
                }

                if (destinated && (this.massiveTarget !== null && this.massiveTarget !== target)) {
                    destinated = false;
                }

                if (destinated) {
                    this.destinated = true;
                    this.massiveTarget = target;
                    jQuery(target).addClass('destinated');
                } else if (!destinated) {
                    this.destinated = false;
                    this.massiveTarget = null;
                    this.destination.removeClass('destinated');
                }
            } else {
                if (!this.destinated && this._isInPosition(this.destinationPosition, e)) {
                    this.destinated = true;
                    this.destination.addClass('destinated');
                } else {
                    this.destinated = false;
                    this.destination.removeClass('destinated');
                }
            }
        },

        onMouseUp: function (e) {
            if (!this.dragged) {
                return;
            }

            this.dragged = false;

            this.position.x = null;
            this.position.y = null;

            if (this.showed) {
                if (this.$config.massiveDestination) {
                    for (var i = 0; i < this.destinationPosition.length; i++) {
                        if (this._isInPosition(this.destinationPosition[i], e)) {
                            this.destinated = false;
                            this.destination.removeClass('destinated');
                            this.$config.handler(
                                this.showed,
                                jQuery(this.destinationPosition[i].element)
                            );
                            break;
                        }
                    }
                } else {
                    if (this._isInPosition(this.destinationPosition, e)) {
                        this.destinated = false;
                        this.destination.removeClass('destinated');
                        this.$config.handler(
                            this.showed,
                            this.destination
                        );
                    }
                }

                this.showed.detach();
                this.showed = null;

            }

            if (this.$config.onStop) {
                this.$config.onStop();
            }
        },

        addEventListeners: function () {
            this.onMouseMove = this.onMouseMove.bind(this);
            this.onMouseDown = this.onMouseDown.bind(this);
            this.onMouseUp = this.onMouseUp.bind(this);

            this.$config.section.on('mousedown', this.$config.target, this.onMouseDown);
            jQuery(document).on('mousemove', this.onMouseMove);
            jQuery(document).on('mouseup', this.onMouseUp);
        },

        removeEventListeners: function () {
            this.$config.section.off('mousedown', this.$config.target, this.onMouseDown);
            jQuery(document).off('mousemove', this.onMouseMove);
            jQuery(document).off('mouseup', this.onMouseUp);
        }
    });
});