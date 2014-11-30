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
        },

        render: function () {
            this.collection = new CollectionEquipmentWeapon();
            var holder = systemPreStart.map.body.holder;
            this.viewEquipmentWeapon.render(holder, this.collection);
            this.load();
        },

        load: function () {
            serviceStandaloneUser.getMe(function (user) {
                this.collection.setUser(user);
                this.collection.load();
            }.bind(this));
        }
    });
});