define('service/standalone/map/gameMapItems/Access', [], function () {
    return AbstractService.extend({
        getMapHeight: function() {
            return this.sumHeight;
        },

        getMapWidth: function() {
            return this.sumWidth;
        },

        /**
         * Set current position from top-left corner
         * @param x
         * @param y
         */
        setPosition: function(x, y) {
            this.positionX = x;
            this.positionY = y;
            this.trigger('onSetPosition', [x, y]);
            this.update();
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
        }
    });
});