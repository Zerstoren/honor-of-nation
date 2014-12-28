define('service/equipment/armor', [
    'system/preStart',
    'service/standalone/user',

    'view/equipment/armor',

    'collection/equipment/armor'
], function (
    systemPreStart,
    serviceStandaloneUser,

    ViewEquipmentArmor,

    CollectionEquipmentArmor
) {
    return AbstractService.extend({
        initialize: function () {
            this.viewEquipmentArmor = new ViewEquipmentArmor();
            this.viewEquipmentArmor.on('save', this.onSave, this);
            this.viewEquipmentArmor.on('remove', this.onRemove, this);
            this.traverseEvent('close', this.viewEquipmentArmor);
        },

        render: function () {
            this.collection = new CollectionEquipmentArmor();
            var holder = systemPreStart.map.body.holder;
            this.viewEquipmentArmor.render(holder, this.collection);
            this.load();
        },

        load: function () {
            serviceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (user) {
                this.collection.setUser(user);
                this.collection.load();
            }.bind(this));
        },

        onRemove: function (armor) {
            armor.remove(this.afterRemoveArmor.bind(this));
            this.viewEquipmentArmor.removeCurrentArmorDomain(armor);
        },

        onSave: function (armorDomain) {
            armorDomain.save(this.afterCreateSave.bind(this));
        },

        afterCreateSave: function () {
            this.collection.load();
            this.viewEquipmentArmor.afterCreateSave();
        },

        afterRemoveArmor: function () {
            this.collection.load();
            this.viewEquipmentArmor.afterRemoveArmor();
        }
    });
});