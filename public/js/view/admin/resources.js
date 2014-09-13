define('view/admin/resources', [
    'model/resources'
], function (ModelResources) {
    return AbstractView.extend({
        className: 'resources-map',
        events: {
            'click .create': 'onCreate',
            'click .search': 'onSearch',
//            'change .user': 'onChangeUser',
//            'change .town': 'onChangeTown',
            'click .save': 'onSaveResource',
            "mouseenter .form-group .with-tooltip": "onShowHint",
            "mouseout .form-group .with-tooltip": "onHideHint"
        },

        initialize: function () {
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
                    base: 0,
                    output: 0,
                    pos_id: 0,
                    town: null,
                    user: null
                })
            }
            this.set('resource', domain);
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

        onShowHint: function (e) {
            this.tooltip = jQuery(e.target);
            this.tooltip.tooltip({
                trigger: '',
                title: this.tooltip.data('hint'),
                placement: 'right',
                container: 'body'
            });

            this.tooltip.tooltip('show');
        },

        onHideHint: function (e) {
            this.tooltip.tooltip('destroy');
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
                this.showErrorBox('Введен неверный форма координат. Используйте такой вид: 100x100');
                return false;
            }

            x = parseInt(coords[1], 10);
            y = parseInt(coords[4], 10);

            if (isNaN(x) || isNaN(y)) {
                this.showErrorBox('Введен неверный форма координат. Используйте такой вид: 100x100');
                return false;
            }

            return [x, y];
        }
    });
});