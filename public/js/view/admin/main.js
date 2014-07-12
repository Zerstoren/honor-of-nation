define('view/admin/main', [
    'system/template'
], function (template) {
    return Backbone.View.extend({
        events: {
            'click .close': "onClose",
            'click ul li button': 'onSelectType'
        },

        className: 'admin',

        initialize: function () {
        },

        render: function (holder) {
            this.$el.html(template('admin/main'));
            holder.append(this.$el);
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
        }
    });
});
