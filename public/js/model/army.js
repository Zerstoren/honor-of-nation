define('model/army', [], function () {
    return AbstractModel.extend({
        model_url: 'army',

        deepSearchById: function (_id) {
            var searchingArmy = null,
                parentArmy = null;

            return this._deepSearch(this, _id);
        },

        _deepSearch: function (model, _id) {
            var i, subArmyResult, subArmyModels, result;

            if (model.get('_id') === _id) {
                return [this, null, false];
            }

            if (model.get('suite') && model.get('suite').get('_id') === _id) {
                return [model, null, true];
            }

            subArmyResult = model.get('sub_army').where({'_id': _id});
            if (subArmyResult.length === 1) {
                return [
                    subArmyResult.at(0),
                    model,
                    false
                ];
            }

            subArmyModels = model.get('sub_army').models;
            for (i = 0; i < subArmyModels.length; i += 1) {
                result = subArmyModels[i].deepSearchById(_id);

                if (result !== false) {
                    return result
                }
            }

            return false;
        }
    });
});