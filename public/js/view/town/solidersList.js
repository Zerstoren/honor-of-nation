define('view/town/solidersList', [], function () {
    return AbstractView.extend({
        initialize: function () {
            this.template = this.getTemplate('town/unitsList/list');
            this.initRactive();
        },

        render: function (holder, town) {
            holder.append(this.$el);
        }
    });
});