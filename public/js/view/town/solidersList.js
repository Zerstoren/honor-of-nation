define('view/town/solidersList', [
    'view/elements/popup',
    'view/elements/tooltip',
    'view/elements/popover',
    'view/elements/drag',

    'model/dummy',
    'collection/army'
], function (
    ViewElementsPopup,
    ViewElementsTooltip,
    ViewElementsPopover,
    ViewElementsDrag,

    ModelDummy,
    CollectionArmy
) {
    var baseView, CommanderManipulate;

    baseView = AbstractView.extend({
        events: {
            'click ul.units li': 'onUnitClick',
            'contextmenu ul.units li': 'onUnitDetails',

            'click li.merge': 'onUnitMerge',
            'click .confirm-split': 'onUnitSplit',
            'click li.move_out': 'onMoveOut',
            'click li.add_soliders_to_general': 'onAddSolidersToGeneral',
            'click li.add_suite': 'onAddSuite',
            'click .confirm-dissolution': 'onUnitDissolution',

            'mousemove .select-split': 'onChangeSplitSize',
            'change .select-split': 'onChangeSplitSize'
        },

        data: {
            army: null,
            icons: null,

            splitSize: 0,
            splitSelectedSize: 1,
            leftSplitPosition: 1,
            rightSplitPosition: 1
        },

        initialize: function () {
            this.template = this.getTemplate('town/unitsList/list');
            this.setPartials({
                unitPopupDetail: 'town/unitsList/unitPopupDetail'
                //'unitPopoverDetail': 'town/unitsList/unitPopoverDetail'
            });

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

            this.popoverUnits = new ViewElementsPopover(
                this.$el, {
                    timeout: 1,
                    liveTarget: 'ul.units li',
                    align: 'center',
                    valign: 'top',
                    manual: true,
                    namespace: 'manipulation'
                }
            );
            this.popoverUnits.on('hide', this.onUnitDetailsHide, this);

            this.popoverSplit = new ViewElementsPopover(
                this.$el, {
                    timeout: 1,
                    liveTarget: 'li.split',
                    align: 'center',
                    valign: 'top',
                    namespace: 'manipulation'
                }
            );
            this.popoverSplit.disable();

            this.popoverDissolution = new ViewElementsPopover(
                this.$el, {
                    timeout: 1,
                    liveTarget: 'li.dissolution',
                    align: 'center',
                    valign: 'top',
                    namespace: 'manipulation'
                }
            );
            this.popoverDissolution.disable();
        },

        setArmy: function (armyCollection) {
            this.armyCollection = armyCollection;
            this.set('army', this.armyCollection);

            if (this.generalAction) {
                this.generalAction.remove();
            }

            this.generalAction = new ViewElementsDrag({
                section: this.$el.find('.units'),
                target: 'li.unit-item',
                destination: this.$el.find('li.unit-item'),
                massiveDestination: true,
                handler: this.onAttachGeneralToGeneral.bind(this)
            });



            /** FOR DEBUG **/
//            this.viewManipulate = new CommanderManipulate();
//            this.viewManipulate.render(jQuery('li[data-id="54c41f51e0460d1ccf811850"]').find('.popover'));
//
//            this.popoverUnits.showLayer({
//                currentTarget: jQuery('li[data-id="54c41f51e0460d1ccf811850"]')
//            });
//            this.popupUnits.disable();
//            this.trigger('load_details', '54c41f51e0460d1ccf811850');

        },

        onAttachGeneralToGeneral: function (from, to) {
            this.trigger('add_general_to_commander', to.attr('data-id'), from.attr('data-id'));
        },

        setDetailInfo: function (data) {
            if (this.viewManipulate) {
                this.viewManipulate.setData(data);
            }
        },

        onUnitClick: function (e) {
            if (!this.popupUnits.enabled) {
                return;
            }

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

        onUnitDetails: function (e) {
            if (this.viewManipulate) {
                return;
            }

            var id, target = jQuery(e.target);

            target = target.is('.unit-item') ? target : target.parents('.unit-item');
            id = target.attr('data-id');

            this.viewManipulate = new CommanderManipulate();
            this.viewManipulate.render(target.find('.popover'));
            this.viewManipulate.wait();
            this.trigger('load_details', id);

            this.popoverUnits.showLayer(e);
            this.popupUnits.disable();
            this.generalAction.disable();

            e.stopPropagation();
            return false;
        },

        onUnitDetailsHide: function (e) {
            setTimeout(function () {
                this.popupUnits.enable();
                this.generalAction.enable();
            }.bind(this), 0);

            this.viewManipulate.unRender();
            this.viewManipulate = null;
        },

        onUnitMerge: function () {
            this.trigger('merge', this.getSelectedUnitsIds());
            this.selectedArmy.clean();
            this.updateIcons();
        },

        onUnitSplit: function () {
            this.trigger('split', this.getSelectedUnitsIds()[0], this.get('rightSplitPosition'));
            this.selectedArmy.clean();
            this.popoverSplit.disable();
            this.updateIcons();
        },

        onMoveOut: function () {
            this.trigger('move_out', this.getSelectedUnitsIds()[0]);
            this.selectedArmy.clean();
            this.updateIcons();
        },

        onAddSolidersToGeneral: function () {
            this.trigger('add_soliders_to_general', this.selectedArmy);
            this.selectedArmy.clean();
            this.updateIcons();
        },

        onAddSuite: function () {
            this.trigger('add_suite', this.selectedArmy);
            this.selectedArmy.clean();
            this.updateIcons();
        },

        onUnitDissolution: function () {
            this.trigger('dissolution', this.getSelectedUnitsIds()[0]);
            this.selectedArmy.clean();
            this.popoverDissolution.disable();
            this.updateIcons();
        },

        onChangeSplitSize: function (e) {
            if (e && e.type === 'mousemove' && e.which !== 1) {
                return;
            }

            var max = this.get('splitSize'),
                value = this.get('splitSelectedSize');

            this.set('leftSplitPosition', max - value);
            this.set('rightSplitPosition', value);
        },

        getSelectedUnitsIds: function () {
            var result = [];
            this.selectedArmy.each(function (domain) {
                result.push(domain.get('_id'));
            });

            return result;
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
            this.popoverSplit[result ? 'enable' : 'disable']();
            if (result) {
                this.set('splitSize', this.selectedArmy.at(0).get('count'));
                this.set('rightSplitPosition', this.selectedArmy.at(0).get('count'));
                this.onChangeSplitSize();
            }
        },

        iconCheckMoveOut: function () {
            var result = this.selectedArmy.length == 1 && this.selectedArmy.at(0).get('unit_data').type === 'general';
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
                general.get('unit_data').type !== 'general' ||
                general.get('suite')
            ) {
                this.get('icons').set('add_suite', false);
                return;
            }

            result = (!general.get('suite') && !solider.get('commander'));
            this.get('icons').set('add_suite', result);
        },

        iconCheckDissolution: function () {
            var result = this.selectedArmy.length == 1;
            this.get('icons').set('dissolution', result);
            this.popoverDissolution[result ? 'enable' : 'disable']();
        }
    });

    CommanderManipulate = AbstractView.extend({
        events: {

        },

        data : {
            buffer: [],
            commander: null,
            show_general: false,
            wait: false
        },

        initialize: function () {
            this.template = this.getTemplate('town/unitsList/unitPopoverDetail');
            this.setPartials({
                unitPopupDetail: 'town/unitsList/unitPopupDetail'
                //'unitPopoverDetail': 'town/unitsList/unitPopoverDetail'
            });
            this.initRactive();

            this.popupUnits = new ViewElementsPopup(
                this.$el, {
                    liveTarget: '.popupper',
                    timeout: 500,
                    align: 'right',
                    valign: 'middle',
                    ignoreTop: true
                }
            );
        },

        render: function (holder) {
            holder.append(this.$el);

//
//
//            this.fromBufferToGeneralDrag = new ViewElementsDrag({
//                section: this.$el.find('.buffer ul'),
//                target: 'li.buffer-item',
//                destination: this.$el.find('.general-units ul'),
//                handler: this.fromGeneralToBufferHandler.bind(this)
//            });
        },

        wait: function () {
            this.set('wait', true);
        },

        setData: function (data) {
            this.set('wait', false);
            this.set('commander', data);

            this.fromGeneralToBufferDrag = new ViewElementsDrag({
                section: this.$el.find('.general-units ul'),
                target: 'li.general-item',
                destination: this.$el.find('.buffer ul'),
                handler: this.fromGeneralToBufferHandler.bind(this),

                onStart: function () {
                    this.popupUnits.disable();
                }.bind(this),

                onStop: function () {
                    this.popupUnits.enable();
                }
            });
        },

        unRender: function () {
            this.undelegateEvents();
            this.$el.empty();

            this.fromGeneralToBufferDrag.remove();
            delete this.fromGeneralToBufferDrag;
        },

        fromGeneralToBufferHandler: function (target) {

        }
    });

    return baseView;
});