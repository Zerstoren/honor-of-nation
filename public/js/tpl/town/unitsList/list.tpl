<ul class="actions">
    <li class="glyphicon glyphicon-resize-small merge {{#!icons.merge}}disabled{{/}}" data-hint="Объеденить юнитов"></li>
    <li class="glyphicon glyphicon-resize-full split {{#!icons.split}}disabled{{/}}" data-hint="Разделить юнита">
        <div class="popover split-block">
            <span class="split-help-number">{{leftSplitPosition}}</span>
            <input type="range" min="1" max="{{splitSize - 1}}" value="{{splitSelectedSize}}" class="select-split">
            <span class="split-help-number">{{rightSplitPosition}}</span>
            <button class="btn btn-default confirm-split">Разделить</button>
        </div>
    </li>
    <li class="glyphicon glyphicon-arrow-down move_out {{#!icons.move_out}}disabled{{/}}" data-hint="Покинуть город"></li>
    <li class="glyphicon glyphicon-log-in add_soliders_to_general {{#!icons.add_soliders_to_general}}disabled{{/}}" data-hint="Добавить солдат к командиру"></li>
    <li class="glyphicon glyphicon-import add_suite {{#!icons.add_suite}}disabled{{/}}" data-hint="Добавить солдата к командиру в качестве свиты"></li>
    <li class="glyphicon glyphicon-remove dissolution {{#!icons.dissolution}}disabled{{/}}" data-hint="Расформировать отряд">
        <div class="popover dissolution-block">
            <p style="align: center">
                Уверены что хотите расформировать выбранные отряды?
                <button class="btn btn-default confirm-dissolution">Да</button>
            </p>
        </div>
    </li>
</ul>

<div class="unitsWrap vscrolling">
    <ul class="units">
        {{#army}}
        <li data-id="{{this._id}}">
            <img src="test.png">
            {{>unitPopupDetail}}
            {{>unitPopoverDetail}}
        </li>
        {{/army}}
    </ul>
</div>