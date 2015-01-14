define('view/town/solidersList', [
    'view/elements/popup',
    'view/elements/tooltip',
    'view/elements/popover',

    'model/dummy',
    'collection/army'
], function (
    ViewElementsPopup,
    ViewElementsTooltip,
    ViewElementsPopover,

    ModelDummy,
    CollectionArmy
) {
    return AbstractView.extend({
        events: {
            'click ul.units li': 'onUnitClick'
        },

        data: {
            army: null,
            icons: null,
            splitSize: 0
        },


        initialize: function () {
            this.template = this.getTemplate('town/unitsList/list');
            this.initRactive();
            this.popupUnits = null;
            this.selectedArmy = new CollectionArmy();
            this.set('icons', new ModelDummy());
            this.tooltipManager = new ViewElementsTooltip(this, 'ul.actions > li', {
                placement: 'top'
            });
        },

        render: function (holder) {
            holder.append(this.$el);

            this.popupUnits = new ViewElementsPopup(
                this.$el, {
                    liveTarget: 'ul.units li',
                    timeout: 500,
                    align: 'center',
                    ignoreTop: true
                }
            );

            this.popupSplit = new ViewElementsPopover(
                this.$el, {
                    timeout: 1,
                    liveTarget: 'li.split',
                    align: 'center',
                    valign: 'top',
                    namespace: 'manipulation'
                }
            );
            this.popupSplit.disable();

            this.popupDissolution = new ViewElementsPopover(
                this.$el, {
                    timeout: 1,
                    liveTarget: 'li.dissolution',
                    align: 'center',
                    valign: 'top',
                    namespace: 'manipulation'
                }
            );
            this.popupDissolution.disable();
        },

        setArmy: function (armyCollection) {
            this.armyCollection = armyCollection;
            this.set('army', this.armyCollection);
        },

        onUnitClick: function (e) {
            var id, target = jQuery(e.target);

            if (!jQuery.nodeName(target, 'li')) {
                target = target.parents('li');
            }

            id = target.attr('data-id');

            if (target.hasClass('active')) {
                target.removeClass('active');
                this.selectedArmy.remove(
                    this.armyCollection.search('_id', id)
                )
            } else {
                target.addClass('active');
                this.selectedArmy.push(
                    this.armyCollection.search('_id', id)
                );
            }

            this.updateIcons();
        },

        updateIcons: function () {
            this.iconCheckMerge();
            this.iconCheckSplit();
            this.iconCheckMoveOut();
            this.iconCheckAddSoliderToGeneral();
            this.iconCheckAddSuite();
            this.iconCheckDissolution();
        },

        iconCheckMerge: function () {
            var result = true,
                ids = [];

            this.selectedArmy.each(function (domain) {
                ids.push(domain.get('unit'));
                if (domain.get('unit_data').type !== 'solider') {
                    result = false;
                }
            });

            if (result && _.union(ids).length === 1 && ids.length >= 2) {
                this.get('icons').set('merge', true);
            } else {
                this.get('icons').set('merge', false);
            }
        },

        iconCheckSplit: function () {
            var result = this.selectedArmy.length === 1 &&
                    this.selectedArmy.at(0).get('unit_data').type === 'solider' &&
                        this.selectedArmy.at(0).get('count') > 1;

            this.get('icons').set('split', result);
            this.popupSplit[result ? 'enable' : 'disable']();
            if (result) {
                this.set('splitSize', this.selectedArmy.at(0).get('count'));
            }
        },

        iconCheckMoveOut: function () {
            var result,
                armyType = [];

            this.selectedArmy.each(function (domain) {
                armyType.push(domain.get('unit_data').type);
            });

            result = _.union(armyType).length === 1 && armyType[0] === 'general';
            this.get('icons').set('move_out', result);
        },

        iconCheckAddSoliderToGeneral: function () {
            var result = true,
                solider = new CollectionArmy(),
                general = null;

            this.selectedArmy.each(function (domain) {
                if (domain.get('unit_data').type === 'solider') {
                    solider.push(domain);
                } else {
                    if (general !== null) {
                        result = false;
                        return;
                    }

                    general = domain;
                }
            });

            solider.each(function (domain) {
                if (domain.get('commander')) {
                    result = false;
                }
            });

            if (solider.length === 0 || general === null) {
                result = false;
            }

            this.get('icons').set('add_soliders_to_general', result);
        },

        iconCheckAddSuite: function () {
            var result = false,
                solider = null,
                general = null;

            if (this.selectedArmy.length !== 2) {
                this.get('icons').set('add_suite', false);
                return;
            }

            if (this.selectedArmy.at(0).get('unit_data').type === 'solider') {
                solider = this.selectedArmy.at(0);
                general = this.selectedArmy.at(1);
            } else {
                solider = this.selectedArmy.at(1);
                general = this.selectedArmy.at(0);
            }

            if (
                solider.get('unit_data').type !== 'solider' ||
                general.get('unit_data').type !== 'general'
            ) {
                this.get('icons').set('add_suite', false);
                return;
            }

            result = (!general.get('suite') && !solider.get('commander'));
            this.get('icons').set('add_suite', result);
        },

        iconCheckDissolution: function () {
            var result = this.selectedArmy.length >= 1;
            this.get('icons').set('dissolution', result);
            this.popupDissolution[result ? 'enable' : 'disable']();
        }
    });
});