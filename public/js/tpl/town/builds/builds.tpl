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
{{>buildProgress}}
</div>
