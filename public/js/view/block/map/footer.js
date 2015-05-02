define('view/block/map/footer', [
    'system/interval',
    'system/config',
    'service/standalone/map',
    'model/dummy',

    'view/elements/tooltip',

    'factory/town',
    'factory/mapResources',
    'factory/army'
], function(
    systemInterval,
    systemConfig,
    map,
    ModelDummy,

    ViewElementsTooltip,

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
            this.data.footer = new ModelDummy({
                x: '-',
                y: '-',
                type: null,
                town: null,
                resource: null,
                time_to_complete: null,
                army_power: null
            });
            this.tooltipManager = new ViewElementsTooltip(this, '*[data-hint]', {
                placement: 'top'
            });
            this.initRactive();
        },

        events: {

        },

        render: function () {
            this.holder.append(this.$el);
            map.on('mouseMove', this.onMouseMove, this);
            map.on('onMouseMoveObject', this.onFocusObject, this);

            map.on('onMouseClickObject', this.onMouseClickObject, this);
            map.on('onMouseDoubleClickObject', this.onMouseDoubleClickObject, this);
        },

        onMouseMove: function (e) {
            this.data.footer.set('x', e.position.x);
            this.data.footer.set('y', e.position.y);
        },

        onFocusObject: function (ev) {
            var type, domain;

            if (ev.unit()) {
                type = ev.unitType();
                domain = ev.unit();
            } else if (ev.build()) {
                type = ev.buildType();
                domain = ev.build();
            }


            if (this.data.footer.get('type') === type || this.$lastFocusedType) {
                return;
            }

            this.data.footer.set('type', type);

            switch(type) {
                case 'town':
                    this.$focusOnTown(domain);
                    break;

                case 'resource':
                    this.$focusOnResource(domain);
                    break;

                case 'army':
                    this.$focusOnArmy(domain);
                    break;
            }
        },

        onMouseClickObject: function (ev) {
            var type, domain;

            if (ev.unit()) {
                type = ev.unitType();
                domain = ev.unit();
            } else if (ev.build()) {
                type = ev.buildType();
                domain = ev.build();
            } else {
                type = null;

            }

            this.data.footer.set('type', type);
            this.$lastFocusedType = type;

            switch(type) {
                case 'town':
                    this.$focusOnTown(domain);
                    break;

                case 'resource':
                    this.$focusOnResource(domain);
                    break;

                case 'army':
                    this.$removeFocusArmy();
                    this.$focusOnArmy(domain);
                    break;
            }
        },

        onMouseDoubleClickObject: function (ev) {
            // TODO осмотреть слушателей
            this.trigger('open', ev.buildType, ev.build);
        },

        $focusOnTown: function (domain) {
            if (domain === null) {
                return false;
            }

            this.data.footer.set('town', domain);

            return true;
        },

        $focusOnResource: function (domain) {
            if(domain === null) {
                return false;
            }

            this.data.footer.set('resource', domain);
            return true;
        },

        $focusOnArmy: function (domain) {
            var timeToComplete = null,
                pathItem, power;

            if(domain === false) {
                return false;
            }

            if (domain.get('move_path')[0]) {
                pathItem = domain.get('move_path')[0];
                timeToComplete = pathItem.complete_after - (systemConfig.getTime() - pathItem.start_at);
            }

            this.$el.find('.army_mode .mode').off('click.mode');
            this.$el.find('.army_mode .mode').on("click.mode", function (ev) {
                var mode = jQuery(ev.target).attr('data-mode');
                this.trigger('change_mode', domain, mode);
            }.bind(this));

            power = domain.get('power') + (
                (systemConfig.getTime() - domain.get('last_power_update')) * systemConfig.getPowerRestore()
            );

            if (power >= 100 && domain.get('power') <= 101) {
                power = 100;
            }

            this.data.footer.set('army', domain);
            this.data.footer.set('time_to_complete', timeToComplete);
            this.data.footer.set('army_power', power);
            systemInterval.on(systemInterval.EVERY_1_SEC, this._onSecTick, this);
            return true;
        },

        $removeFocusArmy: function () {
            if (this.data.footer.get('time_to_complete')) {
                systemInterval.off(systemInterval.EVERY_1_SEC, this._onSecTick, this);
                this.data.footer.set('time_to_complete', null);
            }

            this.$el.find('.army_mode .mode').off('click.mode');
        },

        _onSecTick: function () {
            var power,
                domain = this.data.footer.get('army'),
                pathItem = domain.get('move_path')[0],
                time_to_complete = this.data.footer.get('time_to_complete');

            if (pathItem) {
                time_to_complete = pathItem.complete_after - (systemConfig.getTime() - pathItem.start_at);
                this.data.footer.set('time_to_complete', time_to_complete);
            } else {
                this.data.footer.set('time_to_complete', null);
            }

            power = domain.get('power') + (
                (systemConfig.getTime() - domain.get('last_power_update')) * systemConfig.getPowerRestore()
            );

            if (power >= 100 && domain.get('power') <= 101) {
                power = 100;
            }

            this.data.footer.set('army_power', power);
        }
    });
});