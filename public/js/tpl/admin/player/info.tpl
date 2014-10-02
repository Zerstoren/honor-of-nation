<div class="resources-edit form">
    <div class="input-group-sm">
        <div class="input-group">
            <span class="input-group-addon">Рубины</span>
            <input type="number" min="0" class="form-control rubins" value="{{resources.rubins}}">
        </div>

        <div class="input-group">
            <span class="input-group-addon">Дерево</span>
            <input type="number" min="0" class="form-control wood" value="{{resources.wood}}">
        </div>

        <div class="input-group">
            <span class="input-group-addon">Сталь</span>
            <input type="number" min="0" class="form-control steel" value="{{resources.steel}}">
        </div>

        <div class="input-group">
            <span class="input-group-addon">Камень</span>
            <input type="number" min="0" class="form-control stone" value="{{resources.stone}}">
        </div>

        <div class="input-group">
            <span class="input-group-addon">Еда</span>
            <input type="number" min="0" class="form-control eat" value="{{resources.eat}}">
        </div>

        <div class="input-group">
            <span class="input-group-addon">Золотые монеты</span>
            <input type="number" min="0" class="form-control gold" value="{{resources.gold}}">
        </div>
    </div>

    <button class="btn btn-default save-info">Сохранить</button>
</div>


<div class="show-terrain">
    <h4>Открыть карту</h4>
    <div class="block-coordinate form-inline" role="form">
        <div class="input-group-sm from">
            <span>C позиции:</span> <br>
            <input type="number" min="0" max="1999" step="1"  placeholder="x" class="form-control x" value="{{position.fromX}}">
            <input type="number" min="0" max="1999" step="1"  placeholder="y" class="form-control y" value="{{position.fromY}}">
        </div>

        <div class="input-group-sm to">
            <span>По позицию:</span> <br>
            <input type="number" min="0" max="1999" step="1" placeholder="x" class="form-control x"  value="{{position.toX}}">
            <input type="number" min="0" max="1999" step="1" placeholder="y" class="form-control y"  value="{{position.toY}}">
        </div>
    </div>

    <button class="btn btn-default save-coordinate">Сохранить</button>
</div>