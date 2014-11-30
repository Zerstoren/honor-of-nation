define('collection/equipment/weapon', [
    'model/equipment/weapon'
], function (
    ModelEquipmentWeapon
) {
    return AbstractCollection.extend({
        collection_url: 'equipment/weapon',
        model: ModelEquipmentWeapon,

        initialize: function () {
            AbstractCollection.prototype.initialize.apply(this);
            this._user = null;
        },

        setUser: function (user) {
            this._user = user;
        },

        getUser: function () {
            return this._user;
        },

        load: function () {
            if (!this.getUser()) {
                throw new Error("For collection user not set");
            }

            this.sync('load', null, {
                data: {
                    'user': this.getUser().get('_id')
                }
            });
        }
    });
});
