define('service/town/main', [
    'system/preStart',
    'system/route',
    'model/town',

    'service/town/builds',
    'service/town/soldiersList',
    'service/town/soldiersCreate',
    'service/town/changeTowns',

    'view/town/main'
], function (
    preStart,
    systemRoute,
    ModelTown,

    ServiceTownBuilds,
    ServiceTownSoldiersList,
    ServiceTownSoldiersCreate,
    ServiceTownChangeTowns,

    ViewTownMain
) {
    return AbstractService.extend({
        initialize: function () {
            this.mainView = new ViewTownMain();
            this.serviceTownBuilds = new ServiceTownBuilds();

            this.mainView.on('close', this.onClose, this);
        },

        render: function (townId) {
            this.holder = preStart.map.body.getHolder();

            this.mainView.render(this.holder);

            this.currentDomain = new ModelTown();
            this.currentDomain.set('id', townId);
            this.currentDomain.getById(this.onTownLoad.bind(this));

            this.serviceTownBuilds.render(
                this.mainView.getLeftSide(),
                this.currentDomain
            );
        },

        unRender: function () {
            this.mainView.unRender();
        },

        onTownLoad: function () {
            this.mainView.setDomain(this.currentDomain);
        },

        onClose: function () {
            systemRoute.navigate('');
        }
    });
});