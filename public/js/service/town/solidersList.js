define('service/town/solidersList', [
    'view/town/solidersList',

    'collection/army'
], function (
    VeiwTownSoliderList,

    CollectionArmy
) {
    return AbstractService.extend({
        initialize: function () {
            this.mainView = new VeiwTownSoliderList();
            this.collectionArmy = new CollectionArmy();
        },

        render: function (holder, town) {
            this.mainView.render(holder, town);
            this.collectionArmy.setTown(town);
            this.collectionArmy.load(function () {
                this.mainView.setArmy(this.collectionArmy);
            }.bind(this));
        }
    });
});