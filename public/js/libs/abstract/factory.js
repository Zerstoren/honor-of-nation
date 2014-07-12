define('libs/abstract/factory', [], function () {
    window.AbstractFactory = function () {
        this.initialize.apply(this, arguments);
    };

    _.extend(window.AbstractFactory.prototype, Backbone.Events, {
        __pool: null,
        domain: null,

        initialize: function () {

        },

        getFromPool: function (id) {
            if (this.__pool === null) {
                this.__pool = {};
            }

            return this.__pool[id];
        },

        pushToPool: function (domain) {
            if (!(domain instanceof this.domain)) {
                throw new Error('Try add wrong domain instance');
            }

            if (this.__pool === null) {
                this.__pool = {};
            }

            if (this.getFromPool(domain.get('id')) !== undefined) {
                throw new Error('Domain already in pool');
            }

            this.__pool[domain.get('id')] = domain;
        },

        getDomainFromData: function (data) {
            if (!data.id) {
                return new this.domain(data);
            }

            if (this.__pool === null) {
                this.__pool = {};
            }

            var domain = this.getFromPool(data.id);

            if (domain === undefined) {
                domain = new this.domain(data);
                this.pushToPool(domain);
            }

            return domain;
        }
    });

    window.AbstractFactory.extend = Backbone.Model.extend;
});