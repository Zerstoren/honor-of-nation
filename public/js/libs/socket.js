/**
 * Класс-абстракция над веб сокетами. Доступны только современные браузеры.
 */
define('libs/socket', function() {
    "use strict";

    var Socket = function(host, port) {
        this.counter = 0;
        this.logsend = [];
        this.init(host, port);
    };

    Socket.prototype.pool = null;

    /**
     * Автоматически иницилизатор соединения и всего остального
     * @return {void}
     */
    Socket.prototype.init = function(host, port) {
        this.pool = [];

        this.host = host;
        this.port = port;

        this.need_reconnect = true;

        this.nextMessageIsSingle = false;
        this.collectMessages = false;

        if(window.MozWebSocket && window.WebSocket === undefined) {
            window.WebSocket = window.MozWebSocket;
        }

        this.listeners = {};

        // Bugfix for old Firefox MozWebSocket
        // Don`t disconnect, before close browser
        // Close socket on tab close
        window.addEventListener('beforeunload', this.close.bind(this));
        this.$Socket_timeoutUnload();
    };

    /**
     * Установка соединения с сервером
     * @param reconnect {boolean} Установить соединение, как повторное.
     * @return {void}
     */
    Socket.prototype.connect = function(reconnect) {
        if(reconnect !== undefined) {
            this.need_reconnect = reconnect;
        }

        if(this.ws !== undefined) {
            return;
        }

        this.ws = new window.WebSocket('ws://' + this.host + ':' + this.port + '/');
        this.ws.onopen = this.onOpen.bind(this);
        this.ws.onclose = this.onClose.bind(this);
        this.ws.onmessage = this.onMessage.bind(this);
        this.ws.onerror = this.onError.bind(this);
    };

    /**
     * Дает команду следующему запросу уйти немедленно, обходя пул сообщений
     * @return {void}
     */
    Socket.prototype.single = function() {
        this.nextMessageIsSingle = true;
    };

    /**
     * Принудительно выгружает все запросы, которые попали в пул сообщений
     * @return {void}
     */
    Socket.prototype.unload = function() {
        if(this.ws === undefined || this.ws.readyState !== 1) {
            return;
        }

        if(this.pool.length === 0) {
            return;
        }

        this.collectMessages = false;

        this.ws.send(JSON.stringify({
            collection: this.pool
        }));

        this.pool = [];
    };

    /**
     * Начинает сбор сообщений, игнорируя таймаутовские выгрузки
     * Выгрузка произойдет только по вызову unload
     *
     * @return {void}
     */
    Socket.prototype.collect = function() {
        this.collectMessages = true;
    };

    /**
     * Отправка сообщения на сервер
     * @param  {string}   module  Имя модуля
     * @param  {object}   message Объект сообщения
     * @param  {function} asyncFn Callback функция, для асинхронных запросов
     * @return {void}
     */
    Socket.prototype.send = function(module, message, asyncFn) {

        if(module.length !== 1 && (module[0] !== '/' || module[module.length -1] === '/')) {
            throw new Error('Wrong path type');
        }

        var data, asyncName = false;

        window.console.log('%cSend message: ' + module + ' - %o', 'color: #aaa;', message);
        this.logsend.push('%cSend message: ' + module + ' - %o', 'color: #aaa;', message);

        if(asyncFn) {
            this.counter += 1;
            asyncName = Math.random();
            this.listeners[asyncName] = asyncFn;
        }

        data = {
            module: module,
            message: message,
            async: asyncName
        };

        if((this.ws === undefined || this.ws.readyState !== 1) && this.nextMessageIsSingle) {
            this.pool.push(data);
            return;
        }

        if(this.nextMessageIsSingle) {
            this.nextMessageIsSingle = false;
            this.ws.send(JSON.stringify(data));
        } else {
            this.pool.push(data);
        }
    };

    /**
     * Закрывает сокет соединение
     * @return {void}
     */
    Socket.prototype.close = function() {
        this.need_reconnect = false;
        this.ws.close();
        this.ws = undefined;
        this.trigger('close');
    };

    /**
     * Получение сообщения с сервера
     * @param  {object} data Сообщение с сервера
     * @return {void}
     */
    Socket.prototype.onMessage = function(data) {
        var i,
            message = JSON.parse(data.data);

        if(message.collection) {
            for(i = 0; i < message.collection.length; i += 1) {
                this.$Socket_OnMessageGet(message.collection[i]);
            }
        } else {
            this.$Socket_OnMessageGet(message);
        }
    };

    Socket.prototype.$Socket_OnMessageGet = function(message) {
        window.console.log('%cGet message: ' + message.module + ' - %o', 'color: #aaa;',  message.message);
        this.logsend.push('%cGet message: ' + message.module + ' - %o', 'color: #aaa;',  message.message);

        if (message.message.done) {
            this.trigger('message' + message.module, message.message);
        }

        if(message.async !== null && this.listeners[message.async]) {
            this.counter -= 1;
            this.listeners[message.async](message.message);
            delete this.listeners[message.async];
        }
    };

    /**
     * Событие открытия соединения с сервером
     * @return {void}
     */
    Socket.prototype.onOpen = function() {
        this.unload();
        this.trigger('connect');
    };

    /**
     * Событие закрытия соединения с сервером
     * @return {void}
     */
    Socket.prototype.onClose = function() {
        if(this.need_reconnect) {
            var self = this;
            this.ws.close();
            this.ws = undefined;
            setTimeout(function() {
                self.connect(true);
            }, 1000);
        } else {
            this.trigger('close');
        }
    };

    Socket.prototype.onError = function(e) {
        if (e.type === 'error') {
            switch(e.currentTarget.readyState) {
                case 0:
                    this.trigger('error:notOpen');
                    break;
                case 2:
                    this.trigger('error:close');
                    break;
                case 3:
                    this.trigger('error:closed');
                    break;
            }
        }

        this.trigger('error');
    };

    Socket.prototype.$Socket_timeoutUnload = function() {
        var self = this;

        setInterval(function() {
            if(self.collectMessages) {
                return false;
            }

            self.unload();

            return true;
        }, 50);
    };

    Socket.prototype = _.extend(Socket.prototype, Backbone.Events);

    return Socket;
});
