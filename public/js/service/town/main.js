define('service/town/main', [
    'system/preStart',
    'system/route',
    'model/town',
    'factory/town',

    'service/town/builds',
    'service/town/soldiersList',
    'service/town/soldiersCreate',
    'service/town/changeTowns',
    'service/equipment/weapon',

    'view/town/main'
], function (
    preStart,
    systemRoute,
    ModelTown,
    factoryTown,

    ServiceTownBuilds,
    ServiceTownSoldiersList,
    ServiceTownSoldiersCreate,
    ServiceTownChangeTowns,
    ServiceEquipmentWeapon,

    ViewTownMain
) {
    return AbstractService.extend({
        initialize: function () {
            this.mainView = new ViewTownMain();
            this.serviceTownBuilds = new ServiceTownBuilds();
            this.serviceEquipmentWeapon = new ServiceEquipmentWeapon();

            this.mainView.on('close', this.onClose, this);

            this.mainView.on('onDevelopWeapon', this.onDevelopWeapon, this);
        },

        render: function (townId) {
            var townPoolDomain = factoryTown.getFromPool(townId);
            this.holder = preStart.map.body.getHolder();

            this.mainView.render(this.holder);

            if (townPoolDomain) {
                this.currentDomain = townPoolDomain;
            } else {
                this.currentDomain = new ModelTown();
                this.currentDomain.set('_id', townId);

                factoryTown.pushToPool(this.currentDomain);
            }

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
        },

        onDevelopWeapon: function () {
//            debugger;
            this.serviceEquipmentWeapon.render();
        }
    });
});