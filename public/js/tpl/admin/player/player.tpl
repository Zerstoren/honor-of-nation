<div class="input-group user-search">
    <span class="input-group-addon">Логин игрока</span>
    <input type="text" class="form-control search-user-login" value="{{login}}">
    <div class="input-group-btn">
        <button type="button" class="btn btn-default search-user" tabindex="-1">Искать</button>
    </div>
</div>

<div id="user-info">
    {{#user}}
        {{>info}}
    {{/user}}
</div>
