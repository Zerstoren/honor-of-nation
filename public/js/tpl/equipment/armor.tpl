<div class="equipment_window">

    <div class="row">
        <div class="full-height">
            <div class="col-md-4 col-xs-4 nav">

                <div class="btn-group select-filter-equipment" role="group">
                    <button type="button" class="btn btn-default filter all" data-type="all">Все</button>
                    <button type="button" class="btn btn-default filter leather" data-type="sword">Кожа</button>
                    <button type="button" class="btn btn-default filter mail" data-type="blunt">Кольчужные</button>
                    <button type="button" class="btn btn-default filter plate" data-type="spear">Латные</button>
                    <button type="button" class="btn btn-defaul add"><b class="glyphicon glyphicon-plus"></b></button>
                </div>

                <div class="equipment-items-wrapper">
                    <div class="equipments-items scrolling">

                        {{#each this.collection}}
                        <div
                            class="equipment-item row {{#this._id==armor._id}}active{{/this._id==armor._id}}"
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
                        <h1>Разработка доспехов</h1>
                    </div>

                    <div class="col-md-1 header-icon-close">
                        <i class="glyphicon glyphicon-remove-circle"></i>
                    </div>
                </div>

                <div class="dev-wrapper">
                    <div class="develop well">
                        {{#this.armor}}
                        <div class="btn-group select-equipment-type" role="group">
                            <button
                                type="button"
                                class="btn btn-default active leather"
                                data-type="leather"
                                {{#armor._id}}
                                disabled="disabled"
                                {{/#armor._id}}
                            >Кожа</button>
                            <button
                                type="button"
                                class="btn btn-default mail"
                                data-type="mail"
                                {{#armor._id}}
                                disabled="disabled"
                                {{/#armor._id}}
                            >Кольчуга</button>
                            <button
                                type="button"
                                class="btn btn-default plate"
                                data-type="plate"
                                {{#armor._id}}
                                disabled="disabled"
                                {{/#armor._id}}
                            >Латы</button>
                        </div>

                        <div class="space"></div><div class="space"></div><div class="space"></div>

                        <div class="row">
                            <div class="col-md-4">
                                <div class="input-group">
                                    <div class="input-group-addon">Здоровье</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{armor.health}}"
                                        {{#armor._id}}
                                        disabled="disabled"
                                        {{/#armor._id}}
                                    >
                                </div>

                            </div>
                            <div class="col-md-4">
                                <div class="input-group">
                                    <div class="input-group-addon">Ловкость</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{armor.agility}}"
                                        {{#armor._id}}
                                        disabled="disabled"
                                        {{/#armor._id}}
                                    >
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group">
                                    <div class="input-group-addon">Поглощение</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{armor.absorption}}"
                                        {{#armor._id}}
                                        disabled="disabled"
                                        {{/#armor._id}}
                                    >
                                </div>
                            </div>
                        </div>

                        <div class="space"></div><div class="space"></div><div class="space"></div>

                        <div class="row">
                            <div class="col-md-4">
                                <div class="input-group">
                                  <span class="input-group-addon">Щит</span>
                                  <select class="form-control shield_type">
                                      <option value="none">Нету</option>
                                      <option value="wood">Дерево</option>
                                      <option value="steel">Сталь</option>
                                  </select>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="input-group">
                                    <div class="input-group-addon">Прочность</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{armor.shield_durability}}"
                                        {{#!armor.shield}}
                                        disabled="disabled"
                                        {{/#!armor.shield}}
                                    >
                                </div>

                            </div>
                            <div class="col-md-4">
                                <div class="input-group">
                                    <div class="input-group-addon">Шанс блокировки</div>
                                    <input
                                        type="number"
                                        class="form-control"
                                        value="{{armor.shield_blocking}}"
                                        {{#!armor.shield}}
                                        disabled="disabled"
                                        {{/#!armor.shield}}
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
                                                armor.level
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
                                                armor.time
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
                                                armor.rubins
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
                                                armor.wood
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
                                                armor.steel
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
                                                armor.eat
                                            )
                                        }}
                                    </div>
                                </div>
                            </div>

                        </div>

                        {{#!armor._id}}
                        <button class="btn btn-default save">Сохранить</button>
                        {{/armor._id}}

                    {{/this.armor}}
                    </div>
                </div>
            </div>
        </div>
    </div>

</div>

<div class="extended-glass window-glass"></div>
