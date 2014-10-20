define('view/block/map/footer', [
    'service/standalone/map',
    'model/dummy',

    'factory/town',
    'factory/mapResources'
], function(
    map,
    ModelDummy,

    factoryTown,
    factoryMapResources
) {
    'use strict';

    return AbstractView.extend({
        initialize: function (holder) {
            this.holder = holder;
            this.template = this.getTemplate('block/map/footer');
            this.$lastFocusedContainer = null;
            this.data.footer = new ModelDummy({
                x: '-',
                y: '-',
                type: null,
                town: null,
                resource: null
            });

            this.initRactive();
        },

        render: function () {
            this.holder.append(this.$el);
            map.on('mouseMove', this.onMouseMove, this);
            map.on('onMouseMoveObject', this.onFocusObject, this);

            map.on('onMouseClickObject', this.onMouseClickObject, this);
        },

        onMouseMove: function (e) {
            this.data.footer.set('x', e.x);
            this.data.footer.set('y', e.y);
        },

        onFocusObject: function (x, y, type, idContainer) {
            if (this.data.footer.get('type') === type || this.$lastFocusedContainer) {
                return;
            }

            this.data.footer.set('type', type);

            switch(type) {
                case 'town':
                    this.$focusOnTown(x, y, idContainer);
                    break;

                case 'resource':
                    this.$focusOnResource(x, y, idContainer);
                    break;
            }
        },

        onMouseClickObject: function (x, y, type, idContainer) {
            this.data.footer.set('type', type);
            this.$lastFocusedContainer = type;

            switch(type) {
                case 'town':
                    this.$focusOnTown(x, y, idContainer);
                    break;

                case 'resource':
                    this.$focusOnResource(x, y, idContainer);
                    break;
            }
        },

        $focusOnTown: function (x, y, idContainer) {
            var domain = factoryTown.getFromPool(idContainer);

            if (domain === false) {
                return false;
            }

            this.data.footer.set('town', domain);

            return true;
        },

        $focusOnResource: function (x, y, idContainer) {
            var domain = factoryMapResources.getFromPool(idContainer);

            if(domain === false) {
                return false;
            }

            this.data.footer.set('resource', domain.attributes);

            return true;
        }
    });
});