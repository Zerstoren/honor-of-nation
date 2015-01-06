define('service/town/solidersCreate', [
    'view/town/solidersCreate',
    'collection/armyQueue',
    'collection/equipment/unit',

    'service/standalone/user',
    'service/standalone/messages',

    'gateway/armyQueue'
], function (
    ViewTownSolidersCreate,
    CollectionArmyQueue,
    CollectionEquipmentUnits,

    serviceStandaloneUser,
    serviceStandaloneMessages,

    gatewayArmyQueue
) {

    return AbstractService.extend({
        initialize: function () {
            this.equipmentUnits = new CollectionEquipmentUnits();
            this.armyQueue = new CollectionArmyQueue();
            this.mainView = new ViewTownSolidersCreate();
            this.mainView.setArmyQueue(this.armyQueue);
            this.mainView.setEquipmentUnitsCollection(this.equipmentUnits);

            this.mainView.on('create', this.onCreateUnit, this);
            this.mainView.on('remove', this.onRemoveUnit, this);

            serviceStandaloneMessages.on('unitsUpdate', this.onUnitsUpdate, this);
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
            gatewayArmyQueue.create(this.townDomain, unitId, count, function () {
                this.armyQueue.load();
            }.bind(this));
        },

        onRemoveUnit: function (_id) {
            gatewayArmyQueue.remove(this.townDomain, _id, function () {
                this.armyQueue.load();
            }.bind(this));
        },

        onUnitsUpdate: function (townId, armyQueue) {
            if (townId !== this.townDomain.get('_id')) {
                return; // Data for other town
            }

            this.armyQueue.reset();
            this.armyQueue.update(armyQueue);
        }
    });
});