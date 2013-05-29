initSignInForm = function () {
    $.get('/profile/signin/', function(data) {

        // loads the form into the form container and sets the submit action
        $('.signin-container').append(data);
        $('.loader').hide();
        $('.btn-signin-submit').click(function(){
            $('.form-signin').submit();
        });

    });
}

initSignUpForm = function () {
    $.get('/profile/signup/', function(data) {

        // loads the form into the form container and sets the submit action
        $('.signup-container').html(data);
        $('.btn-signup-submit').click(function(){
            $('.form-signup').submit();
        });

        // add a validation method for valid passwords
        $.validator.addMethod("validpassword", function(value, element) {
            return this.optional(element) || /^.*(?=.{6,})(?=.*[a-z])(?=.*[\d]).*$/.test(value);
        });

        // initialise form validation
        $('.form-signup').validate({
            messages: {
                "signup-username": {
                    remote: "is already in use."
                },
                "signup-email": {
                    remote: "is already registered."
                },
                "signup-password": {
                    validpassword: "must be 6 characters long and contain at least one number."
                },
                "signup-confirm_password": {
                    equalTo: "doesn't match password field."
                }
            }
        });
    });
}

initUpdateForm = function () {
    $.get('/profile/update/', function(data) {

        // loads the form into the form container and sets the submit action
        $('.update-container').html(data);
        $('.btn-update-submit').click(function(){
            $('.form-update').submit();
        });

        // initialise the datepicker
        $('#id_datepicker').datepicker({
            autoclose: true
        });

        // initialise form validation
        $('.form-update').validate({
            messages: {
                "update-username": {
                    remote: "is already registered."
                },
                "update-email": {
                    remote: "is already registered."
                }
            }
        });
    });
}

initAvatarForm = function () {
    $.get('/profile/avatar/', function(data) {

        // loads the form into the form container
        $('.avatar-container').html(data);

        // initialise the file inputs to use upload kit
        $('#id_avatar-avatar').each(function (index, element) {
            new UploadKit(element);
        });

        $('#id_avatar-avatar').bind(UKEventType.FileUploaded, function(event) {
            var data = $.parseJSON(event.response.response);
            window.location = data.redirect_url;
        });
    });
}

initForgotPasswordForm = function () {
    $.get('/profile/forgot-password/', function(data) {

        // loads the form into the form container and sets the submit action
        $('.forgotpassword-container').html(data);
        $('.btn-forgotpassword-submit').click(function(){
            $('.form-forgotpassword').submit();
        });

        // initialise form validation
        $('.form-forgotpassword').validate({
            messages: {
                "forgot_password-email": {
                    remote: "is not registered."
                }
            }
        });
    });
}

initResetPasswordForm = function () {
    $.get('/profile/reset-password/', function(data) {

        // loads the form into the form container and sets the submit action
        $('.resetpassword-container').html(data);
        $('.btn-resetpassword-submit').click(function(){
            $('.form-resetpassword').submit();
        });

        // add a validation method for valid passwords
        $.validator.addMethod("validpassword", function(value, element) {
            return this.optional(element) || /^.*(?=.{6,})(?=.*[a-z])(?=.*[\d]).*$/.test(value);
        });

        // initialise form validation
        $('.form-resetpassword').validate({
            messages: {
                "reset_password-password": {
                    validpassword: "must be 6 characters long and contain at least one number."
                },
                "reset_password-confirm_password": {
                    equalTo: "doesn't match password field."
                }
            }
        });
    });
}

initActivationForm = function () {
    $.get('/profile/activate/', function(data) {

        // loads the form into the form container and sets the submit action
        $('.activate-container').html(data);
        $('.btn-activate-submit').click(function(){
            $('.form-activate').submit();
        });

        // add a validation method for valid passwords
        $.validator.addMethod("validpassword", function(value, element) {
            return this.optional(element) || /^.*(?=.{6,})(?=.*[a-z])(?=.*[\d]).*$/.test(value);
        });

        // initialise form validation
        $('.form-activate').validate({
            messages: {
                "activate-email": {
                    remote: "is already registered."
                },
                "activate-password": {
                    validpassword: "must be 6 characters long and contain at least one number."
                },
                "activate-confirm_password": {
                    equalTo: "doesn't match password field."
                }
            }
        });
    });
}

initResendActivationForm = function () {
    $.get('/profile/resend-activation/', function(data) {

        // loads the form into the form container and sets the submit action
        $('.resendactivation-container').html(data);
        $('.btn-resendactivation-submit').click(function(){
            $('.form-resendactivation').submit();
        });

        // initialise form validation
        $('.form-resendactivation').validate({
            messages: {
                "resend_activation-email": {
                    remote: "is not registered."
                }
            }
        });
    });
}

$(document).ready(function() {

    // initialise profile forms
    initSignInForm();
    initSignUpForm();
    initForgotPasswordForm();
    initResetPasswordForm();
    initActivationForm();
    initResendActivationForm();

    // initialise the modals with required options
    $('#id_signup_modal').modal({
        keyboard: false,
        show: false
    });
    $('#id_resetpassword_modal').modal({
        keyboard: false,
        show: false
    });
    $('#id_activate_modal').modal({
        keyboard: false,
        show: false
    });
    $('#id_resendactivation_modal').modal({
        keyboard: false,
        show: false
    });
});
