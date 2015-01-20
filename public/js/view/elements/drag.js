define('view/elements/drag', [], function () {
    return AbstractView.extend({
        initialize: function (config) {
            this.showed = null;
            this.enabled = true;
            this.dragged = false;
            this.startedFrom = null;

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
                target,
                boundaryTarget;

            target = this.startedFrom;

            this.showed = cloneItem = target.clone();
            target.after(cloneItem);

            targetBounce = target[0].getBoundingClientRect();
            this.pseudoPosition.x = e.pageX - targetBounce.left;
            this.pseudoPosition.y = e.pageY - targetBounce.top;

            boundaryTarget = this.$config.destination[0].getBoundingClientRect();
            this.destinationPosition = {
                startY: boundaryTarget.top,
                endY: boundaryTarget.top + boundaryTarget.height,
                startX: boundaryTarget.left,
                endX: boundaryTarget.left + boundaryTarget.width
            };


            this.showed.addClass('draggable');
            this.showed.css({
                top: e.pageY - this.pseudoPosition.y,
                left: e.pageX - this.pseudoPosition.x
            });
        },

        onMouseDown: function (e) {
            var target = jQuery(e.target);

            this.dragged = true;
            this.position.x = e.pageX;
            this.position.y = e.pageY;
            this.startedFrom = target.is(this.$config.target) ? target : target.parents(this.$config.target);
        },

        onMouseMove: function (e) {
            if (!this.dragged) {
                return false;
            }

            var moveOut = this.$config.moveOut;
            if (
                this.showed === null &&
                (
                    (e.pageX <= this.position.x - moveOut || this.position.x + moveOut <= e.pageX) ||
                    (e.pageY <= this.position.y - moveOut || this.position.y + moveOut <= e.pageY)
                )
            ) {
                this.attachDuplicate(e);
            } else if (!this.showed) {
                return false;
            }

            this.showed.css({
                top: e.pageY - this.pseudoPosition.y,
                left: e.pageX - this.pseudoPosition.x
            });

            if (
                (this.destinationPosition.startX < e.pageX || this.destinationPosition.endX > e.pageX) &&
                (this.destinationPosition.startY < e.pageY || this.destinationPosition.endY > e.pageY)
            ) {
                console.log('Add');
                this.$config.destination.addClass('destinated');
            } else {
                console.log('Ren');
                console.log(this.destinationPosition.startX, e.pageX, this.destinationPosition.endX, e.pageX)
                this.$config.destination.removeClass('destinated');
            }
        },

        onMouseUp: function (e) {
            this.dragged = false;

            this.position.x = null;
            this.position.y = null;

            this.showed.detach();
            this.showed = null;
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