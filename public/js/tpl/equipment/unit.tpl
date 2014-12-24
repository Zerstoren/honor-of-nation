<div class="equipment_window">

    <div class="row">
        <div class="full-height">
            <div class="col-md-4 col-xs-4 nav">

                <div class="btn-group select-filter-equipment unit" role="group">
                    <button type="button" class="btn btn-default filter all" data-type="all">Все</button>
                    <button type="button" class="btn btn-default filter soliders" data-type="solider">Солдаты</button>
                    <button type="button" class="btn btn-default filter generals" data-type="general">Генералы</button>
                    <button type="button" class="btn add"><b class="glyphicon glyphicon-plus"></b></button>
                </div>

                <div class="equipment-items-wrapper">
                    <div class="equipments-items scrolling">

                        {{#each this.collection}}
                        <div
                            class="equipment-item row {{#this._id==unit._id}}active{{/this._id==unit._id}}"
                            data-id="{{this._id}}"
                        >
                            <div class="col-md-2 preview">
                                <img src="."/>
                            </div>
                            <div class="col-md-6 name">
                                {{this.type}} {{this.level}}
                            </div>
                            <div class="col-md-4 manipulate">
                                <button class="btn btn-default remove">Удалить</button>
                            </div>
                        </div>
                        {{/each}}
                    </div>
                </div>
            </div>
            <div class="col-md-8 col-xs-8 man">
                <div class="row">
                    <div class="col-md-9">
                        <h1>Разработка юнитов</h1>
                    </div>

                    <div class="col-md-1 header-icon-close">
                        <i class="glyphicon glyphicon-remove-circle"></i>
                    </div>
                </div>

                <div class="dev-wrapper">
                    <div class="develop well">
                        {{#this.unit}}
                        <div class="btn-group select-equipment-type" role="group">
                            <button
                                type="button"
                                class="btn btn-default active solider"
                                data-type="solider"
                                {{#unit._id}}
                                disabled="disabled"
                                {{/#unit._id}}
                            >Солдат</button>
                            <button
                                type="button"
                                class="btn btn-default general"
                                data-type="general"
                                {{#unit._id}}
                                disabled="disabled"
                                {{/#unit._id}}
                            >Генерал</button>
                        </div>

                        <div class="space"></div>

                        <div class="row">
                            <div class="col-md-4">
                                <div class="input-group">
                                    <div class="input-group-addon">Здоровье</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{unit.health}}"
                                        min="{{setting.health}}"
                                        {{#unit._id}}
                                        disabled="disabled"
                                        {{/#unit._id}}
                                    >
                                </div>

                            </div>
                            <div class="col-md-4">
                                <div class="input-group">
                                    <div class="input-group-addon">Ловкость</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{unit.agility}}"
                                        min="{{setting.agility}}"
                                        {{#unit._id}}
                                        disabled="disabled"
                                        {{/#unit._id}}
                                    >
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group">
                                    <div class="input-group-addon">Поглощение</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{unit.absorption}}"
                                        min="{{setting.absorption}}"
                                        {{#unit._id}}
                                        disabled="disabled"
                                        {{/#unit._id}}
                                    >
                                </div>
                            </div>
                        </div>

                        <div class="space"></div>

                        <div class="row">
                            <div class="col-md-4">
                                <div class="input-group">
                                    <div class="input-group-addon">Сила</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{unit.strength}}"
                                        min="{{setting.strength}}"
                                        {{#unit._id}}
                                        disabled="disabled"
                                        {{/#unit._id}}
                                    >
                                </div>

                            </div>
                            <div class="col-md-4">
                                <div class="input-group">
                                    <div class="input-group-addon">Выносливость</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{unit.stamina}}"
                                        min="{{setting.stamina}}"
                                        {{#unit._id}}
                                        disabled="disabled"
                                        {{/#unit._id}}
                                    >
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group">
                                    <div class="input-group-addon">Отряд</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{unit.troop_size}}"
                                        min="{{setting.troop_size}}"
                                        {{#unit._id}}
                                        disabled="disabled"
                                        {{/#unit._id}}
                                    >
                                </div>
                            </div>
                        </div>

                        <hr />

                        <div class="unit-equipment-wrapper">
                            <div class="row unit-equipment">
                                <div class="col-md-4 cell">
                                    <div class="armors scrolling">
                                        {{#each armor_collection}}
                                        <div
                                            class="armor cursor_pointer {{#this._id == unit.armor}}selected{{/this._id == unit.armor}}"
                                            data-id="{{this._id}}"
                                        >
                                            <img src="." width="32" height="32" />
                                            <div class="text">
                                                {{this.type}} {{this.level}}
                                            </div>
                                            <div class="reset"></div>
                                            <div class="popup">
                                                <div class="row">
                                                    <div class="col-xs-12">
                                                        Тип брони:
                                                        {{#this.type == 'leather'}}
                                                        кожа
                                                        {{/this.type == 'leather'}}
                                                        {{#this.type == 'mail'}}
                                                        кольчуга
                                                        {{/this.type == 'mail'}}
                                                        {{#this.type == 'plate'}}
                                                        латы
                                                        {{/this.type == 'plate'}}
                                                    </div>
                                                </div>

                                                <div class="row">
                                                    <div class="col-xs-6">Здоровье: {{this.health}}</div>
                                                    <div class="col-xs-6">Ловкость:  {{this.agility}}</div>
                                                </div>

                                                <div class="row">
                                                    <div class="col-xs-6">Поглощение:  {{this.absorption}}</div>
                                                </div>

                                                {{#this.shield}}
                                                    <div class="row">
                                                        <div class="col-xs-6">Прочность щита:  {{this.shield_durability}}</div>
                                                        <div class="col-xs-6">Шанс Блокировки:  {{this.shield_blocking}}</div>
                                                    </div>
                                                {{/this.shield}}

                                                <hr />

                                                <div class="row">
                                                    <div class="col-xs-6">Уровень:  {{this.level}}</div>
                                                    <div class="col-xs-6">Время:
                                                        {{formatters.fromIntToTime(this.time)}}
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-xs-6">Рубины:
                                                        {{formatters.transformNumberToPretty(this.rubins)}}
                                                    </div>
                                                    <div class="col-xs-6">Дерево:
                                                        {{formatters.transformNumberToPretty(this.wood)}}
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-xs-6">Сталь:
                                                        {{formatters.transformNumberToPretty(this.steel)}}
                                                    </div>
                                                    <div class="col-xs-6">Еда:
                                                        {{formatters.transformNumberToPretty(this.eat)}}
                                                    </div>
                                                </div>

                                            </div>
                                        </div>
                                        {{/each armor_collection}}
                                    </div>
                                </div>

                                <div class="col-md-4 cell">
                                    <div class="weapons scrolling">
                                        {{#each weapon_collection}}
                                        <div
                                            class="weapon cursor_pointer {{#this._id == unit.armor}}selected{{/this._id == unit.armor}}"
                                            data-id="{{this._id}}"
                                        >
                                            <img src="." width="32" height="32" />
                                            <div class="text">
                                                {{this.type}} {{this.level}}
                                            </div>
                                            <div class="reset"></div>
                                            <div class="popup">
                                                <div class="row">
                                                    <div class="col-xs-12">
                                                        Тип оружия:
                                                        {{#this.type == 'sword'}}
                                                        меч
                                                        {{/this.type == 'sword'}}
                                                        {{#this.type == 'blunt'}}
                                                        булава
                                                        {{/this.type == 'blunt'}}
                                                        {{#this.type == 'spear'}}
                                                        копье
                                                        {{/this.type == 'spear'}}
                                                        {{#this.type == 'bow'}}
                                                        лук
                                                        {{/this.type == 'bow'}}
                                                    </div>

                                                </div>
                                                <div class="row">
                                                    <div class="col-xs-6">Урон: {{this.damage}}</div>
                                                    <div class="col-xs-6">Сила крита:  {{this.critical_damage}}</div>
                                                </div>

                                                <div class="row">
                                                    <div class="col-xs-6">Скорость атаки:  {{this.speed}}</div>
                                                    <div class="col-xs-6">Шанс крита:  {{this.critical_chance}}</div>
                                                </div>

                                                <hr />

                                                <div class="row">
                                                    <div class="col-xs-6">Уровень: {{this.level}}</div>
                                                    <div class="col-xs-6">Время:
                                                        {{formatters.fromIntToTime(this.time)}}
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-xs-6">Рубины:
                                                        {{formatters.transformNumberToPretty(this.rubins)}}
                                                    </div>
                                                    <div class="col-xs-6">Дерево:
                                                        {{formatters.transformNumberToPretty(this.wood)}}
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-xs-6">Сталь:
                                                        {{formatters.transformNumberToPretty(this.steel)}}
                                                    </div>
                                                    <div class="col-xs-6">Еда:
                                                        {{formatters.transformNumberToPretty(this.eat)}}
                                                    </div>
                                                </div>
                                            </div>

                                        </div>
                                        {{/each weapon_collection}}
                                    </div>
                                </div>

                                <div class="col-md-4 cell">
                                    <div class="weapons-second scrolling">
                                        <div
                                            class="weapon-second cursor_pointer"
                                            data-id="none"
                                        >
                                            <img src="." width="32" height="32" />
                                            <div class="text">
                                                Без второго оружия
                                            </div>
                                            <div class="reset"></div>
                                            <div class="popup">
                                                Отменить выбор вторичного оружия
                                            </div>
                                        </div>

                                        {{#each weapon_second_collection}}
                                        <div
                                            class="weapon-second cursor_pointer {{#this._id == unit.second_weapon}}selected{{/this._id == unit.second_weapon}}"
                                            data-id="{{this._id}}"
                                        >
                                            <img src="." width="32" height="32" />
                                            <div class="text">
                                                {{this.type}} {{this.level}}
                                            </div>
                                            <div class="reset"></div>
                                            <div class="popup">
                                                <div class="row">
                                                    <div class="col-xs-12">
                                                        Тип оружия:
                                                        {{#this.type == 'sword'}}
                                                        меч
                                                        {{/this.type == 'sword'}}
                                                        {{#this.type == 'blunt'}}
                                                        булава
                                                        {{/this.type == 'blunt'}}
                                                        {{#this.type == 'spear'}}
                                                        копье
                                                        {{/this.type == 'spear'}}
                                                        {{#this.type == 'bow'}}
                                                        лук
                                                        {{/this.type == 'bow'}}
                                                    </div>

                                                </div>
                                                <div class="row">
                                                    <div class="col-xs-6">Урон: {{this.damage}}</div>
                                                    <div class="col-xs-6">Сила крита:  {{this.critical_damage}}</div>
                                                </div>

                                                <div class="row">
                                                    <div class="col-xs-6">Скорость атаки:  {{this.speed}}</div>
                                                    <div class="col-xs-6">Шанс крита:  {{this.critical_chance}}</div>
                                                </div>

                                                <hr />

                                                <div class="row">
                                                    <div class="col-xs-6">Уровень: {{this.level}}</div>
                                                    <div class="col-xs-6">Время:
                                                        {{formatters.fromIntToTime(this.time)}}
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-xs-6">Рубины:
                                                        {{formatters.transformNumberToPretty(this.rubins)}}
                                                    </div>
                                                    <div class="col-xs-6">Дерево:
                                                        {{formatters.transformNumberToPretty(this.wood)}}
                                                    </div>
                                                </div>
                                                <div class="row">
                                                    <div class="col-xs-6">Сталь:
                                                        {{formatters.transformNumberToPretty(this.steel)}}
                                                    </div>
                                                    <div class="col-xs-6">Еда:
                                                        {{formatters.transformNumberToPretty(this.eat)}}
                                                    </div>
                                                </div>
                                            </div>

                                        </div>
                                        {{/each weapon_collection}}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <hr />

                        <div class="row">
                            <div class="col-md-6">
                                <div class="row">
                                    <div class="col-md-6">Время</div>
                                    <div class="col-md-6 right">
                                        {{
                                            formatters.fromIntToTime(
                                                unit.time
                                            )
                                        }}
                                    </div>
                                </div>
                                <div class="space"></div>
                                <div class="row">
                                    <div class="col-md-6">Рубины</div>
                                    <div class="col-md-6 right">
                                        {{
                                            formatters.transformNumberToPretty(
                                                unit.rubins
                                            )
                                        }}
                                    </div>
                                </div>
                            </div>

                            <div class="col-md-6">
                                <div class="row">
                                    <div class="col-md-6">Дерево</div>
                                    <div class="col-md-6 right">
                                        {{
                                            formatters.transformNumberToPretty(
                                                unit.wood
                                            )
                                        }}
                                    </div>
                                </div>
                                <div class="space"></div>
                                <div class="row">
                                    <div class="col-md-6">Сталь</div>
                                    <div class="col-md-6 right">
                                        {{
                                            formatters.transformNumberToPretty(
                                                unit.steel
                                            )
                                        }}
                                    </div>
                                </div>
                                <div class="space"></div>
                                <div class="row">
                                    <div class="col-md-6">Еда</div>
                                    <div class="col-md-6 right">
                                        {{
                                            formatters.transformNumberToPretty(
                                                unit.eat
                                            )
                                        }}
                                    </div>
                                </div>
                            </div>

                        </div>

                        {{#!unit._id}}
                        <button class="btn btn-default save">Сохранить</button>
                        {{/unit._id}}

                    {{/this.unit}}
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>

<div class="extended-glass window-glass"></div>
