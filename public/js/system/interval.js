define('system/interval', [], function () {

    var result = AbstractService.extend({
        nums: {},
        events: {},
        EVERY_1_SEC: 24,

        initialize: function () {
            var self = this,
                requestFrame;

            this.frame = 0;

            this.nums[this.EVERY_1_SEC] = 0;
            this.events[this.EVERY_1_SEC] = [];

            requestFrame = function () {
                self.processFrame();
                window.requestAnimationFrame(requestFrame);
            };

            window.requestAnimationFrame(requestFrame);
        },

        processFrame: function () {
            this.frame += 1;

            if (this.nums[this.EVERY_1_SEC] && this.frame % this.EVERY_1_SEC === 0) {
                this.trigger(this.EVERY_1_SEC);
//                this.loop(this.EVERY_1_SEC);
            }
        },

//        loop: function (name) {
//            var i = 0;
//            for (; i < this.events[name].length; i++) {
//                this.events[name][i]();
//            }
//        },

        on: function (string, fn, context) {
            this.nums[string] += 1;
            AbstractService.prototype.on(string, fn, context);
//            this.events[string].push(fn);
        },

        un: function (string, fn, context) {
            this.nums[string] -= 1;
            AbstractService.prototype.un(string, fn, context);
//            this.events[string].remove(fn);
        }
    });

    return new result();
});