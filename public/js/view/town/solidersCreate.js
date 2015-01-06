define('view/town/solidersCreate', [
    'view/elements/popup'
], function (
    ViewElementsPopup
) {
    return AbstractView.extend({
        events: {
            'click .create': 'onCreateUnit'
        },

        initialize: function () {
            this.template = this.getTemplate('town/createUnits/units');
            this.setPartials({
                equipmentUnitsItem: 'town/createUnits/createUnitsItem',
                unitsInProgress: 'town/createUnits/unitsInProgress'
            });
            this.initRactive();
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
        },

        setArmyQueue: function (collection) {
            this.set('armyQueue', collection);
        },

        setEquipmentUnitsCollection: function (collection) {
            this.set('equipmentUnits', collection);
            this.equipmentUnits = collection;
        },

        onCreateUnit: function (ev) {
            container = jQuery(ev.target).parents('.units_container');
            if (!container) {
                throw new Error("Clicked not in container");
            }

            var unitId = container.attr('data-id'),
                count = container.find('.count_to_create');

            this.trigger('create', unitId, count);
        }
    });
});