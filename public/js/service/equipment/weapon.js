define('service/equipment/weapon', [
    'system/preStart',
    'service/standalone/user',

    'view/equipment/weapon',

    'collection/equipment/weapon'
], function (
    systemPreStart,
    serviceStandaloneUser,

    ViewEquipmentWeapon,

    CollectionEquipmentWeapon
) {
    return AbstractService.extend({
        initialize: function () {
            this.viewEquipmentWeapon = new ViewEquipmentWeapon();
            this.viewEquipmentWeapon.on('save', this.onSave, this);
            this.viewEquipmentWeapon.on('remove', this.onRemove, this);
            this.traverseEvent('close', this.viewEquipmentWeapon);
        },

        render: function () {
            this.collection = new CollectionEquipmentWeapon();
            var holder = systemPreStart.map.body.holder;
            this.viewEquipmentWeapon.render(holder, this.collection);
            this.load();
        },

        load: function () {
            serviceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (user) {
                this.collection.setUser(user);
                this.collection.load();
            }.bind(this));
        },

        onRemove: function (weapon) {
            weapon.remove(this.afterRemoveWeapon.bind(this));
            this.viewEquipmentWeapon.removeCurrentWeaponDomain(weapon);
        },

        onSave: function (weaponDomain) {
            weaponDomain.save(this.afterCreateSave.bind(this));
        },

        afterCreateSave: function () {
            this.collection.load();
            this.viewEquipmentWeapon.afterCreateSave();
        },

        afterRemoveWeapon: function () {
            this.collection.load();
            this.viewEquipmentWeapon.afterRemoveWeapon();
        }
    });
});