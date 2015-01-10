define('service/town/main', [
    'system/preStart',
    'system/route',
    'model/town',
    'factory/town',

    'service/town/builds',
    'service/town/solidersList',
    'service/town/solidersCreate',
    'service/town/changeTowns',

    'service/equipment/weapon',
    'service/equipment/armor',
    'service/equipment/unit',

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
    ServiceEquipmentArmor,
    ServiceEquipmentUnit,

    ViewTownMain
) {
    return AbstractService.extend({
        initialize: function () {
            this.mainView = new ViewTownMain();
            this.serviceTownBuilds = new ServiceTownBuilds();
            this.serviceTownSolidersCreate = new ServiceTownSoldiersCreate();
            this.serviceTownSoldiersList = new ServiceTownSoldiersList();

            // Buttons
            this.serviceEquipmentWeapon = new ServiceEquipmentWeapon();
            this.serviceEquipmentArmor = new ServiceEquipmentArmor();
            this.serviceEquipmentUnit = new ServiceEquipmentUnit();

            this.mainView.on('close', this.onClose, this);

            this.mainView.on('onDevelopWeapon', this.onDevelopWeapon, this);
            this.mainView.on('onDevelopArmor', this.onDevelopArmor, this);
            this.mainView.on('onDevelopUnit', this.onDevelopUnit, this);
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

            this.serviceTownSolidersCreate.render(
                this.mainView.getRightSide(),
                this.currentDomain
            );
        },

        unRender: function () {
            this.mainView.unRender();
        },

        onTownLoad: function () {
            this.mainView.setDomain(this.currentDomain);

            this.serviceTownSoldiersList.render(
                this.mainView.getUnitsPosition(),
                this.currentDomain
            );
        },

        onClose: function () {
            systemRoute.navigate('');
        },

        onDevelopWeapon: function () {
            this.mainView.undelegateEvents();
            this.serviceEquipmentWeapon.render();
            this.serviceEquipmentWeapon.on('close', this.onDevClose, this);
        },

        onDevelopArmor: function () {
            this.mainView.undelegateEvents();
            this.serviceEquipmentArmor.render();
            this.serviceEquipmentArmor.on('close', this.onDevClose, this);
        },

        onDevelopUnit: function () {
            this.mainView.undelegateEvents();
            this.serviceEquipmentUnit.render();
            this.serviceEquipmentUnit.on('close', this.onDevClose, this);
        },

        onDevClose: function () {
            this.mainView.delegateEvents();
            this.serviceEquipmentWeapon.off('close', this.onDevClose, this);
            this.serviceEquipmentArmor.off('close', this.onDevClose, this);
            this.serviceEquipmentUnit.off('close', this.onDevClose, this);
        }
    });
});