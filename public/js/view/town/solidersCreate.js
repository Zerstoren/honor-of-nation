define('view/town/solidersCreate', [
    'view/elements/popup'
], function (
    ViewElementsPopup
) {
    return AbstractView.extend({
        initialize: function () {
            this.template = this.getTemplate('town/createUnits/units');
            this.setPartials({
                equipmentUnitsItem: 'town/createUnits/createUnitsItem'
            });
            this.initRactive();
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
        }
    });
});