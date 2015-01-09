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

        load: function () {
            if (!this.getTown()) {
                throw new Error("For collection town not set");
            }

            if (!this.getUser())

            this.sync('load', {
                data: {
                    'town': this.getTown().get('_id')
                }
            });
        }
    });
});