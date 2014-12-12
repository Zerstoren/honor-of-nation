<div class="equipment_window">

    <div class="row">
        <div class="full-height">
            <div class="col-md-4 col-xs-4 nav">

                <div class="btn-group select-filter-weapon" role="group">
                    <button type="button" class="btn btn-default filter all" data-type="all">Все</button>
                    <button type="button" class="btn btn-default filter sword" data-type="sword">Мечи</button>
                    <button type="button" class="btn btn-default filter blunt" data-type="blunt">Булавы</button>
                    <button type="button" class="btn btn-default filter spear" data-type="spear">Копья</button>
                    <button type="button" class="btn btn-default filter bow" data-type="bow">Луки</button>
                    <button type="button" class="btn btn-defaul add"><b class="glyphicon glyphicon-plus"></b></button>
                </div>

                <div class="weapon-items-wrapper">
                    <div class="weapons-items scrolling">

                        {{#each this.collection}}
                        <div
                            class="weapon-item row {{#this._id==weapon._id}}active{{/this._id==weapon._id}}"
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
                        <h1>Разработка оружия</h1>
                    </div>

                    <div class="col-md-1 header-icon-close">
                        <i class="glyphicon glyphicon-remove-circle"></i>
                    </div>
                </div>

                <div class="dev-wrapper">
                    <div class="develop well">
                        {{#this.weapon}}
                        <div class="btn-group select-weapon-type" role="group">
                            <button type="button" class="btn btn-default active sword" data-type="sword">Мечь</button>
                            <button type="button" class="btn btn-default blunt" data-type="blunt">Булава</button>
                            <button type="button" class="btn btn-default spear" data-type="spear">Копье</button>
                            <button type="button" class="btn btn-default bow" data-type="bow">Лук</button>
                        </div>

                        <div class="space"></div><div class="space"></div><div class="space"></div>

                        <div class="row">
                            <div class="col-md-6">
                                <div class="input-group">
                                    <div class="input-group-addon">Урон</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{weapon.damage}}"
                                        min="{{settings.damage_min}}"
                                        max="{{settings.damage_max}}"
                                        {{#weapon._id}}
                                        disabled="disabled"
                                        {{/#weapon._id}}
                                    >
                                </div>

                            </div>
                            <div class="col-md-6">
                                <div class="input-group">
                                    <div class="input-group-addon">Сила крита</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        step="0.1"
                                        value="{{weapon.critical_damage}}"
                                        min="{{settings.critical_damage_min}}"
                                        max="{{settings.critical_damage_max}}"
                                        {{#weapon._id}}
                                        disabled="disabled"
                                        {{/#weapon._id}}
                                    >
                                </div>
                            </div>
                        </div>

                        <div class="space"></div><div class="space"></div><div class="space"></div>

                        <div class="row">
                            <div class="col-md-6">
                                <div class="input-group">
                                    <div class="input-group-addon">Скорость атаки</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{weapon.speed}}"
                                        min="{{settings.speed_min}}"
                                        max="{{settings.speed_max}}"
                                        {{#weapon._id}}
                                        disabled="disabled"
                                        {{/#weapon._id}}
                                    >
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="input-group">
                                    <div class="input-group-addon">Шанс крита</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{weapon.critical_chance}}"
                                        min="{{settings.critical_chance_min}}"
                                        max="{{settings.critical_chance_max}}"
                                        {{#weapon._id}}
                                        disabled="disabled"
                                        {{/#weapon._id}}
                                    >
                                </div>
                            </div>
                        </div>

                        <div class="space"></div>

                        <hr />

                        <div class="row">
                            <div class="col-md-6">
                                <div class="row">
                                    <div class="col-md-6">Уровень</div>
                                    <div class="col-md-6 right">
                                        {{
                                            formatters.transformNumberToPretty(
                                                weapon.level
                                            )
                                        }}
                                    </div>
                                </div>
                                <div class="space"></div><div class="space"></div>
                                <div class="row">
                                    <div class="col-md-6">Время</div>
                                    <div class="col-md-6 right">
                                        {{
                                            formatters.fromIntToTime(
                                                weapon.time
                                            )
                                        }}
                                    </div>
                                </div>
                                <div class="space"></div><div class="space"></div>
                            </div>

                            <div class="col-md-6">
                                <div class="row">
                                    <div class="col-md-6">Рубины</div>
                                    <div class="col-md-6 right">
                                        {{
                                            formatters.transformNumberToPretty(
                                                weapon.rubins
                                            )
                                        }}
                                    </div>
                                </div>
                                <div class="space"></div><div class="space"></div>
                                <div class="row">
                                    <div class="col-md-6">Дерево</div>
                                    <div class="col-md-6 right">
                                        {{
                                            formatters.transformNumberToPretty(
                                                weapon.wood
                                            )
                                        }}
                                    </div>
                                </div>
                                <div class="space"></div><div class="space"></div>
                                <div class="row">
                                    <div class="col-md-6">Сталь</div>
                                    <div class="col-md-6 right">
                                        {{
                                            formatters.transformNumberToPretty(
                                                weapon.steel
                                            )
                                        }}
                                    </div>
                                </div>
                                <div class="space"></div><div class="space"></div>
                                <div class="row">
                                    <div class="col-md-6">Еда</div>
                                    <div class="col-md-6 right">
                                        {{
                                            formatters.transformNumberToPretty(
                                                weapon.eat
                                            )
                                        }}
                                    </div>
                                </div>
                            </div>

                        </div>

                        {{#!weapon._id}}
                        <button class="btn btn-default save">Сохранить</button>
                        {{/weapon._id}}

                    {{/this.weapon}}
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>

<div class="extended-glass window-glass"></div>
