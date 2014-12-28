define('view/equipment/armor', [
    'view/equipment/abstract',
    'system/config',
    'service/standalone/user',
    'model/dummy',
    'model/equipment/armor'
], function (
    ViewEquipmentAbstract,
    systemConfig,
    serviceStandaloneUser,
    ModelDummy,
    ModelEquipmentArmor
) {
    return ViewEquipmentAbstract.extend({
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
        tpl: 'equipment/armor',

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

            serviceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (user) {
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

        afterCreateSave: function () {
            this.successMessage("Доспех успешно создано");
        },

        afterRemoveArmor: function () {
            this.successMessage("Доспех успешно удалено");
        },

        changeShieldType: function (type) {
            this.armorDomain.set('shield', type ? type : false);
            this.armorDomain.set('shield_type', type);
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

        // TODO RENAME
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
        }
    });
});
