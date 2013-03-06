enableCarouselControl = function (carousel_ele, ele, action) {
    ele.click(function(){
        carousel_ele.carousel(action);
    }).removeClass("disabled");
}

disableCarouselControl = function (ele) {
    ele.unbind("click").addClass("disabled");
}

initNewSightingForm = function () {
    $.get('/sighting/create/', function(data) {

        // loads the form into the form container and sets the submit action
        $('.new_sighting-container').append(data);
        $('.btn-new_sighting-submit').click(function(){
            $('.form-new_sighting').submit();
        });

        // initialise the form wizard controls
        var carousel_ele = $("#new_sighting-carousel").carousel({
            interval: false
        });
        var next_btn = $("#btn-next");
        var prev_btn = $("#btn-prev");

        enableCarouselControl(carousel_ele, next_btn, "next");

        carousel_ele.bind('slid', function (){
            if($('#new_sighting-carousel .carousel-inner .item:first').hasClass('active')) {
                disableCarouselControl(prev_btn);
                enableCarouselControl(carousel_ele, next_btn, "next");
            }
            else if($('#new_sighting-carousel .carousel-inner .item:last').hasClass('active')) {
                disableCarouselControl(next_btn);
                enableCarouselControl(carousel_ele, prev_btn, "prev");
            }
            else {
                enableCarouselControl(carousel_ele, prev_btn, "prev");
                enableCarouselControl(carousel_ele, next_btn, "next");
            }
        });

        // initialise the file inputs to use upload kit
        $('input.uk-input[type="file"]').each(function(index, element) {
            new UploadKit(element);
        });

        $('input.uk-input[type="file"]').bind(UKEventType.FileUploaded, function(e) {
            var data = $.parseJSON(e.response.response);
            var image_ids_ele = $("#id_image_ids");

            var image_ids = image_ids_ele.val();
            if(image_ids) {
                image_ids = image_ids + "," + data.id;
            }
            else {
                image_ids = data.id;
            }
            image_ids_ele.val(image_ids);
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
