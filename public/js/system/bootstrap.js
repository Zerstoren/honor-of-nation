requirejs.config({
    baseUrl: '/js/',

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
        var controllerMethod,
            args = arguments;


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

    for (item in routes) {
        if (routes.hasOwnProperty(item)) {
            data = routes[item].split('/');

            route.routes[item] = routes[item];
            route[routes[item]] = routeFunc(data[0], data[1]);
        }
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
    RouterBone = Backbone.Router.extend(route);

    router = new RouterBone();
    define('system/route', function () {
        return router;
    });

    define('system/socket', function () {
        return new Socket('127.0.0.1', localStorage.port || 8080);
    });


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