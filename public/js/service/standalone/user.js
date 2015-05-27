define('service/standalone/user', [
    'system/socket',
    'system/route',
    'libs/alertify',

    'model/user',

    'view/user/auth'
], function (
    systemSocket,
    systemRoute,
    libsAlertify,

    ModelUser,
    ViewUserAuth
) {

    var User = AbstractService.extend({
        STATE_WAR      : 0,
        STATE_NEUTRAL  : 1,
        STATE_TRADE    : 2,
        STATE_UNION    : 3,
        STATE_ALLIANCE : 4,

        initialize: function () {
            this.getMeFn = [];
            this.states = {};
            this.defferTrigger = new window.DefferedTrigger();
        },

        me: new ModelUser(),

        viewUserAuth: null,

        getDeffer: function () {
            return this.defferTrigger;
        },

        getStateFor: function (userId) {
            return this.states[userId];
        },

        login: function () {
            if (localStorage.authLogin === undefined) {
                this.redirectToLoginForm();
            } else {
                var login = localStorage.authLogin,
                    password = localStorage.authPassword;

                this.onLogin({
                    login: login,
                    password: password,
                    auto: true
                });
            }
        },

        renderForm: function () {
            if (this.viewUserAuth === null) {
                this.viewUserAuth = new ViewUserAuth();
                this.viewUserAuth.on('login', this.onLogin, this);
            }

            require(['system/preStart'], function (systemPreStart) {
                this.viewUserAuth.render(systemPreStart.no.body.getHolder());
            }.bind(this));
        },

        onLogin: function (data) {
            var self = this;

            this.me.auth(data.login, data.password, function (domain, authResult, states) {
                if (authResult === false) {
                    if (data.auto === true) {
                        self.renderForm();
                    } else {
                        libsAlertify.error('Логин или пароль указаны не верно');
                    }
                    return;
                } else {
                    localStorage.authLogin = data.login;
                    localStorage.authPassword = data.password;

                    if (self.viewUserAuth) {
                        self.viewUserAuth.clean();
                    }
                }

                self.defferTrigger.set(self.me);

                _.each(states, function (item) {
                    self.states[item.user] = item.state;
                });
            });
        },

        redirectToLoginForm: function () {
            systemRoute.navigate('login');
        }
    });

    return new User();
});

