define('service/equipment/unit', [
    'system/preStart',
    'service/standalone/user',

    'view/equipment/unit',

    'collection/equipment/unit',
    'collection/equipment/armor',
    'collection/equipment/weapon'
], function (
    systemPreStart,
    serviceStandaloneUser,

    ViewEquipmentUnit,

    CollectionEquipmentUnit,
    CollectionEquipmentArmor,
    CollectionEquipmentWeapon
) {
    return AbstractService.extend({
        initialize: function () {
            this.viewEquipmentUnit = new ViewEquipmentUnit();
            this.viewEquipmentUnit.on('save', this.onSave, this);
            this.viewEquipmentUnit.on('remove', this.onRemove, this);
            this.traverseEvent('close', this.viewEquipmentUnit);
        },

        render: function () {
            this.collection = new CollectionEquipmentUnit();
            this.armorCollection = new CollectionEquipmentArmor();
            this.weaponCollection = new CollectionEquipmentWeapon();

            var holder = systemPreStart.map.body.holder;
            this.viewEquipmentUnit.render(
                holder,
                this.collection,
                this.armorCollection,
                this.weaponCollection
            );
            this.load();
        },

        load: function () {
            serviceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (user) {
                this.collection.setUser(user);
                this.collection.load();

                this.armorCollection.setUser(user);
                this.armorCollection.load();

                this.weaponCollection.setUser(user);
                this.weaponCollection.load();
            }.bind(this));
        },

        onRemove: function (unit) {
            unit.remove(this.afterRemoveArmor.bind(this));
            this.viewEquipmentUnit.removeCurrentUnitDomain(unit);
        },

        onSave: function (unitDomain) {
            unitDomain.save(this.afterCreateSave.bind(this));
        },

        afterCreateSave: function () {
            this.collection.load();
            this.viewEquipmentUnit.afterCreateSave();
        },

        afterRemoveArmor: function () {
            this.collection.load();
            this.viewEquipmentUnit.afterRemoveUnit();
        }
    });
});