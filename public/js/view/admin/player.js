define('view/admin/player', [
    'view/block/error'
], function (
    viewBlockError
) {
    return AbstractView.extend({
        className: 'player',
        events: {
            'click .search-user': 'onSearchUser'
        },

        render: function (holder) {
            this.$el.html(this.template('admin/player/player'));
            holder.append(this.$el);
        },

        unRender: function () {
            this.$el.remove();
        },

        onSearchUser: function (e) {
            var value = this.$el.find('.search-user-login').val();

            if (!value) {
                viewBlockError.showErrorBox('Поле логина пустое');
            }

            this.trigger('search-user', value);
        }
    });
});