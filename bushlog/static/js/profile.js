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

        // initialise form validation
        $('.form-signup').validate({
            messages: {
                "signup-username": {
                    required: "Username is required.",
                    remote: "Username entered is already in use."
                },
                "signup-email": {
                    required: "Email is required.",
                    remote: "Email entered is already registered."
                },
                "signup-password": {
                    required: "Password is required."
                },
                "signup-confirm_password": {
                    required: "Password confirmation is required.",
                    equalTo: "Passwords don't match."
                }
            },
            success: function(label) {
                label.html('<i class="icon-ok"></i>');
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
                    required: "Email is required.",
                    remote: "Email entered is already registered."
                },
                "update-password": {
                    required: "Password is required."
                },
                "update-confirm_password": {
                    required: "Password confirmation is required.",
                    equalTo: "Passwords don't match."
                }
            }
        });
    });
}

initResetPasswprdForm = function () {
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

$(document).ready(function() {

    // initialise profile forms
    initSignInForm();
    initSignUpForm();
    initUpdateForm();
    initResetPasswprdForm();

    // initialise the modals with required options
    $('#id_signup_modal').modal({
        keyboard: false,
        show: false
    });
    $('#id_update_modal').modal({
        keyboard: false,
        show: false
    });
});
