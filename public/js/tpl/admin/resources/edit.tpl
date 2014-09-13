<div class="form-horizontal" role="form">
    <div class="form-group">
        <div class="col-sm-2">
            <input type="text" class="form-control with-tooltip coordinate" data-hint="Координаты в формате 100х100" value="{{resource.position}}"/>
        </div>
        <div class="col-sm-2">
            <select class="form-control with-tooltip resource-type" data-hint="Тип ресурса" value="{{resource.type}}">
                <option value="rubins">Рубины</option>
                <option value="wood">Дрова</option>
                <option value="steel">Сталь</option>
                <option value="stone">Камень</option>
                <option value="eat">Еда</option>
            </select>
        </div>
    </div>

    <div class="form-group">
        <div class="col-sm-2">
            <select class="form-control with-tooltip user" data-hint="Игрок" value="{{resource.user}}">
                {{#!resource.user}}
                    <option disabled>Выберите пользователя</option>
                {{/resource.user}}

                {{#each users}}
                    <option value="{{_id}}">{{login}}</option>
                {{/each}}
            </select>
        </div>
        <div class="col-sm-2">
            <select class="form-control with-tooltip town" data-hint="Город" value="{{resource.town}}">
                {{#!resource.town}}
                    <option disabled>Выберите город</option>
                {{/resource.town}}
            </select>
        </div>
    </div>

    <div class="form-group">
        <div class="col-sm-2">
            <input type="number" class="form-control with-tooltip count" data-hint="Количество залежей" value="{{resource.amount}}" />
        </div>
        <div class="col-sm-2">
            <input type="number" class="form-control with-tooltip production" data-hint="Базовая добыча" value="{{resource.base_output}}" />
        </div>
    </div>

    <button class="btn btn-default save">Сохранить</button>
</div>
