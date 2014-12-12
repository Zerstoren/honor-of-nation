define('view/equipment/weapon', [
    'system/config',
    'service/standalone/user',
    'model/dummy',
    'model/equipment/weapon'
], function (
    systemConfig,
    serviceStandaloneUser,
    ModelDummy,
    ModelEquipmentWeapon
) {
    return AbstractView.extend({
        events: {
            'click .header-icon-close': 'onClose',
            'keydown global': 'onKeyDown',
            'click .weapon-item': 'onSelectWeapon',
            'click .select-filter-weapon .filter': 'onChangeFilterWeapon',
            'click .select-weapon-type button': 'onChangeWeaponType',
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

        initialize: function () {
            this.viewCollection = null;

            this.timeoutUpdate = null;
            this.selectedType = null;

            this.template = this.getTemplate('equipment/weapon');
            this.initRactive();

            this.set('settings', new ModelDummy());
        },

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

            this.changeWeaponType('sword');
            this.weaponDomain.on('change', this.onWeaponUpdate, this);

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

            this.$el.find('.select-weapon-type button').removeClass('active');
            this.$el.find('.select-weapon-type .' + type).addClass('active');
        },

        changeFilterType: function (type) {
            this.$el.find('.select-filter-weapon .filter').removeClass('active');
            this.$el.find('.select-filter-weapon .' + type).addClass('active');

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

        afterRemoveWeapon: function () {
            this.successMessage("Оружие успешно удалено");
        },

        onRemove: function (e) {
            var target = jQuery(e.target).parents('.weapon-item'),
                id = target.attr('data-id');

            this.trigger('remove', this.viewCollection.searchById(id));
            return false;
        },

        onSelectWeapon: function (e) {
            var weaponDomain,
                targetId = null;

            target = jQuery(e.target).parents('.weapon-item');

            if (!target.length) {
                target = jQuery(e.target);

                if (!target.hasClass('weapon-item')) {
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
