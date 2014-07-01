define('collection/user', [
    'collection/abstract',
    'model/user'
], function (
    CollectionAbstract,
    ModelUser
) {
    return CollectionAbstract.extend({
        model: ModelUser,
        collection_url: 'user'
    });
});