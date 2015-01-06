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
            this.armyQueue = new CollectionArmyQueue();
            this.mainView = new ViewTownSolidersCreate();
            this.mainView.setArmyQueue(this.armyQueue);
            this.mainView.setEquipmentUnitsCollection(this.equipmentUnits);

            this.mainView.on('create', this.onCreateUnit, this);
        },

        render: function (holder, townDomain) {
            this.holder = holder;
            this.townDomain = townDomain;

            this.mainView.render(holder, townDomain);

            serviceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (user) {
                this.equipmentUnits.setUser(user);
                this.equipmentUnits.load();
            }.bind(this));

            this.armyQueue.setTown(townDomain);
            this.armyQueue.load();
        },

        onCreateUnit: function (unitId, count) {

        }
    });
});