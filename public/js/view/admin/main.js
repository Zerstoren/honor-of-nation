define('view/admin/main', [], function () {
    return AbstractView.extend({
        events: {
            'click .close'      : "onClose",
            'click ul li button': 'onSelectType'
        },

        eventsGlobal: {
            'keydown': 'onKeyDown'
        },

        className: 'admin',

        render: function (holder) {
            this.$el.html(this.getTemplate('admin/main'));
            holder.append(this.$el);
            this.delegateEvents();
        },

        unRender: function() {
            this.$el.remove();
            this.undelegateEvents();
        },

        getHolder: function () {
            return this.$el.find('#admin-holder');
        },

        onClose: function () {
            this.trigger('close');
        },

        onSelectType: function (e) {
            var target = $(e.currentTarget);

            this.$el.find('ul li button').removeClass('active');
            target.addClass('active');
            this.trigger('selectType', target.data('type'));
        },

        onKeyDown: function (e) {
            if (e.keyCode === this.keyCodes.esc) {
                this.trigger('close');
            }
        }
    });
});
