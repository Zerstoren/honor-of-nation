define('collection/armyQueue', [
    'model/armyQueue'
], function (
    ModelArmyQueue
) {
    return AbstractCollection.extend({
        model: ModelArmyQueue,
        collection_url: 'army/queue'
    });
});