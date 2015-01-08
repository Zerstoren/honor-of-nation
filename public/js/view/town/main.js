define('view/town/main', [

], function (

) {
    return AbstractView.extend({
        events: {
            'click .close': 'onClose',
            'keydown global': 'onKeyDown',
            'click .town_info .develop_weapon': 'onDevelopWeapon',
            'click .town_info .develop_armor': 'onDevelopArmor',
            'click .town_info .develop_people': 'onDevelopUnit'
        },

        className: 'town',

        initialize: function () {
            this.template = this.getTemplate('town/base');
            this.initRactive();
        },

        render: function (holder) {
            holder.append(this.$el);
            this.delegateEvents();
        },

        unRender: function () {
            this.$el.remove();
            this.undelegateEvents();
        },

        getLeftSide: function () {
            return this.$el.find('.left');
        },

        getRightSide: function () {
            return this.$el.find('.right');
        },

        getUnitsPosition: function () {
            return this.$el.find('.listUnits');
        },

        setDomain: function (townDomain) {
            this.set('town', townDomain);
        },

        onClose: function () {
            this.trigger('close');
        },

        onKeyDown: function (e) {
            if (e.keyCode === this.keyCodes.esc) {
                this.onClose();
            }
        },

        onDevelopWeapon: function () {
            this.undelegateEvents();
            this.trigger('onDevelopWeapon');
        },

        onDevelopArmor: function () {
            this.undelegateEvents();
            this.trigger('onDevelopArmor');
        },

        onDevelopUnit: function () {
            this.undelegateEvents();
            this.trigger('onDevelopUnit');
        }
    });
});