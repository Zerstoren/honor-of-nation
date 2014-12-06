define('model/equipment/weapon', [
], function () {
    return AbstractModel.extend({
        model_url: "equipment/weapon",

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
                    damage: this.get('damage'),
                    speed: this.get('speed'),
                    critical_damage: this.get('critical_damage'),
                    critical_chance: this.get('critical_chance'),
                    type: this.get('type'),
                    user: this.get('user')
                },
                success: successCallback
            });
        },

        simulate: function () {
            if (
                !this.get('damage') ||
                !this.get('speed') ||
                !this.get('critical_damage') ||
                !this.get('critical_chance') ||
                !this.get('type')
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