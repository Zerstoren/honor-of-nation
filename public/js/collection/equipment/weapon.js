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

        comparator: function (model) {
            return model.get('level');
        },

        setUser: function (user) {
            this._user = user;
        },

        getUser: function () {
            return this._user;
        },

        searchById: function (id) {
            var result = this.where({'_id': id});
            if (result.length === 0) {
                return null;
            }

            return result.at(0);
        },

        load: function () {
            if (!this.getUser()) {
                throw new Error("For collection user not set");
            }

            this.sync('load', {
                data: {
                    'user': this.getUser().get('_id')
                }
            });
        }
    });
});
