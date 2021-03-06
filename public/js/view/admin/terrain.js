define('view/admin/terrain', [
    'service/standalone/map',
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
            this.template = this.getTemplate('admin/terrain/terrain');

            this.partials = {
                chunkItem: this.getTemplate('admin/terrain/chunkItem')
            };

            this.initRactive();
        },

        data: {
            position: {
                fromX: null,
                fromY: null,
                toX  : null,
                toY  : null
            },
            chunk: null,
            searchChunk: {
                x: null,
                y: null
            },
            chunkListToAdd: []
        },

        render: function (holder) {
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
                chunkNum = parseInt(this.get('chunk'), 10);

            if (isNaN(chunkNum)) {
                x = parseInt(this.get('searchChunk').x, 10);
                y = parseInt(this.get('searchChunk').y, 10);

                chunkNum = gameMap.help.fromPlaceToChunk(x, y);

                if (isNaN(chunkNum)) {
                    return;
                }
            }

            if (this.chunksListToAdd.indexOf(chunkNum) === -1) {
                this.chunksListToAdd.push(chunkNum);
            }

            this.set('chunk', null);
            this.set('searchChunk', {x: null, y: null});
            this.set('chunksListToAdd', this.chunksListToAdd);
        },

        onRemoveFromList: function (e) {
            var chunk = parseInt($(e.target).data('chunk'), 10);
            this.chunksListToAdd = _.without(this.chunksListToAdd, chunk);
            this.set('chunksListToAdd', this.chunksListToAdd);
        },

        onSelectLandType: function (e) {
            var target = $(e.target);
            this.fillLandType = target.data('type');
            this.fillLand = target.parent().data('type');

            this.$el.find('.fill-items button').removeClass('active');
            target.addClass('active');
        },

        onSend: function () {
            var send;

            if (this.fillType === 'coordinate') {
               send = {
                   type: 'coordinate',
                   coordinate: this.get('position')
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
                   type: 'chunks',
                   chunks: _.clone(this.chunksListToAdd)
                };

                this.chunksListToAdd = [];
                this.set('chunksListToAdd', this.chunksListToAdd);
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