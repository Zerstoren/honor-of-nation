define('view/admin/player', [], function () {
    return AbstractView.extend({
        className: 'player',
        events: {
            'click .search-user': 'onSearchUser',
            'keydown .search-user-login': 'onSearchUser',
            'click .save-info': 'onSaveInfo',
            'click .save-coordinate': 'onSaveCoordinate'
        },

        initialize: function () {
            this.template = this.getTemplate('admin/player/player');
            this.partials = {
                info: this.getTemplate('admin/player/info')
            };

            this.initRactive();
        },

        data: {
            login: '',
            position: {
                fromX: null,
                toX: null,
                fromY: null,
                toY: null
            }
        },

        render: function (holder) {
            holder.append(this.$el);
            this.delegateEvents();
        },

        unRender: function () {
            this.$el.remove();
            this.undelegateEvents();
        },

        showUserData: function (userDomain, resourceDomain) {
            this.set('user', userDomain);
            this.set('resources', resourceDomain);
        },

        successSave: function () {
            this.successMessage('Данные успешно сохранены');
        },

        onSaveInfo: function () {
            this.trigger('save-info', {
                rubins : this.get('resources').get('rubins'),
                wood   : this.get('resources').get('wood'),
                steel  : this.get('resources').get('steel'),
                stone  : this.get('resources').get('stone'),
                eat    : this.get('resources').get('eat'),
                gold   : this.get('resources').get('gold')
            });
        },

        onSaveCoordinate: function (e) {
            var data = {};
            data.user = this.data.user.get('_id');
            data.coordinate = this.get('position');

            if (!data.coordinate.fromX || !data.coordinate.fromY || !data.coordinate.toX || !data.coordinate.toY) {
                this.errorMessage('Указаны не все координаты');
                return;
            }

            this.set('position', {
                fromX: null,
                toX: null,
                fromY: null,
                toY: null
            });

            this.trigger('save-coordinate', data);
        },

        onSearchUser: function (e) {
            if (e.keyCode && e.keyCode !== this.keyCodes.enter) {
                return;
            }

            if (!this.get('login')) {
                viewBlockError.showErrorBox('Поле логина пустое');
                return;
            }

            this.trigger('search-user', this.get('login'));
        }
    });
});