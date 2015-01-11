define('collection/armyQueue', [
    'model/armyQueue'
], function (
    ModelArmyQueue
) {
    return AbstractCollection.extend({
        model: ModelArmyQueue,
        collection_url: 'army/queue',

        getTown: function () {
            return this._town;
        },

        setTown: function (town) {
            this._town = town;
        },

        load: function () {
            if (!this.getTown()) {
                throw new Error("For collection town not set");
            }

            this.sync('load', {
                data: {
                    'town': this.getTown().get('_id')
                }
            });
        }
    });
});