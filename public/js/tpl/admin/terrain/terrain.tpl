<div class="row">
    <div role="form" class="form-inline col-md-6">
        <div class="change-type-fill btn-group">
            <button class="btn btn-default active" data-type="coordinate">По координатам</button>
            <button class="btn btn-default" data-type="chunk">По чанкам</button>
            <br /><br /><br />
        </div>

        <div class="block-coordinate">
            <div class="input-group-sm from">
                <span>C позиции:</span> <br>
                <input type="number" min="0" max="1999" step="1"  placeholder="x" class="form-control x" value="{{position.fromX}}">
                <input type="number" min="0" max="1999" step="1"  placeholder="y" class="form-control y" value="{{position.fromY}}">
            </div>

            <div class="input-group-sm to">
                <span>По позицию:</span> <br>
                <input type="number" min="0" max="1999" step="1" placeholder="x" class="form-control x" value="{{position.toX}}">
                <input type="number" min="0" max="1999" step="1" placeholder="y" class="form-control y" value="{{position.toY}}">
            </div>
        </div>

        <div class="block-chunk" style="display: none;">
            <div class="input-group-sm">
                <span>Номер чанка:</span> <br>
                <input type="number" min="0" max="15625" step="1" class="form-control chunk" value="{{chunk}}">
            </div>

            <div class="input-group-sm chunk-position">
                <span>Позиция чанка:</span> <br>
                <input type="number" min="0" max="1999" step="1" placeholder="x" class="form-control x" value="{{searchChunk.x}}">
                <input type="number" min="0" max="1999" step="1" placeholder="y" class="form-control y" value="{{searchChunk.y}}">
            </div>

            <br>
            <button class="btn btn-default sl-add-to-list">Добавить в список</button>
            <br>

            <span>Чанки для добавления:</span>
            <span class="chunk-to-add">
                <span>
                    {{#each chunksListToAdd}}
                        {{>chunkItem}}
                    {{/each}}
                </span>
            </span>
        </div>


        <div>
            <br>
            <button class="btn btn-default send">Заполнить участок</button>
        </div>


    </div>

    <div class="fill-items col-md-6">
        <div>
            <span class="name">Долина:</span>
            <span data-type="1">
                <button class="btn btn-default" data-type="1">1</button>
            </span>
        </div>

        <div>
            <span class="name">Степь:</span>
            <span data-type="2">
                <button class="btn btn-default" data-type="1">1</button>
            </span>
        </div>

        <div>
            <span class="name">Болота:</span>
            <span data-type="3">
                <button class="btn btn-default" data-type="1">1</button>
            </span>
        </div>

        <div>
            <span class="name">Леса:</span>
            <span data-type="4">
                <button class="btn btn-default" data-type="1">1</button>
            </span>
        </div>

        <div>
            <span class="name">Джунгли:</span>
            <span data-type="5">
                <button class="btn btn-default" data-type="1">1</button>
            </span>
        </div>

        <div>
            <span class="name">Горы:</span>
            <span data-type="6">
                <button class="btn btn-default" data-type="1">1</button>
            </span>
        </div>

    </div>
</div>
