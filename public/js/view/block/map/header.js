define('view/block/map/header', [
    'service/standalone/user',
    'view/elements/resource',
    'view/elements/menu'
], function(
    serviceStandaloneUser,
    ViewElementsResource,
    ViewElementsMenu
) {
    'use strict';

    return AbstractView.extend({
        viewResource: null,
        viewMenu    : null,
        name: "b",
        initialize: function (holder) {
            this.holder = holder;
            this.template = this.getTemplate('block/map/header');
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

            serviceStandaloneUser.getMe(function (domain) {
                this.viewResource.setUserResources(domain.getResources());
            }.bind(this));
        }
    });
});