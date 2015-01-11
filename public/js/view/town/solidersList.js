define('view/town/solidersList', [
    'view/elements/popup'
], function (
    ViewElementsPopup
) {
    return AbstractView.extend({
        events: {
            'click ul.units li': 'onUnitClick'
        },

        data: {
            army: null
        },

        initialize: function () {
            this.template = this.getTemplate('town/unitsList/list');
            this.initRactive();
            this.popupUnits = null;
        },

        render: function (holder, town) {
            holder.append(this.$el);

            this.popupUnits = new ViewElementsPopup(
                this.$el, {
                    liveTarget: 'ul.units li',
                    timeout: 500,
                    align: 'center',
                    ignoreTop: true
                }
            );
        },

        setArmy: function (armyCollection) {
            this.armyCollection = armyCollection;
            this.set('army', this.armyCollection);
        },

        onUnitClick: function (e) {
            var target = jQuery(e.target);
            if (!jQuery.nodeName(target, 'li')) {
                target = target.parents('li');
            }

            if (target.hasClass('active')) {
                target.removeClass('active');
            } else {
                target.addClass('active');
            }
        }
    });
});