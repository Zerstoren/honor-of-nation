define('collection/user', [
    'model/user'
], function (
    ModelUser
) {
    return AbstractCollection.extend({
        model: ModelUser,
        collection_url: 'user'
    });
});