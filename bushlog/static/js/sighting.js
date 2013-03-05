initNewSightingForm = function () {
    $.get('/sighting/create/', function(data) {

        console.log(data)

        // loads the form into the form container and sets the submit action
        $('.new_sighting-container').append(data);
        $('.btn-new_sighting-submit').click(function(){
            $('.form-new_sighting').submit();
        });

    });
}

$(document).ready(function() {

    // initialise sightings forms
    initNewSightingForm();

    // initialise the modals with required options
    $('#id_new_sighting').modal({
        keyboard: false,
        show: false
    });
});
