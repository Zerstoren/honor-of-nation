requirejs.config({
    baseUrl: '/js/',
    waitSeconds: 30,
    paths: {
        app: '/js/'
    }
});

define('system/bootstrap', ['system/router', 'libs/socket'], function(routes, Socket) {
    'use strict';

    var route, item, data, RouterBone, router, controllerMethodLeave,
        events = _.clone(Backbone.Events);

    route = {};
    route.routes = {};

    function routeFunc(routeController, routeMethod) {
        var controllerMethod;


        function triggerCall(routeController, routeMethod) {
            events.trigger(
                'route',
                routeController,
                routeMethod,
                'route'
            );

            events.trigger(
                ['route', routeController].join(":"),
                routeController,
                routeMethod,
                ['route', routeController].join(":")
            );

            events.trigger(
                ['route', routeController, routeMethod].join(":"),
                routeController,
                routeMethod,
                ['route', routeController, routeMethod].join(":")
            );

            console.log('route = ' + [routeController, routeMethod].join(":"));
        }

        return function () {
            var args = arguments;
            requirejs(['controller/' + routeController], function(controller) {
                if (controller[routeMethod] === undefined) {
                    throw new Error('Route method ' + routeMethod + ' not found in controller ' + routeController);
                }

                if (controllerMethodLeave) {
                    controllerMethodLeave();
                }

                controllerMethod = controller[routeMethod];
                controllerMethodLeave = controller['leave' + routeMethod.charAt(0).toUpperCase() + routeMethod.slice(1)];

                triggerCall(routeController, routeMethod);
                controllerMethod.apply(this, Array.prototype.slice.call(args));
            });
        };
    }

    route.navigate = function (path, trigger, replace) {
        if (!trigger) {
            trigger = true;
        }

        Backbone.Router.prototype.navigate.apply(this, [path, {
            trigger : trigger === undefined ? true : trigger,
            replace : replace === undefined ? false : replace
        }]);
    };

    route.initialize = function () {
        Backbone.Router.prototype.initialize.apply(this, arguments);

        var routePath;
        for (item in routes) {
            if (routes.hasOwnProperty(item)) {
                data = item.split('/');
                routePath = routes[item];

                this[item] = routeFunc(data[0], data[1]);
                this.route(routePath, item);
            }
        }
    };

    RouterBone = Backbone.Router.extend(route);

    router = new RouterBone();
    define('system/route', function () {
        return router;
    });

    define('system/socket', function () {
        return new Socket(window.socketHost || '127.0.0.1', window.port || localStorage.port || 10585);
    });

    if (window.env === 'production') {
        jQuery(document).contextmenu(function (e) {
            e.stopPropagation();
            return false;
        });
    }

    requirejs([
        'libs/abstract/collection',
        'libs/abstract/factory',
        'libs/abstract/gateway',
        'libs/abstract/model',
        'libs/abstract/service',
        'libs/abstract/view'
    ], function () {
        requirejs(['system/preStart', 'system/config'], function () {
            Backbone.history.start({pushState: true});
        });
    });

    return events;
});

requirejs([
    'system/bootstrap'
], function() {

});