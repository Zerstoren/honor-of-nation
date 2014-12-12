define('view/equipment/abstract', [], function () {
    return AbstractView.extend({
        tpl: null,
        initialize: function () {
            this.viewCollection = null;

            this.timeoutUpdate = null;
            this.selectedType = null;

            this.template = this.getTemplate(this.tpl);
            this.initRactive();

            this.set('settings', new ModelDummy());
        },

        render: function (holder, collection) {
            this.viewCollection = collection;
            this.viewCollection.on('change', this.onChangeCollection, this);
            this.viewCollection.on('reset', this.onChangeCollection, this);
            this.changeFilterType('all');

            holder.append(this.$el);

            this.delegateEvents();
        },

        unRender: function () {
            this.$el.remove();
            this.undelegateEvents();

        },

        changeFilterType: function (type) {
            this.$el.find('.select-filter-equipment .filter').removeClass('active');
            this.$el.find('.select-filter-equipment .' + type).addClass('active');

            if (type === 'all') {
                this.selectedType = null;
                this.onChangeCollection(this.viewCollection);
            } else {
                this.selectedType = type;
                this.onChangeCollection(this.viewCollection, type);
            }
        },

        onRemove: function (e) {
            var target = jQuery(e.target).parents('.equipment-item'),
                id = target.attr('data-id');

            this.trigger('remove', this.viewCollection.searchById(id));
            return false;

        },

        onChangeCollection: function (collection, type) {
            var viewCollection = collection.clone();
            viewCollection.sort();

            if (type === undefined) {
                type = this.selectedType;
            }

            if (type !== null) {
                viewCollection = viewCollection.where({type: type});
            }

            this.set('collection', viewCollection);
        },


        onClose: function () {
            this.unRender();
            this.trigger('close');
        },

        onKeyDown: function (e) {
            if (e.keyCode === this.keyCodes.esc) {
                this.onClose();
            }
        }
    });
});