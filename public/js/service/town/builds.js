define('service/town/builds', [
    'gateway/town',
    'view/town/builds'
], function (
    gatewayTown,
    ViewTownBuilds
) {
    return AbstractService.extend({
        initialize: function () {
            this.buildsView = new ViewTownBuilds();
            this.buildsView.on('createBuild', this.onCreateBuild, this);
        },

        render: function (holder, townDomain) {
            this.holder = holder;
            this.currentTown = townDomain;
            gatewayTown.loadBuilds(townDomain, this.onBuildsLoad.bind(this));
        },

        onBuildsLoad: function (builds) {
            this.buildsView.render(this.holder, builds, this.currentTown);
        },

        onCreateBuild: function (key) {

        }
    });
});