define('system/errorHandler', [
    'system/socket'
], function (socket) {
    window.consoleLog = [];
    var ErrorHandler = AbstractService.extend({
        consoleLog: window.consoleLog,
        init: function () {
            window.onerror = this.onError.bind(this);
            //this.initConsole();
        },

        initConsole: function () {
            var self = this, consoleDump = console.log;
            console.log = function () {
                var args = Array.prototype.slice.call(arguments);
                self.consoleLog.push(args);
            };
        },

        onError: function (error, file, line, charPlace, stack) {
            var errorData = {
                "error": error,
                "file": "Error in file " + file + " line " + line + " char " + charPlace,
                "stack": stack.stack
            };

            socket.send('/system/error', errorData);

            this.printInWindow(errorData);
        },

        printInWindow: function (data) {
            var body = jQuery(document.body);

            body.append(
                '<pre class="error">' + data.error + '\n\n' + data.file + '\n\n' + data.stack + '</pre>'
            );
        },

        sendDebug: function (msg) {
            var errorData = {
                "error": msg,
                "file": "",
                "stack": ""
            };

            socket.send('/system/log', errorData);
        }
    });

    return new ErrorHandler();
});

