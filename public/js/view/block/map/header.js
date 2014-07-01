define('view/block/map/header', [
    'system/template',

    'view/elements/resource',
    'view/elements/menu'
], function(
    template,
    ViewElementsResource,
    ViewElementsMenu
) {
    'use strict';

    return Backbone.View.extend({
        template: template('block/map/header'),

        viewResource: null,
        viewMenu    : null,

        initialize: function (holder) {
            this.holder = holder;
        },

        render: function () {
            if (this.viewResource === null) {
                this.viewResource = new ViewElementsResource();
            }

            if (this.viewMenu === null) {
                this.viewMenu = new ViewElementsMenu();
                this.viewMenu.on('onMenuClick', function (menuName) {
                    this.trigger('onMenuClick', menuName)
                }, this)
            }

            this.$el.html(this.template);

            this.viewResource.render(this.$el.find('.mpi__resource_wrapper'));
            this.viewMenu.render(this.$el.find('.mpi__menu'));

            this.holder.append(this.$el);
        }
    });
});