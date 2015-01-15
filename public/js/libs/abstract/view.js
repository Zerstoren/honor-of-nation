define('libs/abstract/view', [
    'system/template',
    'view/block/error',
    'ractive'
], function (
    getTemplate,
    viewBlockError,
    Ractive
) {
    window.AbstractView = Backbone.View.extend({
        adapt: [Ractive.adaptors.Backbone],
        partials: {},
        initRactive: function () {
            this.ractive = new Ractive(this);
            this.set = this.ractive.set.bind(this.ractive);
            this.get = this.ractive.get.bind(this.ractive);
            this.teardown = this.ractive.teardown.bind(this.ractive);
        },

        setPartials: function (data) {
            var key;
            for (key in data) {
                if (data.hasOwnProperty(key)) {
                    this.partials[key] = this.getTemplate(data[key]);
                }
            }
        },

        data: {},

        getTemplate: getTemplate,

        delegateEvents: function (events) {
            Backbone.View.prototype.delegateEvents.apply(this, arguments);

            if (!(events || (events = _.result(this, 'events')))) return this;
            var delegateEventSplitter = /^(\S+) (global)$/;

            for (var key in events) {
                var method = events[key];
                if (!_.isFunction(method)) method = this[events[key]];
                if (!method) continue;

                var match = key.match(delegateEventSplitter);

                if(!match) continue;

                var eventName = match[1], selector = match[2];
                method = _.bind(method, this);
                eventName += '.delegateEvents' + this.cid;

                if (selector === 'global') {
                    $(document).on(eventName, method);
                }
            }

            return this;
        },

        undelegateEvents: function () {
            Backbone.View.prototype.undelegateEvents.apply(this, arguments);
            $(document).off('.delegateEvents' + this.cid);
            return this;
        },

        keyCodes: {
            // Alphabet
            a:65, b:66, c:67, d:68, e:69,
            f:70, g:71, h:72, i:73, j:74,
            k:75, l:76, m:77, n:78, o:79,
            p:80, q:81, r:82, s:83, t:84,
            u:85, v:86, w:87, x:88, y:89, z:90,
            // Numbers
            n0:48, n1:49, n2:50, n3:51, n4:52,
            n5:53, n6:54, n7:55, n8:56, n9:57,
            // Controls
            tab:  9, enter:13, shift:16, backspace:8,
            ctrl:17, alt  :18, esc  :27, space    :32,
            menu:93, pause:19, cmd  :91,
            insert  :45, home:36, pageup  :33,
            'delete':46, end :35, pagedown:34,
            // F*
            f1:112, f2:113, f3:114, f4 :115, f5 :116, f6 :117,
            f7:118, f8:119, f9:120, f10:121, f11:122, f12:123,
            // numpad
            np0: 96, np1: 97, np2: 98, np3: 99, np4:100,
            np5:101, np6:102, np7:103, np8:104, np9:105,
            npslash:11,npstar:106,nphyphen:109,npplus:107,npdot:110,
            // Lock
            capslock:20, numlock:144, scrolllock:145,

            // Symbols
            equals: 61, hyphen   :109, coma  :188, dot:190,
            gravis:192, backslash:220, sbopen:219, sbclose:221,
            slash :191, semicolon: 59, apostrophe: 222,

            // Arrows
            aleft:37, aup:38, aright:39, adown:40
        },

        setHolder: function (holder) {
            if (holder instanceof Backbone.$) {
                this.el = holder[0];
                this.$el = holder;
            } else {
                this.el = holder;
                this.$el = Backbone.$(holder);
            }
        },

        traverseEvent: function (eventName, fromView) {
            var traverseFn = function () {
                this.trigger.apply(this, [eventName]);
            }.bind(this);

            fromView.on(eventName, traverseFn, this);

            return function () {
                fromView.un(eventName, traverseFn, this);
            };
        },

        successMessage: function (str) {
            viewBlockError.showSuccessBox(str);
        },

        errorMessage: function (str) {
            viewBlockError.showErrorBox(str);
        }
    });
});