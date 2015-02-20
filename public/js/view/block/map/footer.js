define('view/block/map/footer', [
    'service/standalone/map',
    'model/dummy',

    'factory/town',
    'factory/mapResources',
    'factory/army'
], function(
    map,
    ModelDummy,

    factoryTown,
    factoryMapResources,
    factoryArmy
) {
    'use strict';

    return AbstractView.extend({
        initialize: function (holder) {
            this.holder = holder;
            this.template = this.getTemplate('block/map/footer');
            this.$lastFocusedType = null;
            this.$lastFocusedId = null;
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
            map.on('onMouseDoubleClickObject', this.onMouseDoubleClickObject, this);
        },

        onMouseMove: function (e) {
            this.data.footer.set('x', e.x);
            this.data.footer.set('y', e.y);
        },

        onFocusObject: function (x, y, type, idContainer) {
            if (this.data.footer.get('type') === type || this.$lastFocusedType) {
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

                case 'army':
                    this.$focusOnArmy(x, y, idContainer);
                    break;
            }
        },

        onMouseClickObject: function (x, y, type, idContainer) {
            this.data.footer.set('type', type);
            this.$lastFocusedType = type;
            this.$lastFocusedId = idContainer;

            switch(type) {
                case 'town':
                    this.$focusOnTown(x, y, idContainer);
                    break;

                case 'resource':
                    this.$focusOnResource(x, y, idContainer);
                    break;

                case 'army':
                    this.$focusOnArmy(x, y, idContainer);
                    break;
            }
        },

        onMouseDoubleClickObject: function (x, y, type, idContainer) {
            this.trigger('open', type, idContainer);
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
        },

        $focusOnArmy: function (x, y, idContainer) {
            var domain = factoryArmy.getFromPool(idContainer);

            if(domain === false) {
                return false;
            }

            this.data.footer.set('army', domain.attributes);
            return true;
        }
    });
});