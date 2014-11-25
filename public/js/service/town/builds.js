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
            this.buildsView.on('cancelBuild', this.onCancelBuild, this);
        },

        render: function (holder, townDomain) {
            this.holder = holder;
            this.currentTown = townDomain;

            this.buildsView.render(this.holder, this.currentTown);
            gatewayTown.loadBuilds(townDomain, this.onBuildsLoad.bind(this));
        },

        onBuildsLoad: function (builds, queue) {
            this.buildsView.update(builds, queue);
        },

        onCreateBuild: function (key) {
            var level = this.buildsView._getMaximumLevel(key) + 1;
            gatewayTown.createBuild(
                this.currentTown,
                key,
                level,
                this.buildsView.update.bind(this.buildsView)
            );
        },

        onCancelBuild: function (key, level) {
            gatewayTown.cancelBuild(
                this.currentTown,
                key,
                level,
                this.buildsView.update.bind(this.buildsView)
            );
        }
    });
});