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

        // add a validation method for valid passwords
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

        $('#id_avatar-avatar').bind(UKEventType.FileUploaded, function(e) {
            var data = $.parseJSON(e.response.response);
            window.location = data.redirect_url;
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
                    remote: "is not registered."
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

    // set an action for the close button if in phone resolution
    $('.btn-back').click(function (event) {
        event.preventDefault();
        history.back(1);
    });
});
