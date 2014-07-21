define('view/admin/player', [
    'view/block/error'
], function (
    viewBlockError
) {
    return AbstractView.extend({
        className: 'player',
        events: {
            'click .search-user': 'onSearchUser',
            'keydown .search-user-login': 'onSearchUser',
            'click .save-info': 'onSaveInfo'
        },

        render: function (holder) {
            this.$el.html(this.template('admin/player/player'));
            holder.append(this.$el);
        },

        unRender: function () {
            this.$el.remove();
        },

        showUserData: function (userDomain, resourceDomain) {
            this.$el.find('#user-info').html(
                this.template(
                    'admin/player/info',
                    {
                        resources: resourceDomain
                    }
                )
            );
        },

        successSave: function () {
            viewBlockError.showSuccessBox('Данные успешно сохранены');
        },

        onSaveInfo: function () {
            this.trigger('save-info', {
                rubins : this.$el.find('input.rubins').val(),
                wood   : this.$el.find('input.wood').val(),
                steel  : this.$el.find('input.steel').val(),
                stone  : this.$el.find('input.stone').val(),
                eat    : this.$el.find('input.eat').val(),
                gold   : this.$el.find('input.gold').val()
            });
        },

        onSearchUser: function (e) {
            if (e.keyCode && e.keyCode !== this.keyCodes.enter) {
                return;
            }

            var value = this.$el.find('.search-user-login').val();

            if (!value) {
                viewBlockError.showErrorBox('Поле логина пустое');
                return;
            }

            this.trigger('search-user', value);
        }
    });
});