define('model/equipment/armor', [
], function () {
    return AbstractModel.extend({
        model_url: "equipment/armor",

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

                    shield: this.get('shield'),
                    shield_type: this.get('shield_type'),
                    shield_durability: this.get('shield_durability'),
                    shield_blocking: this.get('shield_blocking'),

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
                (!this.get('absorption') && !_.isNumber(this.get('absorption')))
            ) {
                return;
            } else {
                if (
                    this.get('shield') &&
                    (
                        (!this.get('shield_type') && _.isNumber(this.get('shield_type'))) ||
                        (!this.get('shield_durability') && _.isNumber(this.get('shield_durability'))) ||
                        (!this.get('shield_blocking') && _.isNumber(this.get('shield_blocking')))
                    )
                ) {
                    return;
                }
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