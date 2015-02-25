define('libs/abstract/factory', [], function () {
    window.AbstractFactory = function () {
        this.initialize.apply(this, arguments);
    };

    _.extend(window.AbstractFactory.prototype, Backbone.Events, {
        __pool: null,
        index: '_id',
        domain: null,

        initialize: function () {
            this.__pool = {};
        },

        getFromPool: function (id) {
            return this.__pool[id];
        },

        pushToPool: function (domain) {
            if (!(domain instanceof this.domain)) {
                throw new Error('Try add wrong domain instance');
            }

            if (this.getFromPool(domain.get(this.index)) !== undefined) {
                throw new Error('Domain already in pool');
            }

            this.__pool[domain.get(this.index)] = domain;
        },

        getDomainFromData: function (data) {
            if (!data || !data._id) {
                return new this.domain(data);
            }

            var domain = this.getFromPool(data._id);

            if (domain === undefined) {
                domain = new this.domain(data);
                this.pushToPool(domain);
            }
            domain.set(data);

            return domain;
        },

        updateDomainFromData: function (data) {
            var domain;

            if (!(domain = this.getFromPool(data._id))) {
                return null;
            }

            domain.set(data);

            return domain;
        },

        searchInPool: function (index, value) {
            var item, result = [];

            for (item in this.__pool) {
                if (this.__pool.hasOwnProperty(item)) {
                    if (this.__pool[item].get(index) === value) {
                        result.push(this.__pool[item]);
                    }
                }
            }

            return result;
        }
    });

    window.AbstractFactory.extend = Backbone.Model.extend;
});