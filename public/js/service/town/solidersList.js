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
            this.mainView.on('move_out', this.onMoveOut, this);
            this.mainView.on('add_soliders_to_general', this.onAddSolidersToGeneral, this);
            this.mainView.on('add_general_to_commander', this.onAddGeneralToCommander, this);
            this.mainView.on('add_suite', this.onAddSuite, this);

            this.mainView.on('remove_suite', this.onRemoveSuite, this);
            this.mainView.on('remove_general_from_commander', this.onRemoveGeneralFromCommander, this);

            this.mainView.on('load_details', this.onLoadDetails, this);
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
                }.bind(this), false, true);
            }.bind(this));
        },

        onLoadDetails: function (id) {
            serviceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (user) {
                gatewayArmy.detail(id, user, function (data) {
                    this.mainView.setDetailInfo(data);
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

        onMoveOut: function (id) {
            gatewayArmy.moveOut(id, function () {
                this.update();
            }.bind(this));
        },

        onAddSolidersToGeneral: function (selectedCollection) {
            var soliders = [],
                general = null;

            selectedCollection.each(function (domain) {
                if (domain.get('unit_data').type === 'general') {
                    general = domain.get('_id');
                } else {
                    soliders.push(domain.get('_id'));
                }
            });

            gatewayArmy.addSolidersToGeneral(soliders, general, function () {
                this.update();
            }.bind(this));
        },

        onAddGeneralToCommander: function (commnader, general) {
            gatewayArmy.addSolidersToGeneral([general], commnader, function () {
                this.update();
            }.bind(this));
        },

        onAddSuite: function (selectedCollection, silent) {
            var solider = null,
                general = null;

            selectedCollection.each(function (domain) {
                if (domain.get('unit_data').type === 'general') {
                    general = domain.get('_id');
                } else {
                    solider = domain.get('_id');
                }
            });

            gatewayArmy.addSuite(general, solider, function () {
                if (!silent) {
                    this.update();
                }
            }.bind(this));
        },

        onDissolution: function (id) {
            gatewayArmy.dissolution(id, function () {
                this.update();
            }.bind(this));
        },

        onRemoveSuite: function (solider, general) {
            gatewayArmy.removeSuite(general, solider, function () {
//                this.update();
            }.bind(this));
        },

        onRemoveGeneralFromCommander: function (solider, general) {
            gatewayArmy.removeSolidersFromGeneral(general, solider, function () {

            });
        }
    });
});