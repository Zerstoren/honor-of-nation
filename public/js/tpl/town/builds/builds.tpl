<div class="list_of_builds">
    <div class="content">
        <div>
            <div>
                {{#builds}}
                    {{>buildItem}}
                {{/builds}}
            </div>
        </div>
    </div>
</div>

<div class="list_of_progress_builds">
    <div class="background bottom">
        <div class="nextBuilds">
            <div>
                <!--popup-->
                <!--popup-callback="data.builds.func.onShowBuildsQueuePopup($target)"-->
                <!--popup-without-coordinate="true"-->
                <!--ng-show="data.builds.vars.queue"-->


                <div class="triangle">

                    <div class="popup">
                    <!--ng-resize-->
                    <!--ng-resize-height="$height - 184"-->
                    <!--scroll-->
                    <!--scroll-direction="y"-->

                    <div class="content">
                        <div class="block">
                            <!--ng-repeat="(key, build) in data.builds.vars.queue | reverse"-->

                            <div class="name">
                                Ничто
                                ур. -1
                            </div>
                            <div class="cancel" ng-click="data.builds.func.removeFromQueue(build.build, build.level)">X</div>

                            <div class="reset"></div>

                            <div class="build_time">{{ build.time_to_construct | fromIntToTime }}</div>
                        </div>
                    </div>
                </div>
                </div>
            </div>
        </div>

        <div class="buildInProgress"> <!--ng-show="data.builds.vars.queue[0].build"-->
            <div class="name">
                Ничто ур. -1
            </div>
            <div class="image">
                <!--<img src="" width="200" height="90" />-->
            </div>

            <div class="completeBar">
                <div class="progress">
                    <div class="bar" id="buildsProgressBar" style="width: 70%"></div>
                </div>
            </div>

            <div class="time">
                25 сек
            </div>
        </div>
    </div>
</div>
