define('service/town/solidersList', [
    'service/standalone/user',
    'service/standalone/messages',

    'view/town/solidersList',

    'collection/army'
], function (
    serviceStandaloneUser,
    serviceStandaloneMessages,

    VeiwTownSoliderList,

    CollectionArmy
) {
    return AbstractService.extend({
        initialize: function () {
            this.mainView = new VeiwTownSoliderList();
            this.collectionArmy = new CollectionArmy();

            serviceStandaloneMessages.on('unitsUpdate', this.update, this);
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
        }
    });
});