initLoginForm = function () {
    $.get('/profile/login/', function(data) {
        $('.login-container').append(data);
        $('.btn-submit').click(function(){
            $('.form-login').submit();
        });
    });
}

$(document).ready(function() {
    // initialise the login form
    initLoginForm();
});
