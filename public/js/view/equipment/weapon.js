define('view/equipment/weapon', [
    'view/equipment/abstract',
    'system/config',
    'service/standalone/user',
    'model/dummy',
    'model/equipment/weapon'
], function (
    ViewEquipmentAbstract,
    systemConfig,
    serviceStandaloneUser,
    ModelDummy,
    ModelEquipmentWeapon
) {
    return ViewEquipmentAbstract.extend({
        events: {
            'click .header-icon-close': 'onClose',
            'keydown global': 'onKeyDown',
            'click .equipment-item': 'onSelectWeapon',
            'click .select-filter-weapon .filter': 'onChangeFilterWeapon',
            'click .select-equipment-type button': 'onChangeWeaponType',
            'click .save': 'onSaveWeapon',
            'click button.add': 'onAdd',
            'click .remove': 'onRemove'
        },

        data: {
            collection: null,
            weapon: null,
            settings: null
        },

        names: ['DAMAGE', 'SPEED', 'CRITICAL_DAMAGE', 'CRITICAL_CHANCE'],

        tpl: 'equipment/weapon',

        createCurrentWeaponDomain: function () {
            if (this.weaponDomain) {
                this.weaponDomain.off('change', this.onWeaponUpdate, this);
            }

            this.weaponDomain = new ModelEquipmentWeapon();
            this.weaponDomain.set('damage', null);
            this.weaponDomain.set('speed', null);
            this.weaponDomain.set('critical_damage', null);
            this.weaponDomain.set('critical_chance', null);

            serviceStandaloneUser.getMe(function (user) {
                this.weaponDomain.set('user', user.get('_id'));
            }.bind(this));

            this.weaponDomain.on('change', this.onWeaponUpdate, this);
            this.changeWeaponType('sword');

            this.set('weapon', this.weaponDomain);
        },

        setCurrentWeaponDomain: function (weaponDomain) {
            if (this.weaponDomain) {
                this.weaponDomain.off('change', this.onWeaponUpdate, this);
            }

            this.weaponDomain = weaponDomain;
            this.changeWeaponType(this.weaponDomain.get('type'));
            this.set('weapon', this.weaponDomain);
        },

        removeCurrentWeaponDomain: function (selected) {
            if (
                selected &&
                this.weaponDomain &&
                selected.get('_id') !== this.weaponDomain.get('_id')
            ) {
                return;
            }

            this.set('weapon', null);
            this.weaponDomain = null;
        },

        changeWeaponType: function (type) {
            var name,
                typeName = type.toUpperCase(),
                config = systemConfig.getEquipmentWeapon(),
                i;

            this.weaponDomain.set('type', type);

            for (i = 0; i < this.names.length; i++) {
                name = this.names[i];

                if (this.weaponDomain.get(name.toLowerCase()) === null) {
                    this.weaponDomain.set(name.toLowerCase(), config[typeName + '_' + name + '_BASE']);
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
            this.successMessage("Оружие успешно создано");
        },

        afterRemoveWeapon: function () {
            this.successMessage("Оружие успешно удалено");
        },


        onSelectWeapon: function (e) {
            var weaponDomain,
                targetId = null;

            target = jQuery(e.target).parents('.equipment-item');

            if (!target.length) {
                target = jQuery(e.target);

                if (!target.hasClass('equipment-item')) {
                    throw Error("Wrong clicked O_o");
                }
            }

            targetId = target.attr('data-id');

            weaponDomain = new ModelEquipmentWeapon();
            weaponDomain.set('_id', targetId);
            weaponDomain.load(function () {
                this.setCurrentWeaponDomain(weaponDomain);
            }.bind(this));
        },

        onAdd: function () {
            this.createCurrentWeaponDomain();
        },

        onSaveWeapon: function () {
            this.trigger('save', this.weaponDomain);
        },

        onWeaponUpdate: function (model) {
            if (model._previousAttributes.stamp != model.get('stamp')) {
                return;
            }

            if (this.timeoutUpdate !== null) {
                clearTimeout(this.timeoutUpdate);
            }

            this.timeoutUpdate = setTimeout(function () {
                this.weaponDomain.simulate();
                this.timeoutUpdate = null;
            }.bind(this), 300);
        },

        onChangeFilterWeapon: function (e) {
            var button = jQuery(e.target),
                type = button.attr('data-type');

            this.changeFilterType(type);
        },

        onChangeWeaponType: function (e) {
            if (this.weaponDomain.get('_id')) {
                return;
            }

            var button = jQuery(e.target);
            this.changeWeaponType(button.attr('data-type'));
        }
    });
});
