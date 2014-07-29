define('view/admin/player', [], function () {
    return AbstractView.extend({
        className: 'player',
        events: {
            'click .search-user': 'onSearchUser',
            'keydown .search-user-login': 'onSearchUser',
            'click .save-info': 'onSaveInfo',
            'click .save-coordinate': 'onSaveCoordinate'
        },

        render: function (holder) {
            this.$el.html(this.template('admin/player/player'));
            holder.append(this.$el);
            this.delegateEvents();

            this.$el.find('.search-user-login').val('Zerst');
            this.onSearchUser({});
        },

        unRender: function () {
            this.$el.remove();
            this.undelegateEvents();
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
            this.successMessage('Данные успешно сохранены');
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

        onSaveCoordinate: function (e) {
            var data = {
                fromX: this.$el.find('.show-terrain .from .x').val(),
                fromY: this.$el.find('.show-terrain .from .y').val(),
                toX: this.$el.find('.show-terrain .to .x').val(),
                toY: this.$el.find('.show-terrain .to .y').val()
            };

            if (!data.fromX || !data.fromY || !data.toX || !data.toY) {
                this.errorMessage('Указаны не все координаты');
                return;
            }

            this.$el.find('.show-terrain .from .x').val('');
            this.$el.find('.show-terrain .from .y').val('');
            this.$el.find('.show-terrain .to .x').val('');
            this.$el.find('.show-terrain .to .y').val('');

            this.trigger('save-coordinate', data);
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