<div class="form-group row">
    <div class="col-sm-2">
        <select class="user form-control" name="user" value="{{town.user}}">
            {{#each users}}
                <option value="{{_id}}">{{login}}</option>
            {{/each}}
        </select>
    </div>

    <div class="col-sm-2">
        <select class="type form-control" name="type" value="{{town.type}}">
            <option value="0">Село</option>
            <option value="1">Город</option>
            <option value="2">Замок</option>
        </select>
    </div>
</div>

<div class="form-group row">
    <div class="col-sm-2">
        <input type="number" value="{{town.population}}" class="form-control with-tooltip" data-hint="Население">
    </div>

    <div class="col-sm-2">
        <input type="text" value="{{town.position}}" class="form-control with-tooltip" data-hint="Позиция">
    </div>
</div>

<div class="form-group row">
    <div class="col-sm-2">
        <input type="text" value="{{town.name}}" class="form-control with-tooltip" data-hint="Название города">
    </div>

    <div class="col-sm-2">
        <button class="btn btn-default save">Сохранить</button>
    </div>
</div>