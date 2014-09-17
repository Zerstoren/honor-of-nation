define('view/admin/resources', [
    'view/elements/tooltip',
    'model/resources'
], function (
    ViewElementsTooltip,
    ModelResources
) {
    return AbstractView.extend({
        className: 'resources-map',
        events: {
            'click .create': 'onCreate',
            'click .search': 'onSearch',
//            'change .user': 'onChangeUser',
//            'change .town': 'onChangeTown',
            'click .save': 'onSaveResource'
        },

        initialize: function () {
            this.tooltipManager = new ViewElementsTooltip(this, '.form-group .with-tooltip');

            this.template = this.getTemplate('admin/resources/show');
            this.partials = {
                edit: this.getTemplate('admin/resources/edit')
            };
            this.initRactive();
        },

        data: {
            search: '',
            resource: null,
            users: null
        },

        render: function (holder) {
            holder.append(this.$el);
            this.delegateEvents();
        },

        unRender: function () {
            this.$el.remove();
            this.undelegateEvents();
        },

        showEditForm: function (domain, users) {
            this.set('users', users);

            if (!domain) {
                domain = new ModelResources({
                    type: ModelResources.prototype.RUBINS,
                    amount: 0,
                    base_output: 0,
                    output: 0,
                    position: this.get('formatters').fromIdToPlace(0),
                    town: null,
                    user: null
                })
            } else {
                domain.set('position', this.get('formatters').fromIdToPlace(domain.get('pos_id')))
            }

            this.set('resource', domain);
        },

        showSuccess: function () {
            this.set('users', null);
            this.set('town', null);
            this.set('search', null);
            this.successMessage('Resource as success save');
        },

        onCreate: function () {
            this.trigger('search', false, false);
        },

        onSearch: function () {
            var coordinate = this.$validateCoordinate(this.get('search'));

            if (coordinate) {
                this.trigger('search', coordinate[0], coordinate[1]);
            }
        },

//        onChangeUser: function () {
//
//        },
//
//        onChangeTown: function () {
//
//        },

        onSaveResource: function () {
            this.trigger('save', this.get('resource'));
        },

        $validateCoordinate: function (coordinate) {
            var x, y,
                coords = coordinate.split(/([0-9]{1,4})([^0-9]{1,})([0-9]{1,4})/);

            if (coords.length != 5) {
                this.errorMessage('Введен неверный форма координат. Используйте такой вид: 100x100');
                return false;
            }

            x = parseInt(coords[1], 10);
            y = parseInt(coords[3], 10);

            if (isNaN(x) || isNaN(y)) {
                this.errorMessage('Введен неверный форма координат. Используйте такой вид: 100x100');
                return false;
            }

            return [x, y];
        }
    });
});