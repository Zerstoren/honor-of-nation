define('service/town/solidersCreate', [
    'view/town/solidersCreate',
    'collection/armyQueue',
    'collection/equipment/unit',

    'service/standalone/user'
], function (
    ViewTownSolidersCreate,
    CollectionArmyQueue,
    CollectionEquipmentUnits,

    serviceStandaloneUser
) {

    return AbstractService.extend({
        initialize: function () {
            this.equipmentUnits = new CollectionEquipmentUnits();
            this.mainView = new ViewTownSolidersCreate();
            //this.mainView.setArmyQueue();
            this.mainView.setEquipmentUnitsCollection(this.equipmentUnits);
        },

        render: function (holder, townDomain) {
            this.holder = holder;
            this.townDomain = townDomain;

            this.mainView.render(holder, townDomain);

            serviceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (user) {
                this.equipmentUnits.setUser(user);
                this.equipmentUnits.load();
            }.bind(this));
        }
    });
});