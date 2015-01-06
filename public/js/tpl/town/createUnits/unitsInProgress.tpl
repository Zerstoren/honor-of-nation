<div class="background bottom">
    <div class="nextBuilds">
        <div>
            {{#armyQueue.length}}
            <div class="triangle">

                <div class="popup">
                    <div class="content">
                        {{#each armyQueue}}

                        <div class="block">

                            <div class="name">
                                <span class="build-name">
                                    {{#this.type == 'solider'}}
                                    Солдат
                                    {{/this.type == 'solider'}}

                                    {{#this.type == 'general'}}
                                    Генерал
                                    {{/this.type == 'general'}}
                                </span>. Кол-во <span class="build-level">{{this.count}}</span>
                            </div>
                            <div class="cancel" data-id="{{this._id}}">X</div>

                            <div class="reset"></div>

                            <div class="build_time">{{ formatters.fromIntToTime(this.timeToCreate) }}</div>
                        </div>
                        {{/each}}
                    </div>
                    <div class="reset"></div>

                </div>
            </div>
            {{/armyQueue}}
        </div>
    </div>

    <div class="buildInProgress">
        {{#firstSection}}
        <div class="name">
            <span class="build-name">
                {{#this.type == 'solider'}}
                Солдат
                {{/this.type == 'solider'}}

                {{#this.type == 'general'}}
                Генерал
                {{/this.type == 'general'}}
            </span>. Кол-во <span class="build-level">{{firstSection.count}}</span>
            <span class="cancel" data-id="{{firstSection._id}}">X</span>
        </div>
        <div class="image">
        </div>

        <div class="completeBar">
            <div class="progress">
                <div class="progress-bar bar" id="buildsProgressBar" style="width: {{firstSection.percentComplete}}%"></div>
            </div>
        </div>

        <div class="time">
            {{formatters.fromIntToTime(firstSection.timeToComplete)}}
        </div>
        {{/firstSection}}

        {{#!firstSection}}
        <div class="nothing-builds">Никто не тренируется</div>
        {{/firstSection}}
    </div>
</div>