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
        initialize: function () {
            this.getMeFn = [];
            this.defferTrigger = new window.DefferedTrigger();
        },

        me: new ModelUser(),

        viewUserAuth: null,

        getDeffer: function () {
            return this.defferTrigger;
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

            this.me.auth(data.login, data.password, function (domain, authResult) {
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

            });
        },

        redirectToLoginForm: function () {
            systemRoute.navigate('login');
        }
    });

    return new User();
});

