define('view/equipment/armor', [
    'system/config',
    'service/standalone/user',
    'model/dummy',
    'model/equipment/armor'
], function (
    systemConfig,
    serviceStandaloneUser,
    ModelDummy,
    ModelEquipmentArmor
) {
    return AbstractView.extend({
        events: {
            'click .header-icon-close': 'onClose',
            'keydown global': 'onKeyDown',
            'change .shield_type': 'onChangeShieldType',
            'click .equipment-item': 'onSelectArmor',
            'click .select-filter-equipment .filter': 'onChangeFilterArmor',
            'click .select-equipment-type button': 'onChangeArmorType',
            'click .save': 'onSaveArmor',
            'click button.add': 'onAdd',
            'click .remove': 'onRemove'
        },

        data: {
            collection: null,
            armor: null,
            settings: null
        },

        names: ['HEALTH', 'AGILITY', 'ABSORPTION'],

        initialize: function () {
            this.viewCollection = null;

            this.timeoutUpdate = null;
            this.selectedType = null;

            this.template = this.getTemplate('equipment/armor');
            this.initRactive();

            this.set('settings', new ModelDummy());
        },

        createCurrentArmorDomain: function () {
            if (this.armorDomain) {
                this.armorDomain.off('change', this.onArmorUpdate, this);
            }

            this.armorDomain = new ModelEquipmentArmor();
            this.armorDomain.set('health', null);
            this.armorDomain.set('agility', null);
            this.armorDomain.set('absorption', null);

            this.armorDomain.set('shield_durability', 0);
            this.armorDomain.set('shield_blocking', 0);

            serviceStandaloneUser.getMe(function (user) {
                this.armorDomain.set('user', user.get('_id'));
            }.bind(this));


            this.set('armor', this.armorDomain);

            this.armorDomain.on('change', this.onArmorUpdate, this);
            this.changeArmorType('leather');
            this.changeShieldType(null);


        },

        setCurrentArmorDomain: function (armorDomain) {
            if (this.armorDomain) {
                this.armorDomain.off('change', this.onArmorUpdate, this);
            }

            this.armorDomain = armorDomain;
            this.changeArmorType(this.armorDomain.get('type'));
            this.set('armor', this.armorDomain);
        },

        removeCurrentArmorDomain: function (selected) {
            if (
                selected &&
                this.armorDomain &&
                selected.get('_id') !== this.armorDomain.get('_id')
            ) {
                return;
            }

            this.set('armor', null);
            this.armorDomain = null;
        },

        render: function (holder, collection) {
            this.viewCollection = collection;
            this.viewCollection.on('change', this.onChangeCollection, this);
            this.viewCollection.on('reset', this.onChangeCollection, this);
            this.changeFilterType('all');

            holder.append(this.$el);

            this.delegateEvents();
        },

        unRender: function () {
            this.$el.remove();
            this.undelegateEvents();
        },

        changeArmorType: function (type) {
            var name,
                typeName = type.toUpperCase(),
                config = systemConfig.getEquipmentArmor(),
                i;

            this.armorDomain.set('type', type);

            for (i = 0; i < this.names.length; i++) {
                name = this.names[i];

                if (this.armorDomain.get(name.toLowerCase()) === null) {
                    this.armorDomain.set(name.toLowerCase(), config[typeName + '_' + name + '_BASE']);
                }

                this.data.settings.set(
                    name.toLowerCase() + '_min',
                    config[typeName + '_' + name + '_MIN'] || 0
                );
                this.data.settings.set(
                    name.toLowerCase() + '_max',
                    config[typeName + '_' + name + '_MAX'] || 9999999999999999999
                );
            }

            this.$el.find('.select-equipment-type button').removeClass('active');
            this.$el.find('.select-equipment-type .' + type).addClass('active');
        },

        changeFilterType: function (type) {
            this.$el.find('.select-filter-equipment .filter').removeClass('active');
            this.$el.find('.select-filter-equipment .' + type).addClass('active');

            if (type === 'all') {
                this.selectedType = null;
                this.onChangeCollection(this.viewCollection);
            } else {
                this.selectedType = type;
                this.onChangeCollection(this.viewCollection, type);
            }
        },

        afterCreateSave: function () {
            this.successMessage("Оружие успешно создано");
        },

        afterRemoveArmor: function () {
            this.successMessage("Оружие успешно удалено");
        },

        changeShieldType: function (type) {
            this.armorDomain.set('shield', type ? type : false);
            this.armorDomain.set('shield_type', type);
        },

        onRemove: function (e) {
            var target = jQuery(e.target).parents('.equipment-item'),
                id = target.attr('data-id');

            this.trigger('remove', this.viewCollection.searchById(id));
            return false;
        },

        onSelectArmor: function (e) {
            var armorDomain;

            target = jQuery(e.target).parents('.equipment-item');

            if (!target.length) {
                target = jQuery(e.target);

                if (!target.hasClass('equipment-item')) {
                    throw Error("Wrong clicked O_o");
                }
            }

            targetId = target.attr('data-id');

            armorDomain = new ModelEquipmentArmor();
            armorDomain.set('_id', targetId);
            armorDomain.load(function () {
                this.setCurrentArmorDomain(armorDomain);
            }.bind(this));
        },

        onAdd: function () {
            this.createCurrentArmorDomain();
        },

        onChangeCollection: function (collection, type) {
            var viewCollection = collection.clone();
            viewCollection.sort();

            if (type === undefined) {
                type = this.selectedType;
            }

            if (type !== null) {
                viewCollection = viewCollection.where({type: type});
            }

            this.set('collection', viewCollection);
        },

        onSaveArmor: function () {
            this.trigger('save', this.armorDomain);
        },

        onArmorUpdate: function (model) {
            if (model._previousAttributes.stamp != model.get('stamp')) {
                return;
            }

            if (this.timeoutUpdate !== null) {
                clearTimeout(this.timeoutUpdate);
            }

            this.timeoutUpdate = setTimeout(function () {
                this.armorDomain.simulate();
                this.timeoutUpdate = null;
            }.bind(this), 300);
        },

        onChangeFilterArmor: function (e) {
            var button = jQuery(e.target),
                type = button.attr('data-type');

            this.changeFilterType(type);
        },

        onChangeArmorType: function (e) {
            if (this.armorDomain.get('_id')) {
                return;
            }

            var button = jQuery(e.target);
            this.changeArmorType(button.attr('data-type'));
        },

        onChangeShieldType: function (e) {
            var target = jQuery(e.target),
                type = target.val();

            if (type === 'none') {
                type = null;
            }

            this.changeShieldType(type);
        },

        onClose: function () {
            this.unRender();
            this.trigger('close');
        },

        onKeyDown: function (e) {
            if (e.keyCode === this.keyCodes.esc) {
                this.onClose();
            }
        }
    });
});
