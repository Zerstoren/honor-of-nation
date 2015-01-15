define('service/town/solidersList', [
    'service/standalone/user',
    'service/standalone/messages',

    'view/town/solidersList',

    'collection/army',

    'gateway/army'
], function (
    serviceStandaloneUser,
    serviceStandaloneMessages,

    VeiwTownSoliderList,

    CollectionArmy,

    gatewayArmy
) {
    return AbstractService.extend({
        initialize: function () {
            this.mainView = new VeiwTownSoliderList();
            this.collectionArmy = new CollectionArmy();

            serviceStandaloneMessages.on('unitsUpdate', this.update, this);

            this.mainView.on('dissolution', this.onDissolution, this);
            this.mainView.on('split', this.onSplit, this);
            this.mainView.on('merge', this.onMerge, this);
        },

        render: function (holder, town) {
            this.town = town;
            this.mainView.render(holder, town);
            this.update();
        },

        update: function () {
            serviceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (user) {
                this.collectionArmy.setUser(user);
                this.collectionArmy.setTown(this.town);

                this.collectionArmy.load(function () {
                    this.mainView.setArmy(this.collectionArmy);
                }.bind(this));
            }.bind(this));
        },

        onMerge: function (army) {
            gatewayArmy.merge(army, function () {
                this.update();
            }.bind(this));
        },

        onSplit: function (id, size) {
            gatewayArmy.split(id, size, function () {
                this.update();
            }.bind(this));
        },

        onDissolution: function (id) {
            gatewayArmy.dissolution(id, function () {
                this.update();
            }.bind(this));
        }
    });
});