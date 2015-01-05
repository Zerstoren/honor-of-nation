<div class="units_container" id="{{_id}}">
    <div class="name btn btn-default">
        <a href="#">
            {{#this.type == 'solider'}}
            Солдат
            {{/this.type == 'solider'}}

            {{#this.type == 'general'}}
            Генерал
            {{/this.type == 'general'}}
        </a>
    </div>

    <div class="popup">
        <div class="head">Параметры:</div>
        <div class="row">
            <div class="col-xs-4">Здоровье: {{this.health}}</div>
            <div class="col-xs-4">Ловеость: {{this.agility}}</div>
            <div class="col-xs-4">Поглощение: {{this.absorption}}</div>
        </div>

        <div class="row">
            <div class="col-xs-4">Сила: {{this.strength}}</div>
            <div class="col-xs-4">Выносливость: {{this.stamina}}</div>
            <div class="col-xs-4">
                {{#this.type == 'general'}}
                Отряд: {{this.troop_size}}
                {{/this.type == 'general'}}
            </div>
        </div>


        <hr class="short" />
        <div class="head">
            Доспех:
            {{#this.armor_data.type == 'leather'}}
            кожа
            {{/this.armor_data.type == 'leather'}}
            {{#this.armor_data.type == 'mail'}}
            кольчуга
            {{/this.armor_data.type == 'mail'}}
            {{#this.armor_data.type == 'plate'}}
            латы
            {{/this.armor_data.type == 'plate'}}

        </div>
        <div class="row">
            <div class="col-xs-4">Здоровье: {{this.armor_data.health}}</div>
            <div class="col-xs-4">Ловкость: {{this.armor_data.agility}}</div>
            <div class="col-xs-4">Поглощение: {{this.armor_data.absorption}}</div>
        </div>

        {{#this.armor_data.shield}}
        <div class="head">Щит</div>
        <div class="row">
            <div class="col-xs-6">Прочность: {{this.armor_data.shield_durability}}</div>
            <div class="col-xs-6">Шанс блокировки: {{this.armor_data.shield_blocking}}</div>
        </div>
        {{/this.armor_data.shield}}

        <hr class="short" />
        <div class="head">Оружие:
            {{#this.weapon_data.type == 'sword'}}
            меч
            {{/this.weapon_data.type == 'sword'}}
            {{#this.weapon_data.type == 'blunt'}}
            булава
            {{/this.weapon_data.type == 'blunt'}}
            {{#this.weapon_data.type == 'spear'}}
            копье
            {{/this.weapon_data.type == 'spear'}}
            {{#this.weapon_data.type == 'bow'}}
            лук
            {{/this.weapon_data.type == 'bow'}}
        </div>

        <div class="row">
            <div class="col-xs-6">Урон: {{this.weapon_data.damage}}</div>
            <div class="col-xs-6">Скорость атаки: {{this.weapon_data.speed}}</div>
        </div>
        <div class="row">
            <div class="col-xs-6">Сила крита: {{this.weapon_data.critical_damage}}</div>
            <div class="col-xs-6">Шанс крита: {{this.weapon_data.critical_chance}}</div>
        </div>

        {{#this.weapon_second}}
        <hr class="short" />
        <div class="head">Второе оружие:
            {{#this.weapon_second_data.type == 'sword'}}
            меч
            {{/this.weapon_second_data.type == 'sword'}}
            {{#this.weapon_second_data.type == 'blunt'}}
            булава
            {{/this.weapon_second_data.type == 'blunt'}}
            {{#this.weapon_second_data.type == 'spear'}}
            копье
            {{/this.weapon_second_data.type == 'spear'}}
            {{#this.weapon_second_data.type == 'bow'}}
            лук
            {{/this.weapon_second_data.type == 'bow'}}
        </div>

        <div class="row">
            <div class="col-xs-6">Урон: {{this.weapon_second_data.damage}}</div>
            <div class="col-xs-6">Скорость атаки: {{this.weapon_second_data.speed}}</div>
        </div>
        <div class="row">
            <div class="col-xs-6">Сила крита: {{this.weapon_second_data.critical_damage}}</div>
            <div class="col-xs-6">Шанс крита: {{this.weapon_second_data.critical_chance}}</div>
        </div>
        {{/this.weapon_second}}

        <hr />

        <div class="head">Траты:</div>

        <div class="row">
            <div class="col-xs-6">
                <div class="price">Рубины: {{formatters.transformNumberToPretty(this.rubins * createCount)}}</div>
            </div>
            <div class="col-xs-6">
                <div class="price">Дерево: {{formatters.transformNumberToPretty(this.wood * createCount)}}</div>
            </div>
        </div>
        <div class="row">
            <div class="col-xs-6">
                <div class="price">Сталь: {{formatters.transformNumberToPretty(this.steel * createCount)}}</div>
            </div>
            <div class="col-xs-6"><div class="price">Еда: {{formatters.transformNumberToPretty(this.eat * createCount)}}</div></div>
        </div>
        <div class="row">
            <div class="col-xs-12">
                <div class="price">Время: {{formatters.fromIntToTime(this.time * createCount)}}</div>
            </div>
        </div>

        <hr />

       <div class="input-group">
            <input
                type="number"
                class="form-control field_strength"
                value="{{createCount}}"
                min="1"
                max="100"
            >
            <div class="input-group-btn">
                <button class="btn btn-default">Создать</button>
            </div>
        </div>

    </div>
</div>
