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
            }
        },

        on: function (string, fn, context) {
            this.nums[string] += 1;
            AbstractService.prototype.on(string, fn, context);
        },

        un: function (string, fn, context) {
            this.nums[string] -= 1;
            AbstractService.prototype.un(string, fn, context);
        }
    });

    return new result();
});