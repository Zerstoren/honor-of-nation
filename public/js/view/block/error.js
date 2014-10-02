define('view/block/error', [
    'libs/alertify',
], function (alertify) {
    'use strict';

    var ErrorBlock = Backbone.View.extend({
        initialize: function () {
            this.boxConnection = false;
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
        },

        _connectionIsNotEstablished: function () {
            if (!this.boxConnection) {
                this.boxConnection = jQuery('<div class="connect-is-not-estabilished">');
                this.boxConnection.text('Сервер недоступен. Повтор соединения происходит автоматически');

                jQuery('body').append(this.boxConnection);
            }
        },

        _connectionIsEstablished: function () {
            if (this.boxConnection) {
                var boxConnection = this.boxConnection;
                this.boxConnection = false;

                boxConnection.removeClass('connect-is-not-estabilished');
                boxConnection.addClass('connect-is-estabilished');
                boxConnection.text('Соединение установлено, простите за неудобства');

                setTimeout(function () {
                    boxConnection.detach();
                }, 5000);
            }
        }
    });

    return new ErrorBlock();
});
