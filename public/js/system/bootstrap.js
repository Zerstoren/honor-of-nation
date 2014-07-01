requirejs.config({
    baseUrl: '/js/',

    paths: {
        app: '/js/'
    }
});

define('system/bootstrap', ['system/router', 'libs/socket'], function(routes, Socket) {
    'use strict';

    var route, item, data, RouterBone, router,
        events = _.clone(Backbone.Events);

    route = {};
    route.routes = {};

    function routeFunc(routeController, routeMethod) {
        var controllerMethod, returnFunction;

        requirejs(['controller/' + routeController], function(controller) {
            if (controller[routeMethod] === undefined) {
                throw new Error('Route method ' + routeMethod + ' not found in controller ' + routeController);
            }

            controllerMethod = controller[routeMethod];
        });

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

        returnFunction = function() {
            if (controllerMethod === undefined) {
                var scope = this,
                    args = Array.prototype.slice.call(arguments);

                setTimeout(function() {
                    returnFunction.apply(scope, args);
                }, 50);
                return;
            }

            triggerCall(routeController, routeMethod);
            controllerMethod.apply(this, Array.prototype.slice.call(arguments));
        };

        return returnFunction;
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
    Backbone.history.start({pushState: true});

    define('system/socket', function () {
        return new Socket('127.0.0.1', 8080);
    });

    define('system/route', function () {
        return router;
    });

    return events;
});

requirejs(['system/bootstrap', 'system/preStart', 'system/config'], function() {
    'use strict';
});