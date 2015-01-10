define('collection/army', [
    'model/army'
], function (
    ModelArmy
) {
    return AbstractCollection.extend({
        model: ModelArmy,
        collection_url: 'army',

        getTown: function () {
            return this._town;
        },

        setTown: function (town) {
            this._town = town;
        },

        getUser: function () {
            return this._user;
        },

        setUser: function (user) {
            this._user = user;
        },

        load: function (fn) {
            if (!this.getTown()) {
                throw new Error("For collection town not set");
            }

            if (!this.getUser()) {
                throw new Error("For collection user not set");
            }

            this.sync('load', {
                data: {
                    'town': this.getTown().get('_id'),
                    'pos_id': this.getTown().get('pos_id'),
                    'user': this.getUser().get('_id')
                },
                success: function (data) {
                    fn(data);
                }
            });
        }
    });
});