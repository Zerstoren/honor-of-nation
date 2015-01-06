define('view/town/solidersCreate', [
    'view/elements/popup',

    'system/config',
    'system/interval'
], function (
    ViewElementsPopup,

    config,
    interval
) {
    return AbstractView.extend({
        events: {
            'click .create': 'onCreateUnit',
            'click .cancel': 'onCancelUnit'
        },

        initialize: function () {
            this.template = this.getTemplate('town/createUnits/units');
            this.setPartials({
                equipmentUnitsItem: 'town/createUnits/createUnitsItem',
                unitsInProgress: 'town/createUnits/unitsInProgress'
            });
            this.initRactive();

            interval.on(interval.EVERY_1_SEC, this.updateQueue, this);
        },

        data: {
            armyQueue: null,
            equipmentUnits: null,
            createCount: 1
        },

        render: function (holder) {
            holder.append(this.$el);

            this.popupUnits = new ViewElementsPopup(
                this.$el, {
                    liveTarget: '.units_container',
                    timeout: 100,
                    align: 'left'
                }
            );

            this.popupQueue = new ViewElementsPopup(
                this.$el, {
                    timeout: 100,
                    liveTarget: '.triangle',
                    ignoreTop: true,
                    align: 'left'
                }
            );
        },

        setArmyQueue: function (collection) {
            this.armyQueue = collection;
        },

        setEquipmentUnitsCollection: function (collection) {
            this.set('equipmentUnits', collection);
            this.equipmentUnits = collection;
        },

        updateQueue: function () {
            if (!this.armyQueue) {
                return;
            }

            var i,
                item,
                tmp,
                armyQueue = this.armyQueue,
                result = [],
                firstSection = {};

            for (i = 0; i < armyQueue.length; i++) {
                item = armyQueue.at(i);

                tmp = {
                    _id: item.get('_id'),
                    type: item.get('unit_data').type,
                    count: item.get('count'),
                    timeToCreate: item.get('complete_after')
                };

                if (i === 0) {
                    tmp.timeToComplete = item.get('complete_after') - (config.getTime() - item.get('start_at'));
                    tmp.percentComplete = 100 - parseInt(((config.getTime() - item.get('start_at')) / item.get('complete_after')) * 100, 10);

                    firstSection = tmp;
                } else {
                    result.push(tmp);
                }
            }

            if (_.isEmpty(firstSection)) {
                firstSection = false;
            }

            result.reverse();

            this.set('firstSection', firstSection);
            this.set('armyQueue', result);
        },

        onCreateUnit: function (ev) {
            var count, unitId, container = jQuery(ev.target).parents('.units_container');
            if (!container) {
                throw new Error("Clicked not in container");
            }

            unitId = container.attr('data-id');
            count = container.find('.count_to_create').val();

            this.trigger('create', unitId, count);
        },

        onCancelUnit: function (ev) {
            var _id = jQuery(ev.target).attr('data-id');
            this.trigger('remove', _id);
        }
    });
});