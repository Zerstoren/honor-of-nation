define('service/standalone/map/eventWrapper', [], function () {

    return AbstractService.extend({
        initialize: function (e) {
            this._x = e.position.x;
            this._y = e.position.y;

            this._e = e;

            this._shadow = null;

            this._land = null;
            this._landType = null;

            this._decor = null;

            this._buildType = null;
            this._build = null;

            this._unitType = null;
            this._unit = null;

            this._unitsList = [];
        },

        e: function () {
            return this._e;
        },

        x: function() {
            return this._x;
        },

        y: function() {
            return this._y;
        },

        shadow: function() {
            return this._shadow;
        },

        land: function() {
            return this._land;
        },

        landType: function() {
            return this._landType;
        },

        decor: function() {
            return this._decor;
        },

        buildType: function() {
            return this._buildType;
        },

        build: function() {
            return this._build;
        },

        unitType: function() {
            return this._unitType;
        },

        unit: function() {
            return this._unit;
        },

        unitList: function () {
            return this._unitsList;
        },

        setShadow: function (shadow) {
            this._shadow = shadow;
        },

        setLand: function (land, landType) {
            this._land = land;
            this._landType = landType;
        },

        setDecor: function (decor) {
            this._decor = decor;
        },

        setBuild: function (type, domain) {
            this._buildType = type;
            this._build = domain;
        },

        setUnit: function (type, domain) {
            this._unitType = type;
            this._unit = domain;

            this._unitsList.push({
                type: type,
                domain: domain
            });
        }
    });

});