initSignInForm = function () {
    $.get('/profile/signin/', function(data) {
        $('.signin-container').append(data);
        $('.btn-signin-submit').click(function(){
            $('.form-signin').submit();
        });
    });
}

initSignUpForm = function () {
    $.get('/profile/signup/', function(data) {
        $('.signup-container').append(data);
        $('.btn-signup-submit').click(function(){
            $('.form-signup').submit();
        });
    });
}

$(document).ready(function() {
    // initialise the login form
    initSignInForm();
    initSignUpForm();

    // ensure the modal is hidden by default
    // $('#modalGeneric').modal('show');
});
