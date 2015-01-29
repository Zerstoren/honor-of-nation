<div class="popup">
    <h4 class="head">
        {{#this.unit_data.type == 'solider'}}
        Солдат {{this.count}} ед.
        {{/this.unit_data.type == 'solider'}}
        {{#this.unit_data.type == 'general'}}
        Генерал
        {{/this.unit_data.type == 'general'}}
    </h4>
    <div class="head">Параметры:</div>
    <div class="row">
        <div class="col-xs-4">Здоровье: {{this.unit_data.health}}</div>
        <div class="col-xs-4">Ловкость: {{this.unit_data.agility}}</div>
        <div class="col-xs-4">Поглощение: {{this.unit_data.absorption}}</div>
    </div>

    <div class="row">
        <div class="col-xs-4">Сила: {{this.unit_data.strength}}</div>
        <div class="col-xs-4">Выносливость: {{this.unit_data.stamina}}</div>
        <div class="col-xs-4">
            {{#this.unit_data.type == 'general'}}
            Отряд: {{this.unit_data.troop_size}}
            {{/this.unit_data.type == 'general'}}
        </div>
    </div>


    <hr class="short" />
    <div class="head">
        Доспех:
        {{#this.unit_data.armor_data.type == 'leather'}}
        кожа
        {{/this.unit_data.armor_data.type == 'leather'}}
        {{#this.unit_data.armor_data.type == 'mail'}}
        кольчуга
        {{/this.unit_data.armor_data.type == 'mail'}}
        {{#this.unit_data.armor_data.type == 'plate'}}
        латы
        {{/this.unit_data.armor_data.type == 'plate'}}

    </div>
    <div class="row">
        <div class="col-xs-4">Здоровье: {{this.unit_data.armor_data.health}}</div>
        <div class="col-xs-4">Ловкость: {{this.unit_data.armor_data.agility}}</div>
        <div class="col-xs-4">Поглощение: {{this.unit_data.armor_data.absorption}}</div>
    </div>

    {{#this.armor_data.shield}}
    <div class="head">Щит</div>
    <div class="row">
        <div class="col-xs-6">Прочность: {{this.unit_data.armor_data.shield_durability}}</div>
        <div class="col-xs-6">Шанс блокировки: {{this.unit_data.armor_data.shield_blocking}}</div>
    </div>
    {{/this.armor_data.shield}}

    <hr class="short" />
    <div class="head">Оружие:
        {{#this.unit_data.weapon_data.type == 'sword'}}
        меч
        {{/this.unit_data.weapon_data.type == 'sword'}}
        {{#this.unit_data.weapon_data.type == 'blunt'}}
        булава
        {{/this.unit_data.weapon_data.type == 'blunt'}}
        {{#this.unit_data.weapon_data.type == 'spear'}}
        копье
        {{/this.unit_data.weapon_data.type == 'spear'}}
        {{#this.unit_data.weapon_data.type == 'bow'}}
        лук
        {{/this.unit_data.weapon_data.type == 'bow'}}
    </div>

    <div class="row">
        <div class="col-xs-6">Урон: {{this.unit_data.weapon_data.damage}}</div>
        <div class="col-xs-6">Скорость атаки: {{this.unit_data.weapon_data.speed}}</div>
    </div>
    <div class="row">
        <div class="col-xs-6">Сила крита: {{this.unit_data.weapon_data.critical_damage}}</div>
        <div class="col-xs-6">Шанс крита: {{this.unit_data.weapon_data.critical_chance}}</div>
    </div>

    {{#this.unit_data.weapon_second}}
    <hr class="short" />
    <div class="head">Второе оружие:
        {{#this.unit_data.weapon_second_data.type == 'sword'}}
        меч
        {{/this.unit_data.weapon_second_data.type == 'sword'}}
        {{#this.unit_data.weapon_second_data.type == 'blunt'}}
        булава
        {{/this.unit_data.weapon_second_data.type == 'blunt'}}
        {{#this.unit_data.weapon_second_data.type == 'spear'}}
        копье
        {{/this.unit_data.weapon_second_data.type == 'spear'}}
        {{#this.unit_data.weapon_second_data.type == 'bow'}}
        лук
        {{/this.unit_data.weapon_second_data.type == 'bow'}}
    </div>

    <div class="row">
        <div class="col-xs-6">Урон: {{this.unit_data.weapon_second_data.damage}}</div>
        <div class="col-xs-6">Скорость атаки: {{this.unit_data.weapon_second_data.speed}}</div>
    </div>
    <div class="row">
        <div class="col-xs-6">Сила крита: {{this.unit_data.weapon_second_data.critical_damage}}</div>
        <div class="col-xs-6">Шанс крита: {{this.unit_data.weapon_second_data.critical_chance}}</div>
    </div>
    {{/this.unit_data.weapon_second}}
</div>