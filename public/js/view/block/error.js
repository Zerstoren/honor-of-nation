define('view/block/error', [
    'libs/alertify'
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
            if (this.boxConnection) {
                this.boxConnection.detach();

                if (this.boxConnectionTimeout) {
                    clearTimeout(this.boxConnectionTimeout);
                }
            }

            var html = '' +
            '<div class="connect-is-not-estabilished"><div class="text">' +
                'Сервер недоступен. Повтор соединения происходит автоматически' +
            '</div><div class="window-glass"></div></div>';

            jQuery('body').append(html);

            this.boxConnection = jQuery('body .connect-is-not-estabilished');
        },

        _connectionIsEstablished: function () {
            if (this.boxConnection) {
                var boxConnection = this.boxConnection;

                boxConnection.removeClass('connect-is-not-estabilished');
                boxConnection.addClass('connect-is-estabilished');
                boxConnection.find('.text').text('Соединение установлено, простите за неудобства');

                this.boxConnectionTimeout = setTimeout(function () {
                    boxConnection.detach();
                    this.boxConnection = false;
                }.bind(this), 4000);
            }
        }
    });

    return new ErrorBlock();
});
