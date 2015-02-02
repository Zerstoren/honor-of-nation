{{#wait == true}}
    Waiting
{{/wait == true}}
{{#wait == false}}
<div class="base-commander">
    <div class="items dynamic-left-floating">
        <div class="left-side commander">
            <h3>Командир</h3>
            <span class="popupper">
                <img src="test.png" data-id="{{this.commander.unit_data.troop_size}}" />
                {{#this.commander}}
                    {{>unitPopupDetail}}
                {{/this.commander}}
            </span>
        </div>

        <div class="right-side wrap-buffer">
            <div class="buffer vscrolling">
                <h3>Буффер</h3>
                <ul>
                    {{#each this.buffer}}
                    <li class="buffer-item popupper" data-id="{{this._id}}">
                        <img src="test.png" />
                        {{>unitPopupDetail}}
                    </li>
                    {{/each}}
                </ul>
            </div>
        </div>
    </div>
</div>

<div class="base-subordinates">
    <div class="subordinates vscrolling dynamic-left-floating">
        <div class="suite left-side {{#this.commander.suite}}popupper{{/this.commander.suite}}">
            <h3>Свита</h3>
            <img src="test.png" data-id="this.commander.suite.unit_data.troop_size" />
            {{#this.commander.suite}}
                {{>unitPopupDetail}}
            {{/this.commander.suite}}
        </div>

        <div class="general-units right-side">
            <h3>Подчиненные</h3>
            <ul>
                {{#each this.commander.sub_army}}
                {{test()}}
                <li class="general-item popupper" data-id="{{this._id}}">
                    <img src="test.png" data-id="{{this.unit_data.troop_size}}" />
                    {{>unitPopupDetail}}
                </li>
                {{/each}}
            </ul>
        </div>
    </div>
</div>

{{#show_general}}
<div class="base-soliders">
    <div class="subordinates vscrolling dynamic-left-floating">
        <div class="suite left-side">
            <h3>Свита</h3>
            <img src="test.png" />
            <div class="popup">Test</div>
        </div>

        <div class="units right-side">
            <h3>Подчиненные</h3>
            <ul>
                <li>
                    <img src="test.png" />
                    <div class="popup">Test</div>
                </li>
            </ul>
        </div>
    </div>
</div>
{{/show_general}}
{{/wait == false}}