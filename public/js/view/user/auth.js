define('view/user/auth', [
    'libs/alertify'
], function (
    libsAlertify
) {
    'use strict';

    return AbstractView.extend({
        events: {
            "click .auth__button": "onSubmit"
        },

        initialize: function () {
            this.$el.html(this.getTemplate('user/login'));
            this.loginInput = this.$el.find('.auth__input_login');
            this.passwordInput = this.$el.find('.auth__input_password');
        },

        render: function (holder) {
            this.holder = holder;
            holder.append(this.$el);
        },

        clean: function () {
            if (this.holder) {
                this.holder.empty();
            }
        },

        onSubmit: function (e) {
            if (this.loginInput.val() === '' || this.passwordInput.val() === '') {
                libsAlertify.error('Одно из полей в форме пустое');
                return;
            }

            this.trigger('login', {
                login: this.loginInput.val(),
                password: this.passwordInput.val()
            });
        }
    });
});
