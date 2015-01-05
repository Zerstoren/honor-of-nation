<div class="background bottom">
    <div class="nextBuilds">
        <div>
            <!--{{#queue.length}}-->
            <!--<div class="triangle">-->

                <!--<div class="popup">-->
                    <!--<div class="content">-->
                        <!--{{#each queue}}-->

                        <!--<div class="block">-->

                            <!--<div class="name">-->
                                <!--<span class="build-name">{{this.name}}</span> ур. <span class="build-level">{{this.level}}</span>-->
                            <!--</div>-->
                            <!--<div class="cancel" data-key="{{this.key}}" data-level="{{this.level}}">X</div>-->

                            <!--<div class="reset"></div>-->

                            <!--<div class="build_time">{{ formatters.fromIntToTime(this.timeToCreate) }}</div>-->
                        <!--</div>-->
                        <!--{{/each}}-->
                    <!--</div>-->
                    <!--<div class="reset"></div>-->

                <!--</div>-->
            <!--</div>-->
            <!--{{/queue}}-->
        </div>
    </div>

    <div class="buildInProgress">
        {{#firstSection}}
        <div class="name">
            <span class="build-name">{{firstSection.name}}</span> ур. <span class="build-level">{{firstSection.level}}</span>
            <span class="cancel" data-key="{{firstSection.key}}" data-level="{{firstSection.level}}">X</span>
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