<div class="build_container" id="{{key}}">
    <div class="name btn btn-default
        {{#levelWithQueue >= maxLevel}}
        disabled
        {{/levelWithQueue >= maxLevel}}">
        {{#levelWithQueue < maxLevel}}
        <a href="#">
            {{name}} ур.
            {{#level == 0}}
            <br /><span class="level">Не построено</span>
            {{/level == 0}}
            {{#level != 0}}
            <span class="level">{{level}}</span>
            {{/level != 0}}

            <img src="/img/icons/build.png" width="20" height="16" />
        </a>
        {{/levelWithQueue < maxLevel}}
        {{#levelWithQueue >= maxLevel}}
            {{name}} ур. <span class="level">{{level}}</span>
            <img src="/img/icons/build.png" width="20" height="16" />
        {{/levelWithQueue >= maxLevel}}
    </div>

    <div class="popup">
        <div class="build-name">
            {{name}}
            {{#levelWithQueue < maxLevel}}
             ур. <span class="level">  {{levelWithQueue + 1}}</span>
            {{/level < maxLevel}}
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