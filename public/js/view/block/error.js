define('view/block/error', [
    'libs/alertify',
], function (alertify) {
    'use strict';

    var ErrorBlock = AbstractView.extend({
        initialize: function () {
        },

        showLoginForm: function () {
            alert('Need auth');
        },

        showErrorBox: function (message) {
            var errorText = '';

            if (_.isObject(message)) {
                errorText += '<div>Code: ' + message.code + '</div>';
                errorText += '<div>Message: ' + message.error + '</div>';
            } else {
                errorText = message;
            }

            if (message.traceback) {
                errorText += '<div><pre><code>' + message.traceback + '</code></pre></div>';
            }

            alertify.error(errorText, 0);
        },

        showSuccessBox: function (message) {
            alertify.success(message);
        }
    });

    return new ErrorBlock();
});
