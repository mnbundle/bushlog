initSignInForm = function () {
    $.get('/profile/signin/', function(data) {

        // loads the form into the form container and sets the submit action
        $('.signin-container').append(data);
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

        $.validator.addMethod("validpassword", function(value, element) {
            return this.optional(element) || /^.*(?=.{8,})(?=.*[a-z])(?=.*[A-Z])(?=.*[\d]).*$/.test(value);
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
                    validpassword: "must contain upper & lower case letters and a number."
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
        $('#id_datepicker').datepicker();

        // initialise form validation
        $('.form-update').validate({
            messages: {
                "update-email": {
                    remote: "is already registered."
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

        // initialise form validation
        $('.form-resetpassword').validate({
            messages: {
                "reset_password-email": {
                    required: "Email is required.",
                    remote: "Email entered is not registered."
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
                    required: "Email is required.",
                    remote: "Email entered is not registered."
                }
            }
        });
    });
}

$(document).ready(function() {

    // initialise profile forms
    initSignInForm();
    initSignUpForm();
    initResetPasswordForm();
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
    $('#id_resendactivation_modal').modal({
        keyboard: false,
        show: false
    });
});
