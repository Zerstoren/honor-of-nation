define('view/elements/tooltip', [], function () {
    var Tooltip = function (view, holder) {
        this.__tooltip = null;
        this.uniqueId = _.uniqueId().toString();

        this.view = view;
        this.holder = holder;

        this.view['__onShowHint-' + this.uniqueId] = this.onShowHint.bind(this);
        this.view['__onHideHint-' + this.uniqueId] = this.onHideHint.bind(this);

        this.view.events["mouseenter " + this.holder] = "__onShowHint-" + this.uniqueId;
        this.view.events["mouseout " + this.holder] = "__onHideHint-" + this.uniqueId;
        this.view.events["focus " + this.holder] = "__onHideHint-" + this.uniqueId;
    };

    Tooltip.prototype.destroy = function () {
        delete this.view['__onShowHint-' + this.uniqueId];
        delete this.view['__onHideHint-' + this.uniqueId];

        delete this.view.events["mouseenter " + this.holder];
        delete this.view.events["mouseout " + this.holder];
        delete this.view.events["focus " + this.holder];
    };

    Tooltip.prototype.onShowHint = function (e) {
        this.__tooltip = jQuery(e.target);
        this.__tooltip.tooltip({
            trigger: '',
            title: this.__tooltip.data('hint'),
            placement: 'right',
            container: 'body'
        });

        this.__tooltip.tooltip('show');
    };

    Tooltip.prototype.onHideHint = function () {
        this.__tooltip.tooltip('destroy');
    };

    return Tooltip;
});