define('service/town/main', [
    'system/preStart',
    'system/route',
    'model/town',
    'view/town/main'
], function (
    preStart,
    systemRoute,
    ModelTown,
    ViewTownMain
) {
    return AbstractService.extend({
        render: function (townId) {
            this.holder = preStart.map.body.getHolder();
            var domain = new ModelTown();
            domain.set('id', townId);
            domain.getById(this.onTownLoad.bind(this));
        },

        onTownLoad: function (data) {

        }
    });
});