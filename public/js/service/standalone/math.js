define('service/standalone/math', [
    'system/config'
], function (config) {
    var math,
        Mathematic = AbstractService.extend({
        percent: function (value, percent) {
            return parseInt(value / 100 * percent, 10);
        },

        rate: function (value) {
            return parseInt(value * config.getBaseRate() / 100, 10);
        },

        getBuildPrice: function (price, level, drop) {
            var i,
                buildPrice = config.getRateBuildUp();

            drop = drop || 1;
            price = _.clone(price);

            for (i = 0; i < level; i++) {
                price.wood += this.percent(price.wood, buildPrice);
                price.rubins += this.percent(price.rubins, buildPrice);
                price.stone += this.percent(price.stone, buildPrice);
                price.steel += this.percent(price.steel, buildPrice);
                price.time += this.percent(price.time, buildPrice);
            }

            return {
                wood: parseInt(this.rate(price.wood) * drop, 10),
                rubins: parseInt(this.rate(price.rubins) * drop, 10),
                stone: parseInt(this.rate(price.stone) * drop, 10),
                steel: parseInt(this.rate(price.steel) * drop, 10),
                time: parseInt(this.rate(price.time) * drop, 10)
            };
        }
    });

    math = new Mathematic();
    return math;
});