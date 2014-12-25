define('model/equipment/unit', [
], function () {
    return AbstractModel.extend({
        model_url: "equipment/units",

        load: function (successCallback) {
            this.sync('get', {
                data: {
                    _id: this.get('_id')
                },
                success: successCallback
            });
        },

        save: function (successCallback) {
            this.sync('save', {
                data: {
                    health: this.get('health'),
                    agility: this.get('agility'),
                    absorption: this.get('absorption'),
                    stamina: this.get('stamina'),
                    strength: this.get('strength'),
                    troop_size: this.get('troop_size'),

                    armor: this.get('armor'),
                    weapon: this.get('weapon'),
                    weapon_second: this.get('weapon_second'),

                    type: this.get('type'),
                    user: this.get('user')
                },
                success: successCallback
            });
        },

        simulate: function () {
            if (
                (!this.get('health') && !_.isNumber(this.get('health'))) ||
                (!this.get('agility') && !_.isNumber(this.get('agility'))) ||
                (!this.get('absorption') && !_.isNumber(this.get('absorption'))) ||
                (!this.get('stamina') && !_.isNumber(this.get('stamina'))) ||
                (!this.get('strength') && !_.isNumber(this.get('strength'))) ||
                !this.get('armor') ||
                !this.get('weapon')
            ) {
                return;
            }

            this.sync('simulate', {
                data: this.attributes
            });
        },

        remove: function (success) {
            this.sync('remove', {
                data: {
                    '_id': this.get('_id')
                },
                success: success
            });
        }
    });
});