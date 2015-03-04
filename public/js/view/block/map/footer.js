define('view/block/map/footer', [
    'system/interval',
    'system/config',
    'service/standalone/map',
    'model/dummy',

    'factory/town',
    'factory/mapResources',
    'factory/army'
], function(
    systemInterval,
    systemConfig,
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
                resource: null,
                army_path: null
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
                default:
                    if (this.data.footer.get('army_path')) {
                        systemInterval.off(systemInterval.EVERY_1_SEC, this._onSecTick, this);
                        this.data.footer.set('army_path', null);
                    }

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

            this.data.footer.set('resource', domain);
            return true;
        },

        $focusOnArmy: function (x, y, idContainer) {
            var armyPath = null,
                pathItem,
                domain = factoryArmy.getFromPool(idContainer);

            if(domain === false) {
                return false;
            }

            if (domain.get('move_path')[0]) {
                pathItem = domain.get('move_path')[0];
                systemInterval.on(systemInterval.EVERY_1_SEC, this._onSecTick, this);

                armyPath = {
                    position: '0x0',
                    timeToComplete: pathItem.complete_after - (systemConfig.getTime() - pathItem.start_at)
                };
            }

            this.data.footer.set('army', domain);
            this.data.footer.set('army_path', armyPath);
            return true;
        },

        _onSecTick: function () {
            var domain = this.data.footer.get('army'),
                pathItem = domain.get('move_path')[0],
                armyPath = this.data.footer.get('army_path');

            if (!pathItem) {
                systemInterval.off(systemInterval.EVERY_1_SEC, this._onSecTick, this);
                this.data.footer.set('army_path', null);
                return;
            }

            armyPath.timeToComplete = pathItem.complete_after - (systemConfig.getTime() - pathItem.start_at);
            this.data.footer.set('army_path', armyPath);
            this.ractive.update();
        }
    });
});