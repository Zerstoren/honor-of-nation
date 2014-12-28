window.DefferedTrigger = function () {
    this.value = null;
    this.callbacks = {};
    this.callbacks[DefferedTrigger.ON_UPDATE] = [];
    this.callbacks[DefferedTrigger.ON_GET] = [];
};

window.DefferedTrigger.ON_GET = 1;
window.DefferedTrigger.ON_UPDATE = 2;
window.DefferedTrigger.ON_GET_AND_UPDATE = 3;

window.DefferedTrigger.prototype.set = function (value) {
    if (this.value === null) {
        this._call(DefferedTrigger.ON_GET, value);
        this._call(DefferedTrigger.ON_UPDATE, value);

        this.callbacks[DefferedTrigger.ON_GET] = [];
    }

    this._call(DefferedTrigger.ON_UPDATE, value);

    this.value = value;
};

window.DefferedTrigger.prototype.deffer = function (action, callback) {
    if ((action === DefferedTrigger.ON_GET || action === DefferedTrigger.ON_GET_AND_UPDATE) && this.value) {
        callback(this.value);
    }

    if (action === DefferedTrigger.ON_GET_AND_UPDATE) {
        this.callbacks[DefferedTrigger.ON_GET].push(callback);
        this.callbacks[DefferedTrigger.ON_UPDATE].push(callback);
    } else {
        this.callbacks[action].push(callback);
    }
};

window.DefferedTrigger.prototype._call = function (action, value) {
    var i, callback;

    for (i = 0; i < this.callbacks[action].length; i++) {
        callback = this.callbacks[action][i];
        callback(value);
    }
};
