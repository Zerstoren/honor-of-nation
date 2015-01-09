define('view/town/solidersList', [], function () {
    return AbstractView.extend({
        events: {

        },

        data: {
            army: null
        },

        initialize: function () {
            this.template = this.getTemplate('town/unitsList/list');
            this.initRactive();
        },

        render: function (holder, town) {
            holder.append(this.$el);
        },

        setArmy: function (armyCollection) {
            this.armyCollection = armyCollection;
            this.set('army', this.armyCollection);
        }
    });
});