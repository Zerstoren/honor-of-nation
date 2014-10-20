define('view/admin/town', [
    'service/standalone/map',
    'view/elements/tooltip'

], function (
    gameMap,
    ViewElementsTooltip
) {
    return AbstractView.extend({
        className: 'town',
        events: {
            'click .create': 'onCreate',
            'click .search': 'onSearch',
            'click .save': 'onSave'
        },

        initialize: function () {
            this.tooltipManager = new ViewElementsTooltip(this, '.with-tooltip');

            this.setPartials({
                edit: 'admin/town/edit'
            });

            this.template = this.getTemplate('admin/town/show');
            this.initRactive();
        },

        data: {
            showEdit: false,
            search: '',
            users: [],
            town: {}
        },

        render: function (holder) {
            holder.append(this.$el);
            this.delegateEvents();
        },

        unRender: function () {
            this.$el.remove();
            this.undelegateEvents();
        },

        showEdit: function (users, town) {
            this.set('users', users);
            this.set('town', town ? town : {});
            this.set('showEdit', true);
        },

        onCreate: function () {
            this.trigger('search', false, false);
        },

        onSearch: function () {
            var coordinate = gameMap.help.validateCoordinate(this.get('search'));

            if (coordinate) {
                this.trigger('search', coordinate[0], coordinate[1]);
            }
        },

        onSave: function () {
            var town = this.get('town');
            var posXY = gameMap.help.validateCoordinate(town.position);

            if (posXY === false) {
                return;
            }

            town.pos_id = gameMap.help.fromPlaceToId(posXY[0], posXY[1]);

            if (isNaN(parseInt(town.population, 10))) {
                this.errorMessage('Неверно заполнено поле популяция');
                return;
            }

            if (!town.name) {
                this.errorMessage('Имя города не заполнено');
            }

            this.trigger('save', town);
        },

        successSave: function (townDomain) {
            this.set('town', townDomain);
            this.successMessage('Город сохранен успешно');
        }
    });
});