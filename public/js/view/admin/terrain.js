define('view/admin/terrain', [

    'service/standalone/gameMap',
    'view/block/error'
], function (
    gameMap,
    viewBlockError
) {
    return AbstractView.extend({
        className: 'terrain',
        events: {
            'click .change-type-fill > button': 'onChangeFillType',
            'click .sl-add-to-list'           : 'onAddToList',
            'click .chunk-to-add a'           : 'onRemoveFromList',
            'click .fill-items button'        : 'onSelectLandType',
            'click .send'                     : 'onSend'
        },

        initialize: function () {
            this.chunksListToAdd = [];
            this.fillType = 'coordinate';
            this.fillLand = null;
            this.fillLandType = null;
        },

        render: function (holder) {
            this.$el.html(this.template('admin/terrain/terrain'));
            holder.append(this.$el);
            this.delegateEvents();
        },

        unRender: function () {
            this.$el.remove();
            this.undelegateEvents();
        },

        successSave: function () {
            viewBlockError.showSuccessBox('Terrain save successful');
        },

        _renderChunkList: function () {
            var i,
                el,
                holder = this.$el.find('.chunk-to-add');

            holder.empty();

            for (i = 0; i < this.chunksListToAdd.length; i += 1) {
                el = $('<span>');
                el.html(
                    template('admin/terrain/chunkItem', {chunk: this.chunksListToAdd[i]})
                );
                holder.append(el);
            }
        },

        onChangeFillType: function (e) {
            var target = $(e.target);
            this.$el.find('.change-type-fill button').removeClass('active');
            target.addClass('active');

            this.fillType = target.data('type');

            this.$el.find('.block-coordinate').hide();
            this.$el.find('.block-chunk').hide();
            this.$el.find('.block-' + target.data('type')).show();
        },

        onAddToList: function () {
            var x,
                y,
                chunkNum = parseInt(this.$el.find('.block-chunk input.chunk').val(), 10);

            if (isNaN(chunkNum)) {
                x = parseInt(this.$el.find('.block-chunk input.x').val(), 10);
                y = parseInt(this.$el.find('.block-chunk input.y').val(), 10);

                chunkNum = gameMap.help.fromPlaceToChunk(x, y);

                if (isNaN(chunkNum)) {
                    return;
                }
            }

            if (this.chunksListToAdd.indexOf(chunkNum) === -1) {
                this.chunksListToAdd.push(chunkNum);
            }

            this.$el.find('.block-chunk input.chunk').val('');
            this.$el.find('.block-chunk input.x').val('');
            this.$el.find('.block-chunk input.y').val('');

            this._renderChunkList();
        },

        onRemoveFromList: function (e) {
            var chunk = parseInt($(e.target).data('chunk'), 10);
            this.chunksListToAdd = _.without(this.chunksListToAdd, chunk);
            this._renderChunkList();
        },

        onSelectLandType: function (e) {
            var target = $(e.target);
            this.fillLandType = target.data('type');
            this.fillLand = target.parent().data('type');

            $('.fill-items button').removeClass('active');
            target.addClass('active');
        },

        onSend: function () {
            var send;

            if (this.fillType === 'coordinate') {
               send = {
                   type: 'coordinate',
                   coordinate: {
                       fromX: parseInt(this.$el.find('.from .x').val(), 10),
                       fromY: parseInt(this.$el.find('.from .y').val(), 10),
                       toX  : parseInt(this.$el.find('.to .x').val(), 10),
                       toY  : parseInt(this.$el.find('.to .y').val(), 10)
                   }
               };

                if (isNaN(send.coordinate.fromX) ||
                    isNaN(send.coordinate.fromY) ||
                    isNaN(send.coordinate.toX) ||
                    isNaN(send.coordinate.toY)
                ) {
                    return;
                }

            } else {
                send = {
                   type: 'chunk',
                   chunks: _.clone(this.chunksListToAdd)
                };

                this.chunksListToAdd = [];
            }

            send.fillLand = this.fillLand;
            send.fillLandType = this.fillLandType;

            if (!this.fillLandType) {
                return;
            }

            this.trigger('send', send);
        }
    });
});