define('view/equipment/weapon', [
], function () {
    return AbstractView.extend({
        initialize: function () {
            this.collection = null;
            this.template = this.getTemplate('equipment/weapon');
            this.initRactive();
        },

        render: function (holder, collection) {
            this.collection = collection;
            holder.append(this.$el);
        }
    });
});
