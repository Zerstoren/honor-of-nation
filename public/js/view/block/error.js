define('view/block/error', [
    'libs/alertify',
    'system/template'
], function (alertify, template) {
    'use strict';

    var ErrorBlock = Backbone.View.extend({
        initialize: function () {
        },

        showLoginForm: function () {
            alert('Need auth');
        },

        showErrorBox: function (message) {
            var errorText = '<div>Code: ' + message.code + '</div>';
            errorText += '<div>Message: ' + message.error + '</div>';

            if (message.traceback) {
                errorText += '<div><pre><code>' + message.traceback + '</code></pre></div>';
            }

            alertify.error(errorText, 0);
        }
    });

    return new ErrorBlock();
});
