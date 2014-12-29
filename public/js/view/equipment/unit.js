define('view/equipment/unit', [
    'view/equipment/abstract',
    'view/elements/popup',
    'system/config',
    'service/standalone/user',
    'model/dummy',
    'model/equipment/unit'
], function (
    ViewEquipmentAbstract,
    ViewElementsPopup,
    systemConfig,
    serviceStandaloneUser,
    ModelDummy,
    ModelEquipmentUnit
) {
    return ViewEquipmentAbstract.extend({
        events: {
            'click .header-icon-close': 'onClose',
            'keydown global': 'onKeyDown',
            'click .equipment-item': 'onSelectUnit',
            'click .select-filter-equipment .filter': 'onChangeFilterUnit',
            'click .select-equipment-type button': 'onChangeUnitType',
            'click .save': 'onSaveUnit',
            'click button.add': 'onAdd',
            'click .remove': 'onRemove',
            'click .armors .armor': 'onSelectArmor',
            'click .weapons .weapon': 'onSelectWeapon',
            'click .weapons-second .weapon-second': 'onSelectWeaponSecond'
        },

        data: {
            collection: null,
            unit: null,
            settings: null,
            weapon_collection: null,
            weapon_second_collection: null,
            armor_collection: null
        },

        names: ['HEALTH', 'AGILITY', 'ABSORPTION', 'STAMINA', 'STRENGTH', 'TROOP_SIZE'],
        tpl: 'equipment/unit',

        render: function (holder, collection, armorCollection, weaponCollection) {
            this.armorCollection = armorCollection;
            this.weaponCollection = weaponCollection;

            ViewEquipmentAbstract.prototype.render.apply(this, [holder, collection]);

            this.popupArmor = new ViewElementsPopup(
                this.$el, {
                    liveTarget: '.armor',
                    timeout: 100,
                    align: 'left'
                }
            );

            this.popupWeapon = new ViewElementsPopup(
                this.$el, {
                    liveTarget: '.weapon',
                    timeout: 100,
                    align: 'left'
                }
            );

            this.popupWeaponSecond = new ViewElementsPopup(
                this.$el, {
                    liveTarget: '.weapon-second',
                    timeout: 100,
                    align: 'left'
                }
            );
        },

        createCurrentUnitDomain: function () {
            if (this.unitDomain) {
                this.unitDomain.off('change', this.onUnitUpdate, this);
            }

            this.unitDomain = new ModelEquipmentUnit();
            this.unitDomain.set('_id', null);
            this.unitDomain.set('health', null);
            this.unitDomain.set('agility', null);
            this.unitDomain.set('absorption', null);
            this.unitDomain.set('stamina', null);
            this.unitDomain.set('strength', null);
            this.unitDomain.set('troop_size', null);

            this.unitDomain.set('armor', null);
            this.unitDomain.set('weapon', null);
            this.unitDomain.set('weapon_second', null);

            serviceStandaloneUser.getDeffer().deffer(DefferedTrigger.ON_GET, function (user) {
                this.unitDomain.set('user', user.get('_id'));
            }.bind(this));


            this.set('weapon_collection', this.weaponCollection);
            this.set('weapon_second_collection', this.weaponCollection);
            this.set('armor_collection', this.armorCollection);
            this.set('unit', this.unitDomain);

            this.unitDomain.on('change', this.onUnitUpdate, this);
            this.changeUnitType('solider');
        },

        setCurrentUnitDomain: function (unitDomain) {
            if (this.unitDomain) {
                this.unitDomain.off('change', this.onUnitUpdate, this);
            }

            this.unitDomain = unitDomain;
            this.set('weapon_collection', null);
            this.set('weapon_second_collection', null);
            this.set('armor_collection', null);
            this.set('unit', this.unitDomain);
            this.changeUnitType(this.unitDomain.get('type'));

        },

        removeCurrentUnitDomain: function (selected) {
            if (
                selected &&
                this.unitDomain &&
                selected.get('_id') !== this.unitDomain.get('_id')
            ) {
                return;
            }

            this.set('unit', null);
            this.unitDomain = null;
        },

        changeUnitType: function (type) {
            var name,
                config = systemConfig.getEquipmentUnit(),
                i;

            this.unitDomain.set('type', type);

            for (i = 0; i < this.names.length; i++) {
                name = this.names[i];

                if (this.unitDomain.get(name.toLowerCase()) === null) {
                    this.unitDomain.set(name.toLowerCase(), config['UNIT_' + name]);
                }

                this.data.settings.set(
                    name.toLowerCase(),
                    config['unit_' + name] || 0
                );
            }

            this.$el.find('.select-equipment-type button').removeClass('active');
            this.$el.find('.select-equipment-type .' + type).addClass('active');
        },

        afterCreateSave: function () {
            this.successMessage("Оружие успешно создано");
        },

        afterRemoveUnit: function () {
            this.successMessage("Оружие успешно удалено");
        },

        changeShieldType: function (type) {
            this.unitDomain.set('shield', type ? type : false);
            this.unitDomain.set('shield_type', type);
        },

        onSelectArmor: function (e) {
            var target = $(e.target),
                id = null;
            if (target.hasClass('armor')) {
                id = target.attr('data-id');
            } else {
                id = target.parents('.armor').attr('data-id');
            }

            this.selectArmor(id);
        },

        // @TODO Refactor this shit
        selectArmor: function (id) {
            var armor, weapon;

            this.$el.find('.armor[data-id]').removeClass('selected');
            this.$el.find('.armor[data-id="' + id  + '"]').addClass('selected');

            this.unitDomain.set('armor', id);

            armor = this.armorCollection.search('_id', id);

            if (armor.get('shield')) {
                this.set(
                    'weapon_collection',
                    this.weaponCollection.whereIn('type', ['sword', 'blunt'])
                );

                this.set(
                    'weapon_second_collection',
                    this.weaponCollection.whereIn('type', ['sword', 'blunt'])
                );
            }

            this.selectWeapon(this.unitDomain.get('weapon'));
            this.selectWeaponSecond(this.unitDomain.get('weapon_second'));
        },

        // @TODO Refactor this shit
        selectWeapon: function (id) {
            this.$el.find('.weapon[data-id]').removeClass('selected');

            if (id) {
                this.$el.find('.weapon[data-id="' + id  + '"]').addClass('selected');
            }

            this.unitDomain.set('weapon', id);

            var secondWeapon,
                armor,
                weapon = this.weaponCollection.search('_id', this.unitDomain.get('weapon'));

            if (weapon && _.contains(['bow', 'spear'], weapon.get('type'))) {
                if (this.unitDomain.get('weapon_second')) {
                    secondWeapon = this.weaponCollection.search('_id', this.unitDomain.get('weapon_second'));
                    if (_.contains(['bow', 'spear'], secondWeapon.get('type'))) {
                        this.set('weapon_second', null);
                    }
                }

                this.set('weapon_second_collection', this.weaponCollection.whereIn('type', ['sword', 'blunt']));
            } else {
                armor = this.armorCollection.search('_id', this.unitDomain.get('armor'));

                if (armor && armor.get('shield')) {
                    this.set('weapon_second_collection', this.weaponCollection.whereIn('type', ['sword', 'blunt']));
                } else {
                    this.set('weapon_second_collection', this.weaponCollection);
                }
            }
        },

        // @TODO Refactor this shit
        selectWeaponSecond: function (id) {
            this.$el.find('.weapon-second[data-id]').removeClass('selected');

            if (id) {
                this.$el.find('.weapon-second[data-id="' + id  + '"]').addClass('selected');
            }

            this.unitDomain.set('weapon_second', id);

            var weapon,
                armor,
                secondWeapon = this.weaponCollection.search('_id', this.unitDomain.get('weapon_second'));

            if (secondWeapon && _.contains(['bow', 'spear'], secondWeapon.get('type'))) {
                if (this.unitDomain.get('weapon')) {
                    weapon = this.weaponCollection.search('_id', this.unitDomain.get('weapon'));
                    if (_.contains(['bow', 'spear'], weapon.get('type'))) {
                        this.set('weapon', null);
                    }
                }

                this.set('weapon_collection', this.weaponCollection.whereIn('type', ['sword', 'blunt']));
            } else {
                armor = this.armorCollection.search('_id', this.unitDomain.get('armor'));

                if (armor && armor.get('shield')) {
                    this.set('weapon_collection', this.weaponCollection.whereIn('type', ['sword', 'blunt']));
                } else {
                    this.set('weapon_collection', this.weaponCollection);
                }
            }
        },

        onSelectWeapon: function (e) {
            var target = $(e.target),
                id = null;
            if (target.hasClass('weapon')) {
                id = target.attr('data-id');
            } else {
                id = target.parents('.weapon').attr('data-id');
            }

            this.selectWeapon(id);
        },

        onSelectWeaponSecond: function (e) {
            var target = $(e.target),
                id = null;
            if (target.hasClass('weapon-second')) {
                id = target.attr('data-id');
            } else {
                id = target.parents('.weapon-second').attr('data-id');
            }

            if (id === 'none') {
                id = null;
            }

            this.selectWeaponSecond(id);
        },

        onSelectUnit: function (e) {
            var unitDomain;

            target = jQuery(e.target).parents('.equipment-item');

            if (!target.length) {
                target = jQuery(e.target);

                if (!target.hasClass('equipment-item')) {
                    throw Error("Wrong clicked O_o");
                }
            }

            targetId = target.attr('data-id');

            unitDomain = new ModelEquipmentUnit();
            unitDomain.set('_id', targetId);
            unitDomain.load(function () {
                this.setCurrentUnitDomain(unitDomain);
            }.bind(this));
        },

        onAdd: function () {
            this.createCurrentUnitDomain();
        },

        onSaveUnit: function () {
            this.trigger('save', this.unitDomain);
        },

        onUnitUpdate: function (model) {
            if (model._previousAttributes.stamp != model.get('stamp')) {
                return;
            }

            if (this.timeoutUpdate !== null) {
                clearTimeout(this.timeoutUpdate);
            }

            this.timeoutUpdate = setTimeout(function () {
                this.unitDomain.simulate();
                this.timeoutUpdate = null;
            }.bind(this), 300);
        },

        onChangeFilterUnit: function (e) {
            var button = jQuery(e.target),
                type = button.attr('data-type');

            this.changeFilterType(type);
        },

        onChangeUnitType: function (e) {
            if (this.unitDomain.get('_id')) {
                return;
            }

            var button = jQuery(e.target);
            this.changeUnitType(button.attr('data-type'));
        }
    });
});
