<div class="build_container">
    {{#level < maxLevel}}
    <div class="name">
        <a href="" id="{{key}}">
            {{name}} ур. <span class="level">{{level + 1}}</span>
            <img src="/img/icons/build.png" width="20" height="16" />
        </a>
    </div>
    {{/level < maxLevel}}

    {{#level > maxLevel}}
    <div class="name">
        {{name}} ур. <span class="level">{{level}}</span>
        <img src="/img/icons/build.png" width="20" height="16" />
    </div>
    {{/level > maxLevel}}

    <div class="popup">
        <div class="build-name">
            {{name}} ур.
            {{#level < maxLevel}}
            <span class="level">  {{level + 1}}</span>
            {{/level < maxLevel}}

            {{#level > maxLevel}}
            <span class="level">  {{level}}</span>
            {{/level > maxLevel}}
        </div>

        <div class="separator"></div>
        <div class="build-detail-info">
            {{#desc}}
            <div>
                <span>{{this.name}}</span>
                <p>{{this.detail}}</p>
            </div>
            {{/desc}}
        </div>
        {{#level < maxLevel}}
        <div class="build-price">
            <div class="separator"></div>
            <div class="price">Цена:</div>
            <span class="rubin">{{price.rubins}}</span>
            <span class="wood">{{price.wood}}</span><br />
            <span class="stone">{{price.stone}}</span>
            <span class="steel">{{price.steel}}</span><br />
            <span class="time">{{price.time}}</span>
        </div>
        {{/level < maxLevel}}
    </div>
</div>