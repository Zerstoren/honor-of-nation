define('service/town/solidersList', [
    'view/town/solidersList'
], function (
    VeiwTownSoliderList
) {
    return AbstractService.extend({
        initialize: function () {
            this.mainView = new VeiwTownSoliderList();
        },

        render: function (holder, town) {
            this.mainView.render(holder, town);
        }
    });
});