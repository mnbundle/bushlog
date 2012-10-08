initSignInForm = function () {
    $.get('/profile/signin/', function(data) {
        $('.signin-container').append(data);
        $('.btn-signin-submit').click(function(){
            $('.form-signin').submit();
        });
    });
}

$.validator.addMethod("unique", function(value, element) {
    return this.optional(element) || (parseFloat(value) > 0);
}, "* Amount must be greater than zero");

initSignUpForm = function () {
    $.get('/profile/signup/', function(data) {
        $('.signup-container').html(data);
        $('.btn-signup-submit').click(function(){
            $('.form-signup').submit();
        });
        $('.form-signup').validate({
            rules: {
                username: {
                    remote: "/profile/validate/"
                },
                email: {
                    remote: "/profile/validate/"
                },
                confirm_password: {
                    equalTo: "#id_password"
                }
            },
            messages: {
                username: {
                    remote: "That username is already in use."
                },
                email: {
                    remote: "That email is already registered."
                }
            }
        });
    });
}

validateUniqueNess = function (type, value) {
    $.get('/profile/validate/' + type + '/' + value + '/', function(data) {
        return data.unique;
    });
}

$(document).ready(function() {
    // initialise the login form
    initSignInForm();
    initSignUpForm();

    $.get('/profile/validate/username/qoda/', function(data) {
        console.log("Username: ");
        console.log(data);
    });

    $.get('/profile/validate/email/jpbydendyk@gmail.com/', function(data) {
        console.log("Email: ");
        console.log(data);
    });

    // ensure the modal is hidden by default
    // $('#modalGeneric').modal('show');
});
