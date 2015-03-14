{{#wait == true}}
    <div class="waiting">Waiting</div>
{{/wait == true}}
{{#wait == false}}
<div class="base-commander">
    <div class="items dynamic-left-floating">
        <div class="left-side commander">
            <h3>Командир</h3>
            <span class="popupper">
                <img src="test.png" />
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
            <div class="suite-target-middleware {{#this.commander.suite}}suite-middleware{{/this.commander.suite}}" data-id="{{this.commander.suite._id}}">
                <img src="test.png" />
                {{#this.commander.suite}}
                    {{>unitPopupDetail}}
                {{/this.commander.suite}}
            </div>
        </div>

        <div class="general-units right-side">
            <h3>Подчиненные</h3>
            <ul class="commander-units-list">
                {{#each this.commander.sub_army}}
                <li class="general-item popupper" data-id="{{this._id}}">
                    <img src="test.png" data-id="{{this.unit_data.troop_size}}" />
                    {{>unitPopupDetail}}
                </li>
                {{/each}}
            </ul>
        </div>
    </div>
</div>

{{#general != false}}
<div class="base-soliders">
    <div class="subordinates vscrolling dynamic-left-floating">
        <div class="suite left-side {{#this.general.suite}}popupper{{/this.general.suite}}">
            <h3>Свита</h3>
            <div class="suite-target-downware {{#this.general.suite}}suite-downware{{/this.general.suite}}" data-id="{{this.general.suite._id}}">
                <img src="test.png" data-id="this.general.suite.unit_data.troop_size" />
                {{#this.general.suite}}
                    {{>unitPopupDetail}}
                {{/this.general.suite}}
            </div>
        </div>

        <div class="units right-side">
            <h3>Подчиненные</h3>
            <ul class="general-units-list">
                {{#each this.general.sub_army}}
                <li class="general-item popupper" data-id="{{this._id}}">
                    <img src="test.png" data-id="{{this.unit_data.troop_size}}" />
                    {{>unitPopupDetail}}
                </li>
                {{/each}}
            </ul>
        </div>
    </div>
</div>
{{/general != false}}
{{/wait == false}}